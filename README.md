
# Log Monitoring Application
A log monitoring tool that parses job logs, tracks execution time, and generates time alerts for performance issues.

## Features Delivered
  Parse CSV log file  (with csv.reader) 
  Track START/END per PID (dictionary-based state) 
  Calculate duration  (HH:MM:SS → seconds → minutes) 
  Warning > 5 min 
  Error > 10 min 
  Clean, readable code 
  Clear commit history 
  Unit tests  (6 test cases, 100% pass) 

  ## Project Structure
  log-monitoring-app 
   logs.log  # Sample input
   src /log_monitor.py  # Main logic
   tests/test_log_monitor.py  # Unit tests

  ## KEY POINTS
  Robust timestamp parsing with full validation (0-23, 0-59)
  Graceful error handling (invalid rows, timestamps, missing END)
  No external dependencies – pure Python
  Test-driven validation using temporary log files and stdout capture
## Tests cover:
Normal job
Warning threshold
Error threshold
Unfinished job
Invalid timestamp
Malformed row
## What I Would Add (if more time)
Configurable thresholds (--warn 5 --error 10) (flixibility)
Output to JSON report (Better observability)
Support for dates (YYYY-MM-DD HH:MM:SS) (real world logs)
Multi-threading for large logs (Performance)

