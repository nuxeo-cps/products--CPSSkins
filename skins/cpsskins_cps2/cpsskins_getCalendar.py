##parameters=REQUEST=None

from DateTime import DateTime

if not hasattr(context, 'portal_calendar'):
    return
portal_calendar = context.portal_calendar
portal_url = context.portal_url()

current = DateTime()
current_day = current.day()
current_month = current.month()
current_year = current.year()
year, month = context.cpsskins_getMonthAndYear()
current_month_and_year = (current_year == year and current_month == month)

weeks = portal_calendar.getEventsForCalendar(month=month, year=year)
this_month = DateTime(('%s/1/%s') %(month, year)).strftime('%B').capitalize()

calendar = []
previews = []
for week in weeks:
    weekdays = []
    for day in week:
        weekday = {}
        daynumber = day['day']
        event = day['event']

        weekday['daynumber'] = daynumber
        weekday['event'] = event
        if current_month_and_year and current_day == int(daynumber):
            dayclass = test(event, "todayevent", "todaynoevent")
        else:
            dayclass = test(event, "event", None)
        weekday['class'] = dayclass

        if event:
            datestring = '%s-%s-%s' % (year, month, daynumber)
            date_id = '%s%s%s' % (year, month, daynumber)
            info = {'date': datestring, 'date_id': 'day%s' % date_id, 'eventslist': day['eventslist'] }
            previews.append(info)

            weekday['date_id'] = date_id
            weekday['link'] = portal_url+'/calendar_day_view?date=' + datestring
        weekdays.append(weekday)
    calendar.append(weekdays)

return {'calendar': calendar,
        'previews': previews,
        'this_month': this_month,
        'this_year': year,
       }
