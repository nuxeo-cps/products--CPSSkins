
from DateTime import DateTime

REQUEST = context.REQUEST
base_url = REQUEST.get('cpsskins_base_url')
if base_url is None:
    base_url = context.cpsskins_getBaseUrl()

# remove the trailing /
context_url = base_url[:-1]

portal_calendar = context.portal_calendar

current = DateTime()
current_day = current.day()
current_month = current.month()
current_year = current.year()
year, month = context.cpsskins_getMonthAndYear()
current_month_and_year = (current_year == year and current_month == month)

weeks = portal_calendar.getCPSEventsForCalendar(month=month, 
                                                year=year, 
                                                location=None, 
                                                event_types=[])

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
            datestring = '%s/%s/%s' % (year, month, daynumber)
            date_id = '%s%s%s' % (year, month, daynumber)
            info = {'date': datestring, 'date_id': 'day%s' % date_id, 'eventslist': day['eventslist'] }
            previews.append(info)
                 
            weekday['date_id'] = date_id
            weekday['link'] = context.getCalCPSDayViewParams(
               context_url=context_url,
               datestring=datestring,
               location=None, event_types=[])

        weekdays.append(weekday)
    calendar.append(weekdays) 

return {'calendar': calendar, 
        'previews': previews,
        'this_month': this_month,
        'this_year': year,
       }
