from datetime import datetime, timedelta

def get_day_index(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    day_index = []
    current_date = start

    while current_date <= end:
        day_index.append(current_date.timetuple().tm_yday)
        current_date += timedelta(days=1)

    return day_index

# Example usage
#start_date = "2020-06-01"
#end_date = "2023-06-01"
#day_index = get_day_index(start_date, end_date)

#print(f"The day index between {start_date} and {end_date} is: {day_index}")


def get_years_in_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    years = []
    current_date = start

    while current_date <= end:
        year = current_date.year
        if year not in years:
            years.append(year)
        current_date += timedelta(days=1)

    return years

# Example usage
#start_date = "2020-06-01"
#end_date = "2023-06-01"
#years = get_years_in_range(start_date, end_date)

#print(f"The years in the range {start_date} to {end_date} are: {years}")

def split_date_range_on_new_year(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    sub_ranges = []
    current_start = start

    while current_start.year < end.year:
        current_end = datetime(current_start.year, 12, 31)
        sub_ranges.append((current_start.strftime("%Y-%m-%d"), current_end.strftime("%Y-%m-%d")))

        current_start = datetime(current_start.year + 1, 1, 1)

    sub_ranges.append((current_start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

    return sub_ranges

# Example usage
start_date = "2020-06-06"
end_date = "2023-06-06"
sub_ranges = split_date_range_on_new_year(start_date, end_date)

for strt, endd in sub_ranges:
    print(strt,endd)
    print(get_day_index(strt,endd))