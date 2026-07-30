from datetime import datetime
from zoneinfo import ZoneInfo


BD_TZ = ZoneInfo("Asia/Dhaka")


def get_bd_time():
    return datetime.now(BD_TZ).strftime("%Y-%m-%d %H:%M:%S")


def format_bd_time(value):
    if not value:
        return ""

    try:
        dt = datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        )

        dt = dt.replace(tzinfo=BD_TZ)

        return dt.strftime(
            "%d %B %Y, %I:%M:%S %p"
        )

    except Exception:
        return str(value)