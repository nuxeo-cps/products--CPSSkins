##parameters=str=None

if str is None:
   return

try:
   v = int(str)
except ValueError:
   return

return v
