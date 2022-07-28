# -*- coding: utf-8 -*-
import sys
import locale
print (sys.getdefaultencoding())
print (locale.getpreferredencoding()) # linux
# и самое интересное:
print (sys.stdout.encoding) # linux
