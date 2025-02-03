from datetime import datetime, timezone, timedelta

# Set Korean Standard Time (UTC+9)
KST = timezone(timedelta(hours=9))

# Define weekdays (starting from Monday)
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Base date: May 14, 2001 (Shine Calendar: Year 1, Month 1, Day 1)
BASE_DATE = datetime(2001, 5, 14, tzinfo=KST)

DAYS_PER_YEAR = 364  # 13 months * 28 days = 364 days
DAYS_PER_MONTH = 28

# Leap year cycles:
LEAP_CYCLE_7 = 7  # Every 7 years, the 13th month extends to 35 days
LEAP_CYCLE_28 = 28  # Every 28 years, the 12th and 13th months extend to 35 days


def convert_to_new_calendar(input_date):
    """
    Converts a given Gregorian date (YYYY MM DD) to the Shine Calendar format.
    """
    # Convert user input to datetime object
    try:
        today = datetime.strptime(input_date, "%Y %m %d").replace(tzinfo=KST)
    except ValueError:
        return "Invalid date format. Please enter the date as YYYY MM DD."

    # Calculate the number of days passed since the base date
    delta_days = (today - BASE_DATE).days

    # Calculate total leap days
    leap_days = ((today.year - 2001) // LEAP_CYCLE_7) * 7
    leap_days += ((today.year - 2001) // LEAP_CYCLE_28) * 7
    delta_days -= leap_days  # Subtract leap days since they were added before

    # Calculate the new Shine year
    new_year = 1 + (delta_days // DAYS_PER_YEAR)
    remaining_days = delta_days % DAYS_PER_YEAR

    # Month lengths (default 28 days each)
    month_lengths = [DAYS_PER_MONTH] * 13

    # Adjust leap months
    if (new_year - 1) % LEAP_CYCLE_7 == 0:
        month_lengths[12] = 35  # 13th month extends

    if (new_year - 1) % LEAP_CYCLE_28 == 0:
        month_lengths[11] = 35  # 12th month extends
        month_lengths[12] = 35  # 13th month extends

    # Determine the month and day
    new_month = 1
    while remaining_days >= month_lengths[new_month - 1]:
        remaining_days -= month_lengths[new_month - 1]
        new_month += 1

    # Adjust to start from day 1
    new_day = remaining_days + 1

    weekday = WEEKDAYS[delta_days % 7]

    return f"{weekday}, {new_year} - {new_month} - {new_day}"


def convert_to_gregorian(y, m, d):
    """
    Converts Shine Calendar date (y, m, d) to a Gregorian date (YYYY-MM-DD).
    """
    # Calculate total days from Shine Calendar year, month, and day
    total_days = (y - 1) * DAYS_PER_YEAR

    # Adjust for leap years before this year
    leap_days = ((y - 1) // LEAP_CYCLE_7) * 7
    leap_days += ((y - 1) // LEAP_CYCLE_28) * 7
    total_days += leap_days  # Add leap days

    # Month lengths (default 28 days each)
    month_lengths = [DAYS_PER_MONTH] * 13

    # Adjust leap months
    if (y - 1) % LEAP_CYCLE_7 == 0:
        month_lengths[12] = 35  # 13th month extends

    if (y - 1) % LEAP_CYCLE_28 == 0:
        month_lengths[11] = 35  # 12th month extends
        month_lengths[12] = 35  # 13th month extends

    # Add months and days
    for i in range(m - 1):
        total_days += month_lengths[i]
    total_days += (d - 1)

    # Convert to Gregorian date
    gregorian_date = BASE_DATE + timedelta(days=total_days)

    # Get weekday
    weekday = WEEKDAYS[total_days % 7]

    return f"{weekday}, {gregorian_date.strftime('%Y - %m - %d')}"


# Get user input for conversion direction
mode = input("Choose mode (1: Gregorian → Shine, 2: Shine → Gregorian): ")

if mode == "1":
    user_date = input("Enter Gregorian date (YYYY MM DD): ")
    result = convert_to_new_calendar(user_date)
    print(f"Shine Calendar Date: {result}")

elif mode == "2":
    user_input = input("Enter Shine Calendar date (YYYY MM DD): ")
    try:
        sh_year, sh_month, sh_day = map(int, user_input.split(" "))
        gregorian_date = convert_to_gregorian(sh_year, sh_month, sh_day)
        print(f"Gregorian Date: {gregorian_date}")
    except ValueError:
        print("Invalid format. Please enter in YYYY MM DD format.")

else:
    print("Invalid mode selected.")
