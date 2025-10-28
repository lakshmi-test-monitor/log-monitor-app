import csv
from datetime import datetime
import logging
from typing import Dict, Tuple

# Configure logging
logging.basicConfig(
    filename='output.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LogMonitor:
    def __init__(self, log_file: str):
        """Initialize LogMonitor with the path to the log file."""
        self.log_file = log_file
        self.jobs: Dict[str, Dict] = {}  # Store job details by PID
        self.warning_threshold = 300  # 5 minutes in seconds
        self.error_threshold = 600   # 10 minutes in seconds

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse HH:MM:SS timestamp into a datetime object."""
        return datetime.strptime(timestamp_str, '%H:%M:%S')

    def process_log(self) -> None:
        """Read and process the log file."""
        try:
            with open(self.log_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 4:
                        logging.error(f"Invalid log entry: {row}")
                        continue
                    timestamp, job_desc, status, pid = row
                    self._process_entry(timestamp, job_desc, status, pid)
        except FileNotFoundError:
            logging.error(f"Log file {self.log_file} not found")
            raise
        except Exception as e:
            logging.error(f"Error processing log file: {str(e)}")
            raise

    def _process_entry(self, timestamp: str, job_desc: str, status: str, pid: str) -> None:
        """Process a single log entry."""
        try:
            ts = self.parse_timestamp(timestamp)
            if pid not in self.jobs:
                self.jobs[pid] = {'description': job_desc, 'start': None, 'end': None}

            if status == 'START':
                self.jobs[pid]['start'] = ts
            elif status == 'END':
                self.jobs[pid]['end'] = ts
            else:
                logging.error(f"Invalid status {status} for PID {pid}")
        except ValueError as e:
            logging.error(f"Invalid timestamp {timestamp} for PID {pid}: {str(e)}")

    def generate_report(self) -> None:
        """Generate a report with job durations and alerts."""
        for pid, job in self.jobs.items():
            if job['start'] is None or job['end'] is None:
                logging.error(f"Incomplete job data for PID {pid}")
                continue

            duration = (job['end'] - job['start']).total_seconds()
            message = (
                f"Job {pid} ({job['description']}): "
                f"Duration {duration:.0f} seconds"
            )

            if duration > self.error_threshold:
                logging.error(f"{message} - ERROR: Exceeded 10 minutes")
            elif duration > self.warning_threshold:
                logging.warning(f"{message} - WARNING: Exceeded 5 minutes")
            else:
                logging.info(message)

def main():
    """Main function to run the log monitor."""
    monitor = LogMonitor('logs.log')
    monitor.process_log()
    monitor.generate_report()

if __name__ == '__main__':
    main()