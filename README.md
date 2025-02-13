# DateTimeOps

## Overview
**DateTimeOps** is a lightweight Python package providing convenient utilities for working with dates, times, and timestamps. It simplifies common datetime operations such as formatting, validation, conversion, offsets, and differences.

## Features
- Get current UTC or timezone-specific datetime.
- Convert between different datetime formats.
- Validate dates and check if they are in the future.
- Perform date arithmetic (add/subtract days, months, offsets).
- Calculate time differences in days, months, or timestamps.
- Convert time formats (e.g., HH:MM:SS to seconds and vice versa).
- Get first and last date of a given month.

## Installation
You can install the package using pip:
```sh
pip install datetimeops
```

## Usage
Import the package and use its functions:

```python
from datetimeops.datetime_utils import now_utc, add_days_to_date, validate_date, change_date_format

# Get current UTC time
print(now_utc())  # '2025-02-13 14:30:00'

# Validate a date
print(validate_date("2025-05-01"))  # True
print(validate_date("Invalid Date"))  # False

# Change date format
print(change_date_format("2025-02-13 14:30:00", "%d-%m-%Y"))  # '13-02-2025'

# Add 10 days to a date
print(add_days_to_date("2025-02-13", 10))  # '2025-02-23 00:00:00'
```

## Functions
### Date & Time Retrieval
- `now_utc(fmt="%Y-%m-%d %H:%M:%S")` → Returns the current UTC time.
- `now_tz(tz, fmt="%Y-%m-%d %H:%M:%S")` → Returns the current time in the specified timezone.

### Date Validation & Formatting
- `validate_date(d, fmt=None, chk_future_date=False)` → Checks if a date is valid and optionally if it is in the future.
- `change_date_format(input_date, to_fmt, from_fmt="%Y-%m-%d %H:%M:%S")` → Converts date format.

### Epoch & Time Difference Calculations
- `epoch(date_str=None)` → Returns Unix timestamp for a date or current time.
- `days_between_dates(start_date, end_date, fmt="%Y-%m-%d")` → Returns the number of days between two dates.
- `months_between_dates(start_date, end_date)` → Returns the number of months between two dates.
- `time_passed(start, end)` → Returns time difference in human-readable format.

### Date Arithmetic
- `add_days_to_date(date, days_to_add, to_fmt=None, from_fmt=None)` → Adds days to a date.
- `add_months_to_date(date, months_to_add, to_fmt=None, from_fmt=None)` → Adds months to a date.
- `offset_date(date, offset_type, offset_amount, to_fmt=None, from_fmt=None)` → Applies an offset of years, months, days, etc.

### Time Format Conversion
- `hhmmss_to_seconds(hhmmss)` → Converts HH:MM:SS to total seconds.
- `seconds_to_hhmmss(seconds)` → Converts seconds to HH:MM:SS format.

### Miscellaneous
- `get_first_last_date_of_month(date, from_fmt, output_fmt)` → Returns first and last date of a given month.
- `sleep_counter(seconds)` → Displays a countdown timer.

## Running Tests
To verify functionality, run the test suite using `pytest`:
```sh
pytest tests/
```

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Author
Created by **Kand Rishiraj**.

## Support
If you like this project, consider supporting it:
- [Buy Me a Coffee](https://buymeacoffee.com/RoamingSaint)
- [Ko-fi](https://ko-fi.com/RoamingSaint)

