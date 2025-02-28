"""
Simulate the get_meetings and free slot API
"""

from datetime import datetime, timedelta

# meetings sample data
appointments_dict = {
    "appointments": [
        {
            "date": "2025-02-01",
            "start_time": "9:00",
            "end_time": "10:00",
            "participants": ["John Doe"],
            "notes": "Training Session",
        },
        {
            "date": "2025-02-03",
            "start_time": "11:00",
            "end_time": "13:00",
            "participants": ["Alice Brown"],
            "notes": "One-on-One",
        },
        {
            "date": "2025-02-03",
            "start_time": "11:00",
            "end_time": "13:00",
            "participants": ["Michael Wilson", "Robert Johnson"],
            "notes": "Planning Session",
        },
        {
            "date": "2025-02-06",
            "start_time": "17:00",
            "end_time": "18:00",
            "participants": ["Robert Johnson", "John Doe"],
            "notes": "One-on-One",
        },
        {
            "date": "2025-02-07",
            "start_time": "16:00",
            "end_time": "18:00",
            "participants": ["Emily Davis"],
            "notes": "Client Call",
        },
        {
            "date": "2025-02-13",
            "start_time": "15:00",
            "end_time": "18:00",
            "participants": ["John Doe", "Robert Johnson", "Alice Brown"],
            "notes": "Client Call",
        },
        {
            "date": "2025-02-14",
            "start_time": "17:00",
            "end_time": "18:00",
            "participants": ["Michael Wilson", "Jane Smith"],
            "notes": "Team Meeting",
        },
        {
            "date": "2025-02-15",
            "start_time": "16:00",
            "end_time": "18:00",
            "participants": ["Emily Davis"],
            "notes": "One-on-One",
        },
        {
            "date": "2025-02-15",
            "start_time": "8:00",
            "end_time": "10:00",
            "participants": ["Michael Wilson"],
            "notes": "Planning Session",
        },
        {
            "date": "2025-02-16",
            "start_time": "9:00",
            "end_time": "12:00",
            "participants": ["John Doe"],
            "notes": "Client Call",
        },
        {
            "date": "2025-02-19",
            "start_time": "9:00",
            "end_time": "10:00",
            "participants": ["Robert Johnson", "Alice Brown"],
            "notes": "One-on-One",
        },
        {
            "date": "2025-02-20",
            "start_time": "14:00",
            "end_time": "17:00",
            "participants": ["Michael Wilson", "Emily Davis", "Jane Smith"],
            "notes": "Team Meeting",
        },
        {
            "date": "2025-02-25",
            "start_time": "14:00",
            "end_time": "16:00",
            "participants": ["Emily Davis"],
            "notes": "Project Review",
        },
        {
            "date": "2025-02-26",
            "start_time": "13:00",
            "end_time": "15:00",
            "participants": ["Michael Wilson", "Alice Brown"],
            "notes": "Team Meeting",
        },
        {
            "date": "2025-02-28",
            "start_time": "10:00",
            "end_time": "12:00",
            "participants": ["Robert Johnson", "Michael Wilson", "John Doe"],
            "notes": "Planning Session",
        },
        {
            "date": "2025-03-09",
            "start_time": "13:00",
            "end_time": "15:00",
            "participants": ["Michael Wilson", "Alice Brown"],
            "notes": "Birthday party",
        },
    ]
}


def filter_appointments(appointments, start_date, end_date=None):
    """
    Filters appointments based on a specific date or a date range.

    :param appointments: List of dictionaries containing appointments.
    :param start_date: Single date or start of range (string format 'YYYY-MM-DD').
    :param end_date: End date of range (optional, string format 'YYYY-MM-DD').
    :return: List of filtered appointments.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end_date = start_date  # If not specified, use only the start_date

    filtered_appointments = [
        app
        for app in appointments
        if start_date <= datetime.strptime(app["date"], "%Y-%m-%d") <= end_date
    ]

    return filtered_appointments


def find_free_slots(appointments, start_date, end_date=None):
    """
    Finds free time slots within a given date range.

    :param appointments: List of appointment dictionaries.
    :param start_date: Start date (string format 'YYYY-MM-DD').
    :param end_date: End date (optional, string format 'YYYY-MM-DD').
    :return: Dictionary with dates as keys and lists of free slots as values.
    """
    WORK_START = 8  # Work starts at 8:00 AM
    WORK_END = 18  # Work ends at 6:00 PM

    # Parse start and end dates
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end_date = start_date  # Single day case

    # Create a dictionary to store free slots for each day
    free_slots = {}

    # Loop through each day in the range
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        # Get appointments for the current date
        day_appointments = filter_appointments(appointments, date_str)

        # Sort appointments by start time
        day_appointments.sort(key=lambda x: datetime.strptime(x["start_time"], "%H:%M"))

        # Initialize free slots with the first available time before the first appointment
        free_time = []
        previous_end = WORK_START

        for app in day_appointments:
            start_time = int(
                app["start_time"].split(":")[0]
            )  # Convert "HH:MM" to hour integer
            end_time = int(app["end_time"].split(":")[0])

            if start_time > previous_end:
                free_time.append(
                    f"{previous_end}:00 - {start_time}:00"
                )  # Free time slot

            previous_end = max(previous_end, end_time)  # Update last occupied time

        # Add final free slot if there's time after the last appointment
        if previous_end < WORK_END:
            free_time.append(f"{previous_end}:00 - {WORK_END}:00")

        # Store the free slots for the current date
        free_slots[date_str] = free_time

        # Move to the next day
        current_date += timedelta(days=1)

    return free_slots
