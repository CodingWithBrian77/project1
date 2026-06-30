import sqlite3


# Configuration Constants
LOG_FILE = "mock_logs.txt"
DB_FILE = "log_vault.db"


def process_and_analyze_logs(log_file_path: str, db_file_path: str) -> None:
    """
    Streams logs into a SQLite database and prints hourly analytics.
    
    Args:
        log_file_path: Path to the log file to process
        db_file_path: Path to the SQLite database file
    """

    try:
        # 1. Initialize Database Connection and Schema
        database_file = sqlite3.connect(db_file_path)
        cursor = database_file.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS log_vault (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_timestamp TEXT,
                log_status TEXT,
                log_message TEXT
            )
        """
        )

        # 2. Parse and Insert Log Streams Safely
        try:
            with open(log_file_path, "r") as data_file:
                for line_number, line in enumerate(data_file, start=1):
                    if "ERROR" in line or "WARNING" in line:
                        clean_line = line.strip()
                        
                        # Validate log format before inserting
                        parts = clean_line.split(" - ", 2)
                        if len(parts) == 3:
                            cursor.execute(
                                "INSERT INTO log_vault(log_timestamp, log_status, log_message) VALUES (?, ?, ?)",
                                parts,
                            )
                        else:
                            print(f"Warning: Skipping malformed log at line {line_number}: {clean_line}")

        except FileNotFoundError:
            print(f"Error: Log file '{log_file_path}' not found.")
            database_file.close()
            return
        except IOError as e:
            print(f"Error reading log file: {e}")
            database_file.close()
            return

        # Commit insertions before querying
        database_file.commit()

        # 3. Aggregate Metrics Using SQL Analytics
        cursor.execute(
            """
            SELECT 
                SUBSTR(log_timestamp, 12, 2) AS hour_of_day,
                log_status,
                COUNT(*) AS total_incidents
            FROM log_vault
            GROUP BY hour_of_day, log_status
            ORDER BY hour_of_day ASC;
        """
        )

        results = cursor.fetchall()

        # 4. Format and Display Reports
        if results:
            print(f"{'Hour':<8} | {'Status':<10} | {'Total Incidents'}")
            print("-" * 35)

            for row in results:
                raw_hour = int(row[0])  # Convert string hours (e.g., '08') to integers

                # Map 24-hour integers to AM/PM human-readable formats
                display_hour = _convert_to_12hour_format(raw_hour)

                print(f"{display_hour:<8} | {row[1]:<10} | {row[2]}")
        else:
            print("No ERROR or WARNING logs found to analyze.")

        # Clean up connections
        database_file.close()

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def _convert_to_12hour_format(hour: int) -> str:
    """
    Convert 24-hour format to 12-hour AM/PM format.
    
    Args:
        hour: Hour in 24-hour format (0-23)
        
    Returns:
        Formatted hour string (e.g., '12 AM', '3 PM')
    """
    if hour == 0:
        return "12 AM"
    elif hour == 12:
        return "12 PM"
    elif hour > 12:
        return f"{hour - 12} PM"
    else:
        return f"{hour} AM"


if __name__ == "__main__":
    # Execute the log processing pipeline
    process_and_analyze_logs(LOG_FILE, DB_FILE)
