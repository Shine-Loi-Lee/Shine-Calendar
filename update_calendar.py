from datetime import datetime, timezone, timedelta
import os

# Set Korean Standard Time (UTC+9)
KST=timezone(timedelta(hours=9))

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def convert_to_new_calendar():
    # Base date: May 14, 2001 (corresponds to year 1, month 1, day 1)
    BASE_DATE = datetime(2001, 5, 14, tzinfo=KST)
    DAYS_PER_YEAR = 364 # 13 months * 28 days = 364 days
    DAYS_PER_MONTH = 28

    # Leap year cycles:
    LEAP_CYCLE_7 = 7 # Every 7 years, the 13th month extends to 35 days
    LEAP_CYCLE_28 = 28 # Every 28 years, the 12th and 13th month extends to 35 days

    # Get the current date in Korean Standard Time
    today = datetime.now(KST)

    # Calculate the number of days passed since the base date
    delta_days = (today - BASE_DATE).days

    total_leap_days = 0

    # Every 7 years, the 13th month has 35 days
    total_leap_days += ((today.year - 2001) // LEAP_CYCLE_7) * 7

    # Every 28 years, both the 12th and 13th months have 35 days (adding another 7 days)
    total_leap_days += ((today.year - 2001) // LEAP_CYCLE_28) * 7

    delta_days += total_leap_days

    new_year = 1 + (delta_days // DAYS_PER_YEAR)
    remaining_days = delta_days % DAYS_PER_YEAR

    month_lengths = [DAYS_PER_MONTH] * 13

    # Every 7 years, the 13th month extends to 35 days
    if (new_year - 1) % LEAP_CYCLE_7 == 0:
        month_lengths[12] = 35

    # Every 28 years, both the 12th and 13th months extend to 35 days
    if (new_year - 1) % LEAP_CYCLE_28 == 0:
        month_lengths[11] = 35
        month_lengths[12] = 35

    # Determine the current month and day
    new_month = 1
    while remaining_days >= month_lengths[new_month - 1]:
        remaining_days -= month_lengths[new_month - 1]
        new_month += 1

    # Adjust to start from day 1
    new_day = remaining_days + 1

    weekday = WEEKDAYS[delta_days % 7]

    return f"{weekday}, {new_year} - {new_month} - {new_day}"

# Generate the new date
new_date = convert_to_new_calendar()

# Read the existing README.md file
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
else:
    lines = []

# Remove the old date and update
lines=lines[3:]

updated_content = ["# Shine Calendar\n\nToday is **[" + new_date + "]**\n"] + lines

# Save the updated README.md
with open(readme_path, "w", encoding="utf-8") as f:
    f.writelines(updated_content)
