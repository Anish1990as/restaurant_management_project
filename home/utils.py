from datetime import datetime, time

def is_restaurant_open():
    """
    Check if the restaurant is currently open based on predefined hours.
    Returns:
        True  -> if restaurant is open
        False -> if restaurant is closed
    """

    # Get current local time and weekday
    now = datetime.now()
    current_day = now.strftime("%A")  # e.g., 'Monday', 'Tuesday'
    current_time = now.time()

    # Define opening hours (example)
    # Format: {day_name: (opening_time, closing_time)}
    opening_hours = {
        "Monday": (time(9, 0), time(22, 0)),     # 9 AM - 10 PM
        "Tuesday": (time(9, 0), time(22, 0)),
        "Wednesday": (time(9, 0), time(22, 0)),
        "Thursday": (time(9, 0), time(22, 0)),
        "Friday": (time(9, 0), time(23, 0)),     # Open later on Fridays
        "Saturday": (time(10, 0), time(23, 0)),  # Weekend hours
        "Sunday": (time(10, 0), time(21, 0)),
    }

    # Check if the current day exists in our schedule
    if current_day not in opening_hours:
        return False  # Closed if not defined

    open_time, close_time = opening_hours[current_day]

    # Compare current time with today's schedule
    return open_time <= current_time <= close_time