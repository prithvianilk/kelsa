SECONDS_IN_A_MINUTE = 60
SECONDS_IN_AN_HOUR = SECONDS_IN_A_MINUTE * 60
SECONDS_IN_A_DAY = SECONDS_IN_AN_HOUR * 24

def seconds_to_minutes(seconds):
    return seconds // SECONDS_IN_A_MINUTE

def seconds_to_hours(seconds):
    return seconds // SECONDS_IN_AN_HOUR

def seconds_to_days(seconds):
    return seconds // SECONDS_IN_A_DAY

def is_less_than_an_hour(seconds):
    return seconds < SECONDS_IN_AN_HOUR

def is_more_than_a_day(seconds):
    return seconds >= SECONDS_IN_A_DAY

def is_more_than_an_hour(seconds):
    return seconds >= SECONDS_IN_AN_HOUR