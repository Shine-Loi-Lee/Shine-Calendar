from datetime import datetime, timezone, timedelta
import os

KST=timezone(timedelta(hours=9))

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def convert_to_new_calendar():
    BASE_DATE = datetime(2001, 5, 14, tzinfo=KST)
    DAYS_PER_YEAR = 364
    DAYS_PER_MONTH = 28
    LEAP_CYCLE = 28
    LEAP_EXTRA_DAYS = 7

    today = datetime.now(KST)
    delta_days = (today - BASE_DATE).days

    leap_days = (today.year - 2001) // LEAP_CYCLE * LEAP_EXTRA_DAYS
    delta_days -= leap_days

    new_year = 1 + (delta_days // DAYS_PER_YEAR)
    remaining_days = delta_days % DAYS_PER_YEAR

    new_month = 1 + (remaining_days // DAYS_PER_MONTH)
    new_day = 1 + (remaining_days % DAYS_PER_MONTH)

    weekday = WEEKDAYS[delta_days % 7]

    return f"{weekday}, {new_year} - {new_month} - {new_day}"

new_date = convert_to_new_calendar()

with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# Shine Calendar\n\nToday is **{new_date}**.\n\n")

# print("README.md updated with new calendar date.")
