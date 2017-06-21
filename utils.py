import re

def isnumber(n):
    numeric_format = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
    test = re.match(numeric_format, n)
    if test:
        return True
    else:
        return False
