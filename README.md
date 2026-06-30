## Log Parsing Audit System

A Python utility for parsing and analyzing log files with a focus on error and warning events. This script streams logs into a SQLite database and provides hourly analytics reports.

### Features

- **Efficient Log Processing**: Streams log files line-by-line for memory efficiency
- **SQLite Database Storage**: Stores parsed logs in a local SQLite database (`log_vault.db`)
- **Log Filtering**: Automatically filters and processes ERROR and WARNING level logs
- **Hourly Analytics**: Aggregates incidents by hour of day and log status
- **Human-Readable Format**: Converts 24-hour timestamps to 12-hour AM/PM format for easy reading
- **Error Handling**: Robust validation and error handling for malformed log entries

### How It Works

1. **Database Initialization**: Creates a SQLite table to store log entries
2. **Log Parsing**: Reads the log file and validates each entry format
3. **Data Insertion**: Stores formatted logs in the database with timestamp, status, and message
4. **Analytics**: Runs SQL queries to aggregate metrics by hour and status
5. **Reporting**: Displays a formatted table with incident counts per hour

### Usage

```bash
python main.py
```

The script processes logs from `mock_logs.txt` and outputs a table showing the number of ERROR and WARNING incidents by hour.

### Configuration

Edit the constants in `main.py` to customize:
- `LOG_FILE`: Path to the log file to process (default: `mock_logs.txt`)
- `DB_FILE`: Path to the SQLite database file (default: `log_vault.db`)

### Log Format

Expected log format (space-separated):
```
YYYY-MM-DD HH:MM:SS - STATUS - MESSAGE
```

Example:
```
2024-06-26 14:30:45 - ERROR - Database connection failed
2024-06-26 15:45:12 - WARNING - High memory usage detected
```
