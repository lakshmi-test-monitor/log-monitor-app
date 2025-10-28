import unittest
import os
import sys
from io import StringIO

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.log_monitor import monitor_logs


class TestLogMonitor(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test_temp.log'
        self.output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = self.original_stdout
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def run_monitor(self, lines):
        with open(self.log_file, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        monitor_logs(self.log_file)

    def test_normal_job(self):
        self.run_monitor([
            '00:00:00,Backup,START,1001',
            '00:04:00,Backup,END,1001'
        ])
        output = self.output.getvalue()
        self.assertNotIn('WARNING', output)
        self.assertNotIn('ERROR', output)

    def test_warning_threshold(self):
        self.run_monitor([
            '00:00:00,Report,START,1002',
            '00:06:00,Report,END,1002'
        ])
        output = self.output.getvalue()
        self.assertIn('WARNING', output)
        self.assertIn('6.00 minutes', output)

    def test_error_threshold(self):
        self.run_monitor([
            '00:00:00,Sync,START,1003',
            '00:11:00,Sync,END,1003'
        ])
        output = self.output.getvalue()
        self.assertIn('ERROR', output)
        self.assertIn('11.00 minutes', output)

    def test_unfinished_job(self):
        self.run_monitor([
            '00:00:00,Unfinished,START,9999'
        ])
        output = self.output.getvalue()
        self.assertIn('has no END', output)

    def test_invalid_timestamp(self):
        self.run_monitor([
            '25:00:00,Bad,START,9999'
        ])
        output = self.output.getvalue()
        self.assertIn('Invalid timestamp', output)
        self.assertIn('Hour must be 0-23', output)

    def test_invalid_row(self):
        self.run_monitor([
            '00:00:00,Only,Three'  # Missing PID
        ])
        output = self.output.getvalue()
        self.assertIn('Invalid row', output)