
* REQUIREMENTS:
  - ZopeTestCase >= 0.9.0 is required
    http://zope.org/Members/shh/ZopeTestCase


* Set the SOFTWARE_HOME and INSTANCE_HOME environment variables
  for your Zope installation:

  $ export SOFTWARE_HOME=/usr/zope/Zope-2.7.0/lib/python/ 
  $ export INSTANCE_HOME=/var/lib/zope/zope-instance


* Set the CPSSKINS_TARGET environment variable for your platform
  and run the tests with 'python runalltests.py'

  - CMF (Default):
  $ CPSSKINS_TARGET=CMF python runalltests.py

  - CPS2:
  $ CPSSKINS_TARGET=CPS2 python runalltests.py

  - CPS3:
  $ CPSSKINS_TARGET=CPS3 python runalltests.py

  - Plone2:
  $ CPSSKINS_TARGET=Plone2 python runalltests.py
