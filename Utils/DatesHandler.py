import datetime

from Models.StatisticModel import StatisticModel


def get_all_dates_from_now(days_count):
    oldest = datetime.datetime.today() - datetime.timedelta(days=days_count - 1)
    return [(oldest + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days_count)]


def fill_data(days, db_result):
    data = {}
    for day in days:
        data[day] = 0
    for line in db_result:
        model = StatisticModel(line[0], line[1])
        if model.date in data.keys():
            data[model.date] = model.count
    return data