#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from server import app

CGIHandler().run(app)