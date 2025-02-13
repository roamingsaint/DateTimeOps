# Source (1): How to validate datetime formats
#   https://stackoverflow.com/questions/18539266/how-to-validate-a-specific-date-and-time-format-using-python
import calendar
import datetime
import time
from typing import Literal, Union

import pytz
from dateutil.relativedelta import relativedelta
import re

utc_time = datetime.datetime.now(datetime.timezone.utc)


# Source (1):
def validate_date(d, fmt="%Y-%m-%d %H:%M:%S", chk_future_date=False):
    try:
        dt = datetime.datetime.strptime(d, fmt)
        if chk_future_date:
            if dt.strftime('%Y-%m-%d') >= now_utc('%Y-%m-%d'):
                return True
            else:
                return False
        return True
    except ValueError:
        return False


def change_date_format(input_date: Union[str, datetime.datetime, datetime.date], to_fmt, from_fmt="%Y-%m-%d %H:%M:%S"):
    if isinstance(input_date, datetime.datetime) or isinstance(input_date, datetime.date):
        return input_date.strftime(to_fmt)
    if isinstance(input_date, str):
        if validate_date(input_date, from_fmt) is True:
            return datetime.datetime.strptime(input_date, from_fmt).strftime(to_fmt)
        # Check the common date formats
        elif validate_date(input_date, "%Y-%m-%d") is True:
            return datetime.datetime.strptime(input_date, "%Y-%m-%d").strftime(to_fmt)
        elif validate_date(input_date, "%Y-%m-%d %H:%M:%S") is True:
            return datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S").strftime(to_fmt)


def sleep_counter(sleep_seconds):
    while sleep_seconds > 0:
        time.sleep(1)
        sleep_seconds -= 1
        # Without spaces, when it goes from 10 to 9, trailing 0 stays so look like 90,80,70 ...
        print(f"\rWait: {sleep_seconds}      ", end='')
    print()


def now_utc(fmt="%Y-%m-%d %H:%M:%S"):
    return utc_time.strftime(fmt)


def now_tz(tz='UTC', fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now(pytz.timezone(tz)).strftime(fmt)


def epoch(date_str=None):
    if date_str is None:
        return str(int(time.time()))
    else:
        try:
            # Attempt to parse with time component
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Fallback to date-only, with time set to 00:00:00
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        # Return the Unix timestamp as an integer
        return int(dt.timestamp())


def add_days_to_now_utc(days, fmt="%Y-%m-%d %H:%M:%S"):
    new_date = utc_time + datetime.timedelta(days=days)
    return new_date.strftime(fmt)


def add_days_to_date(date, days_to_add: int, to_fmt=None, from_fmt="%Y-%m-%d %H:%M:%S"):
    return offset_date(date, offset_type='days', offset_amount=days_to_add, to_fmt=to_fmt, from_fmt=from_fmt)


def add_months_to_date(date, months_to_add: int, to_fmt=None, from_fmt="%Y-%m-%d %H:%M:%S"):
    return offset_date(date, offset_type='months', offset_amount=months_to_add, to_fmt=to_fmt, from_fmt=from_fmt)


def delta_between_dates(start_date, end_date):
    assert validate_date(start_date, fmt="%Y-%m-%d") and validate_date(start_date, fmt="%Y-%m-%d"), \
        f"Invalid dates from: {start_date} to: {end_date}"

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    delta = relativedelta(end_date, start_date)
    return delta


def months_between_dates(start_date, end_date):
    delta = delta_between_dates(start_date, end_date)
    months = delta.years * 12 + delta.months
    return months


def days_between_dates(start_date, end_date, fmt="%Y-%m-%d"):
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, fmt)
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, fmt)

    # Calculate the difference between the two dates
    time_difference = end_date - start_date
    return time_difference.days


