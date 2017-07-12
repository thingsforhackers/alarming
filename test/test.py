import datetime
import dateutil
from dateutil.relativedelta import *
from dateutil.rrule import *


NOW = datetime.datetime.now()

print "NOW:\t", NOW

AL = NOW+relativedelta(hour=12, minute=16)

print "AL:\t", AL

if AL < NOW:
    #Already happend today, move to next
    AL = rrule(DAILY, byweekday=(SA, SU), dtstart=AL)[1]


print "nAL:\t", AL, type(AL)

