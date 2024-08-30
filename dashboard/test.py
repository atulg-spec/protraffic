import pytz

TIMEZONE_COUNTRIES = sorted(set([(pytz.country_names[code], pytz.country_names[code]) for code in pytz.country_names]))
TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


print(TIMEZONE_COUNTRIES)

