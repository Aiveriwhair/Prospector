import Prospector
import Env
import csv

key = Env.Env.getKey()

location1 = (45.191065641583734,5.704763393476271)
location2 = (45.15672344139212,5.744806452056914)
radius = 100
types = ["restaurant"]
fields = ["name","url","website"]

prospector = Prospector.Prospector(key)
places = prospector.ScanZonePlaces(location1, location2, radius, types, fields)