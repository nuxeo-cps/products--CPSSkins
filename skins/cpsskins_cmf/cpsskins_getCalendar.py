
from DateTime import DateTime
from Products.PythonScripts.standard import url_quote

REQUEST=context.REQUEST

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
                 
            begin=DateTime(datestring + ' 12:00:00AM')
            end=DateTime(datestring + ' 11:59:59PM')
            begin_string = url_quote(DateTime(begin.timeTime()+86400).ISO())
            end_string = url_quote(DateTime(end.strftime('%m/%d/%y')).ISO())
            weekday['date_id'] = date_id
            weekday['link'] = portal_url+'/search?review_state=published&amp;' + \
                              '&start_usage=range:max&amp;end_usage=range:min&amp;' + \
                              'start:date=%s&amp;end:date=%s' % (begin_string, end_string)
        weekdays.append(weekday)
    calendar.append(weekdays) 

return {'calendar': calendar, 
        'previews': previews,
        'this_month': this_month,
        'this_year': year,
       }
