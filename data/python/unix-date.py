from time import strftime

def get_unix_date():
    """Same output as Unix's date command.
    
    Example: Fri Apr  6 14:23:27 CEST 2012"""
    return strftime("%a %b %e %H:%M:%S %Z %Y")
