from datetime import datetime


def days(num):
    days_in_week = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']
    return days_in_week[int(num)]


def extract_current_date():
    dt = datetime.now().date()
    today = dt.strftime('%w')
    return [today, dt]


def extract_time():
    dt = datetime.now()
    current_time = dt.strftime("%H:%M:%S")
    return current_time


def get_index(x, lst):
    return lst.index(x)


def write_sms(speed, gusts, temp, winDirection , idx):
    hour = extract_time()[:-2]
    nextHour = str(int(hour[:2]) +1)+":00"
    thirdHour = str(int(nextHour[:2]) +1)+":00"
    sms = f'{days(extract_current_date()[0])} היום '+'\n' \
          f'{extract_current_date()[1]} :תאריך'+'\n' \
          f'עדכון מזג האוויר'+'\n' \
          f'{hour} שעה' + '\n' \
          f'{speed[idx]} :מהירות הרוח בקשרים '+'\n' \
          f'{gusts[idx]} :עוצמת הרוח בקשרים'+'\n' \
          f'{temp[idx]} :טֶמפֶּרָטוּרָה'+'\n' \
          f'{winDirection[idx]} :כיוון הרוח'+'\n'
    sms += "----------------------------"+'\n'
    sms +=f'{nextHour} שעה הבא' + '\n' \
          f'{speed[idx+1]} :מהירות הרוח בקשרים'+'\n' \
          f'{gusts[idx+1]} :עוצמת הרוח בקשרים'+'\n' \
          f'{temp[idx+1]} :טֶמפֶּרָטוּרָה'+'\n' \
          f'{winDirection[idx+1]} :כיוון הרוח'+'\n'
    sms += "----------------------------"+'\n'
    sms += f'{thirdHour} אחרי שעתיים' + '\n' \
           f'{speed[idx + 2]} :מהירות הרוח בקשרים' + '\n' \
           f'{gusts[idx + 2]} :עוצמת הרוח בקשרים' + '\n' \
           f'{temp[idx + 2]} :טֶמפֶּרָטוּרָה' + '\n' \
           f'{winDirection[idx + 2]} :כיוון הרוח'+'\n'

    return sms
