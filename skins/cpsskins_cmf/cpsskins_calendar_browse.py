##parameters=dir, REQUEST=None

if REQUEST is None or dir not in ['prevmonth', 'nextmonth']:
    return

year, month = context.cpsskins_getMonthAndYear()

if dir == 'prevmonth':
    MonthTime = context.portal_calendar.getPreviousMonth(month, year)
elif dir == 'nextmonth':
    MonthTime = context.portal_calendar.getNextMonth(month, year)

referer_url = REQUEST.get('HTTP_REFERER', context.absolute_url())
referer_url = referer_url.split('?')[0]
url_string =  '%s?year:int=%d&month:int=%d'
redirect_url = url_string % (referer_url, MonthTime.year(), MonthTime.month())

REQUEST.RESPONSE.redirect(redirect_url)
