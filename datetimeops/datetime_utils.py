import calendar
import datetime
import time
from typing import Literal, Union

import pytz
from dateutil.relativedelta import relativedelta


def now_utc(fmt="%Y-%m-%d %H:%M:%S"):
    """Returns the current UTC time in the given format."""
    return datetime.datetime.now(datetime.timezone.utc).strftime(fmt)


def now_tz(tz='UTC', fmt="%Y-%m-%d %H:%M:%S"):
    """Returns the current time in the specified timezone."""
    return datetime.datetime.now(pytz.timezone(tz)).strftime(fmt)


def epoch(date_str=None) -> int:
    """Returns the Unix timestamp for a given date or the current timestamp if None."""
    if date_str is None:
        return int(time.time())
    try:
        # Attempt to parse with time component
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Fallback to date-only, with time set to 00:00:00
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    # Return the Unix timestamp as an integer
    return int(dt.timestamp())


def validate_date(d, fmt="%Y-%m-%d %H:%M:%S", chk_future_date=False) -> bool:
    """Validates if a given string is a valid date in the specified format."""
    try:
        dt = datetime.datetime.strptime(d, fmt)
        return dt.strftime('%Y-%m-%d') >= now_utc('%Y-%m-%d') if chk_future_date else True
    except ValueError:
        return False


def change_date_format(input_date: Union[str, datetime.datetime, datetime.date], to_fmt, from_fmt="%Y-%m-%d %H:%M:%S"):
    """Changes the format of a given date string or datetime object."""
    if isinstance(input_date, (datetime.datetime, datetime.date)):
        return input_date.strftime(to_fmt)
    if isinstance(input_date, str):
        try:
            return datetime.datetime.strptime(input_date, from_fmt).strftime(to_fmt)
        except ValueError:
            return None  # Return None instead of failing silently


def sleep_counter(sleep_seconds):
    while sleep_seconds > 0:
        time.sleep(1)
        sleep_seconds -= 1
        # Without spaces, when it goes from 10 to 9, trailing 0 stays so look like 90,80,70 ...
        print(f"\rWait: {sleep_seconds}      ", end='')
    print()


def add_days_to_now_utc(days, fmt="%Y-%m-%d %H:%M:%S"):
    """Adds days to the current UTC date and returns it in the given format."""
    new_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=days)
    return new_date.strftime(fmt)


def add_days_to_date(date, days_to_add: int, to_fmt=None, from_fmt="%Y-%m-%d %H:%M:%S"):
    """Adds days to a given date."""
    return offset_date(date, offset_type='days', offset_amount=days_to_add, to_fmt=to_fmt, from_fmt=from_fmt)


def add_months_to_date(date, months_to_add: int, to_fmt=None, from_fmt="%Y-%m-%d %H:%M:%S"):
    """Adds months to a given date."""
    return offset_date(date, offset_type='months', offset_amount=months_to_add, to_fmt=to_fmt, from_fmt=from_fmt)


def delta_between_dates(start_date, end_date):
    """Calculates the difference between two dates in terms of years, months, days."""
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    return relativedelta(end_date, start_date)


def months_between_dates(start_date, end_date):
    """Returns the number of months between two dates."""
    delta = delta_between_dates(start_date, end_date)
    return delta.years * 12 + delta.months


def days_between_dates(start_date, end_date, fmt="%Y-%m-%d"):
    """Returns the number of days between two dates."""
    # Convert string dates to datetime objects if necessary
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
    Returns a date offset by the specified amount of time (based on offset_type and offset_amount)

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
    offset = relativedelta(**{offset_type: offset_amount})
    new_date = date + offset
    return new_date.strftime(to_fmt)


def get_first_last_date_of_month(date: str = now_utc(fmt="%Y-%m-%d"),
                                 from_fmt: str = "%Y-%m-%d", output_fmt: str = "%Y-%m-%d"):
    """
    Returns the first and last day of the month for a given date.
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
    """Converts hh:mm:ss or mm:ss format to total seconds."""
    # If the input is a timedelta, we can directly return the total seconds
    if isinstance(hhmmss, datetime.timedelta):
        return int(hhmmss.total_seconds())

    # Replace any periods with colons (to handle decimal separator)
    hhmmss = hhmmss.replace('.', ':')

    parts = list(map(int, hhmmss.split(':')))
    return sum(x * 60 ** i for i, x in enumerate(reversed(parts)))


def seconds_to_hhmmss(seconds):
    """Converts total seconds to hh:mm:ss format."""
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"


def hhmmss_check(hhmmss):
    """Validates and converts time in hh:mm:ss format."""
    seconds = hhmmss_to_seconds(hhmmss)
    return seconds_to_hhmmss(seconds)
