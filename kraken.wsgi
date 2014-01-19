#!/usr/bin/python
import os
import subprocess
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vhosts/KrakenMaster")

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from kraken.app import create_app
from kraken.settings import DevConfig, ProdConfig
from kraken.database import db

if os.environ.get("KRAKEN_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)
