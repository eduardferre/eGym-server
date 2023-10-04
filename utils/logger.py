import logging as logging_pkg


class CustomFormatter(logging_pkg.Formatter):
    blue_soft = "\x1b[34;2m"
    blue = "\x1b[34;3m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s:     %(asctime)s || %(message)s - (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging_pkg.DEBUG: blue_soft + format + reset,
        logging_pkg.INFO: blue + format + reset,
        logging_pkg.WARNING: yellow + format + reset,
        logging_pkg.ERROR: red + format + reset,
        logging_pkg.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging_pkg.Formatter(log_fmt)
        return formatter.format(record)


# create logger with 'spam_application'
logging = logging_pkg.getLogger("eGym")
logging.setLevel(logging_pkg.INFO)
# create console handler with a higher log level
ch = logging_pkg.StreamHandler()
ch.setLevel(logging_pkg.INFO)
ch.setFormatter(CustomFormatter())
logging.addHandler(ch)
