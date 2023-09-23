datetime_f = '%Y-%m-%d %H:%M'


def str_datetime(date):
    date = date.replace('%3A', ':')
    date = date.replace('T', ' ')
    return date