def time_passed(start, end):
    """
    The time_passed function takes two datetime objects or strings and returns a dictionary with the following keys:

        days: The number of days between the start and end dates.
        hours: The number of hours between the start and end dates.
        minutes: The number of minutes between the start and end dates.
        seconds (Use total_seconds instead): Always be less than 60, even if time_difference > 24 hours
            (i.e., it is not cumulative).
        total_seconds: The number of seconds between the start and end dates.
        human_readable: The complete time passed in human_readable format (D days H hours M minutes SS seconds)

    :param start: start date/time
    :param end: end date/time
    :return: A dictionary
    """
    # Convert string dates to datetime objects if necessary
    if isinstance(start, str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    if isinstance(end, str):
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    # Convert epoch dates to datetime objects if necessary
    if isinstance(start, int):
        start = datetime.datetime.fromtimestamp(start)
    if isinstance(end, int):
        end = datetime.datetime.fromtimestamp(end)

    # Calculate time difference
    time_difference = end - start

    # Extract time components
    days = time_difference.days,
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Calculate total seconds
    total_seconds = time_difference.total_seconds()
    human_readable = ((f"{days[0]} days " if days[0] > 0 else "") +
                      (f"{hours} hours " if hours > 0 else "") +
                      (f"{minutes} minutes " if minutes > 0 else "") +
                      f"{seconds} seconds")
    human_shorthand = ((f"{days[0]} days " if days[0] > 0 else "") +
                       (f"{hours} hr " if hours > 0 else "") +
                       (f"{minutes} min " if minutes > 0 else "") +
                       f"{seconds} sec")

    return {'days': days[0], 'hours': hours, 'minutes': minutes,
            'total_seconds': total_seconds,
            'human_readable': human_readable, 'human_shorthand': human_shorthand}


def offset_date(date, offset_type: Literal['years', 'months', 'days', 'weeks', 'hours', 'minutes', 'seconds', 'micros'],
                offset_amount: int, to_fmt=None, from_fmt="%Y-%m-%d %H:%M:%S"):
    """
    Returns a date offset based on offset_type and offset_amount

    :param date: date to apply offset to
    :param offset_type: offset by (years/ months/ days/ weeks/ hours/ minutes/ seconds/ micros)
    :param offset_amount: -ve integer to go back in time, +ve to go forward
    :param from_fmt: input date format
    :param to_fmt: output date format (if None, defaults to from_fmt
    :return: date with offset applied
    """
    if to_fmt is None:
        to_fmt = from_fmt

    date = datetime.datetime.strptime(str(date), from_fmt)

    if offset_type == 'years':
        offset = relativedelta(years=offset_amount)
    elif offset_type == 'months':
        offset = relativedelta(months=offset_amount)
    elif offset_type == 'days':
        offset = relativedelta(days=offset_amount)
    elif offset_type == 'weeks':
        offset = relativedelta(weeks=offset_amount)
    elif offset_type == 'hours':
        offset = relativedelta(hours=offset_amount)
    elif offset_type == 'minutes':
        offset = relativedelta(minutes=offset_amount)
    elif offset_type == 'seconds':
        offset = relativedelta(seconds=offset_amount)
    elif offset_type == 'micros':
        offset = relativedelta(microseconds=offset_amount)
    else:
        raise AssertionError(f'Invalid offset_type: {offset_type}')
    new_date = date + offset

    return new_date.strftime(to_fmt)


def get_first_last_date_of_month(date: str = now_utc(fmt="%Y-%m-%d"),
                                 from_fmt: str = "%Y-%m-%d", output_fmt: str = "%Y-%m-%d"):
    """
    Returns first and last day of month (handles leap years)

    Example:
      get_first_last_date_of_month(date='02/14/2020', from_fmt='%m/%d/%Y', output_fmt='%Y-%m-%d')
      -> ('2021-05-01', '2021-05-31')

    :param date: any date
    :param from_fmt: format of the date parameter
    :param output_fmt: format you want your first and last date in
    :return: (first_date_of_month, last_date_of_month)
    """
    date = datetime.datetime.strptime(str(date), from_fmt)
    first_date_of_month = date.replace(day=1).strftime(output_fmt)
    days_in_month = calendar.monthrange(date.year, date.month)[-1]
    last_date_of_month = date.replace(day=days_in_month).strftime(output_fmt)
    return first_date_of_month, last_date_of_month


def hhmmss_to_seconds(hhmmss):
    """Convert hh:mm:ss or mm:ss time format to total seconds."""

    # If the input is a timedelta, we can directly return the total seconds
    if isinstance(hhmmss, datetime.timedelta):
        return int(hhmmss.total_seconds())

    # Replace any periods with colons (to handle decimal separator)
    hhmmss = hhmmss.replace('.', ':')

    # Count the number of colons to determine the format
    no_of_colons = len(re.findall(':', hhmmss))

    if no_of_colons == 2:  # Format: hh:mm:ss
        h, m, s = hhmmss.split(':')
    elif no_of_colons == 1:  # Format: mm:ss (Assume h = 0)
        h = 0
        m, s = hhmmss.split(':')
    else:
        raise Exception(f"{hhmmss} is not in the correct format")

    # Convert hours, minutes, and seconds to total seconds
    return int(h) * 3600 + int(m) * 60 + int(s)


def seconds_to_hhmmss(seconds):
    """Get hh:mm:ss from time."""
    seconds = float(seconds)
    hh = int(seconds / 3600)
    mm = int((seconds % 3600) / 60)
    ss = int((seconds % 3600) % 60)
    return f"{hh:02}:{mm:02}:{ss:02}"


def hhmmss_check(hhmmss):
    seconds = hhmmss_to_seconds(hhmmss)
    return seconds_to_hhmmss(seconds)


if __name__ == '__main__':
    print(add_days_to_now_utc(10))
    print(seconds_to_hhmmss(4041.177667))
    print(add_months_to_date('2020-12-02 12:13:12', -1))
    print(add_months_to_date('202012', 1, from_fmt='%Y%m'))
    print(change_date_format('2020-10-25 00:00:02', to_fmt="%d %b"))
    print(change_date_format('2020-10-25', to_fmt="%Y-%m-%d %H:%M:%S", from_fmt="%Y-%m-%d"))
    print(get_first_last_date_of_month(date='2021.04.01', from_fmt='%Y.%m.%d', output_fmt='%m/%d/%Y'))
    print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3\1',
                 get_first_last_date_of_month(date='2021-04-01', output_fmt='%m/%d/%Y')[0]))