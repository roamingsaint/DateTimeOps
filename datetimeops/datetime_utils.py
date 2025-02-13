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
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
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
    start_date = datetime.datetime.strptime(start_date, fmt)
    end_date = datetime.datetime.strptime(end_date, fmt)
    return (end_date - start_date).days


def time_passed(start, end):
    """
    Returns the time difference between two datetime objects or strings.

    :return: Dictionary with days, hours, minutes, total seconds, and human-readable formats.
    """
    if isinstance(start, str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    if isinstance(end, str):
        end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    if isinstance(start, int):
        start = datetime.datetime.fromtimestamp(start)
    if isinstance(end, int):
        end = datetime.datetime.fromtimestamp(end)

    time_difference = end - start
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_seconds = time_difference.total_seconds()

    human_readable = (f"{days} days " if days > 0 else "") + \
                     (f"{hours} hours " if hours > 0 else "") + \
                     (f"{minutes} minutes " if minutes > 0 else "") + \
                     f"{seconds} seconds"

    human_shorthand = (f"{days} days " if days > 0 else "") + \
                      (f"{hours} hr " if hours > 0 else "") + \
                      (f"{minutes} min " if minutes > 0 else "") + \
                      f"{seconds} sec"

    return {'days': days, 'hours': hours, 'minutes': minutes,
            'total_seconds': total_seconds,
            'human_readable': human_readable, 'human_shorthand': human_shorthand}


def offset_date(date, offset_type: Literal['years', 'months', 'days', 'weeks', 'hours', 'minutes', 'seconds', 'micros'],
                offset_amount: int, to_fmt=None, from_fmt="%Y-%m-%d %H:%M:%S"):
    """Returns a date offset by the specified amount of time."""
    if to_fmt is None:
        to_fmt = from_fmt
    date = datetime.datetime.strptime(str(date), from_fmt)
    offset = relativedelta(**{offset_type: offset_amount})
    new_date = date + offset
    return new_date.strftime(to_fmt)


def get_first_last_date_of_month(date: str = now_utc(fmt="%Y-%m-%d"),
                                 from_fmt: str = "%Y-%m-%d", output_fmt: str = "%Y-%m-%d"):
    """Returns the first and last day of the month for a given date."""
    date = datetime.datetime.strptime(str(date), from_fmt)
    first_date_of_month = date.replace(day=1).strftime(output_fmt)
    days_in_month = calendar.monthrange(date.year, date.month)[-1]
    last_date_of_month = date.replace(day=days_in_month).strftime(output_fmt)
    return first_date_of_month, last_date_of_month


def hhmmss_to_seconds(hhmmss):
    """Converts hh:mm:ss or mm:ss format to total seconds."""
    if isinstance(hhmmss, datetime.timedelta):
        return int(hhmmss.total_seconds())
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
