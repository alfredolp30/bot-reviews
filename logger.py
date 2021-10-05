import logging

def setLogging(logLevel: str):
    LEVELS = { 
        "debug": logging.DEBUG, 
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR 
    }

    level = logging.ERROR
        
    try: 
        level = LEVELS[logLevel]
    except:
        level = logging.ERROR

    logging.basicConfig(level=level)
        
