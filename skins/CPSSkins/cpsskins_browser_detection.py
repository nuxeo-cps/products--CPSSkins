##parameters=REQUEST=None

def indexElement(pList,pElement):
  try:
    position=pList.index(pElement)
  except:
    position=-1
  return position

if REQUEST==None:
  REQUEST=context.REQUEST

identity=REQUEST.HTTP_USER_AGENT.replace('/',' ').lower()
identity=identity.replace('(','')
identity=identity.replace(')','')
identity=identity.replace(';','')
identityParts=identity.split(' ')

if ('compatible' in identityParts):
  pos=indexElement(identityParts,'opera')
  if (pos>=0):
    browser='Opera'
  else:
    pos=indexElement(identityParts,'msie')
    if (pos>=0):
      browser='Explorer'
    else:
      pos=indexElement(identityParts,'konqueror')
      if (pos>=0):
        browser='Konqueror'
else:
  posMozilla=indexElement(identityParts,'mozilla')
  if (posMozilla>=0):
    #Netscape 6 doesn't have an standard agent string
    pos=indexElement(identityParts,'netscape6')
    if (pos>=0):
      browser='Netscape'
    else:
      #From Netscape 7, the standard agent string was fixed
      pos=indexElement(identityParts,'netscape')
      if (pos>=0):
        browser='Netscape'
      else:
        pos=indexElement(identityParts,'galeon')
        if (pos>=0):
          browser = 'Galeon'
        else:
	  #K-meleon has its own agent string since version 0.7
          pos=indexElement(identityParts,'k-meleon')
          if (pos>=0):
            browser = 'K-Meleon'
          else:
            pos=indexElement(identityParts,'gecko')
            if (pos>=0):
              browser='Mozilla'
              pos-=2
            else:
              #Netscape 4.x identifies itself as Mozilla 4.x
              pos=posMozilla
              browser='Netscape'
  #Add not common browsers here
  else:
    pos=indexElement(identityParts,'lynx')
    if (pos>=0):
      browser='Lynx'
    else:
      pos=indexElement(identityParts,'wget')
      if (pos>=0):
        browser='Wget'
      else:
        pos=indexElement(identityParts,'elinks')
        if (pos>=0):
          browser='Links'
if pos>=0:
  version=identityParts[pos+1]
else:
  version='0'
  browser='unknown'
return [browser,version]
