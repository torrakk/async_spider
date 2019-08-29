from logging2 import Logger, FileHandler, StdOutHandler, LogLevel
from webcrawler.settings import LOG_PATH, LOG_LEVEL

fh_handler = FileHandler(file_path=LOG_PATH)
stdout = StdOutHandler(level= LogLevel.__getattr__(LOG_LEVEL))

webcrawl = Logger('webcrawl', handlers=[fh_handler, stdout])
scenari_log = Logger('scenari_log', handlers=[fh_handler, stdout])
connect_log = Logger('connecteur', handlers=[fh_handler, stdout])
parse_log = Logger('parseur', handlers=[fh_handler, stdout])
sele_log = Logger('selenium', handlers=[fh_handler, stdout])