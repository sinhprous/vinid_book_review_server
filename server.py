from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
app = Flask(__name__)
# log = logging.getLogger('werkzeug')
# log.disabled = True
handler = RotatingFileHandler('text-matching.log', maxBytes=10000, backupCount=1, encoding="utf-8")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)
# app.logger.disabled = True

