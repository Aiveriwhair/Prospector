import Prospector
import Env
import csv

key = Env.Env.getKey()

location1 = (45.187207936661736,5.720326761222223)
location2 = (45.18562697096734,5.721473014913573)
radius = 100
types = ["restaurant"]
fields = ["name", "formatted_address", "formatted_phone_number", "place_id","rating", "url","website"]

prospector = Prospector.Prospector(key)
places = prospector.ScanZonePlaces(location1, location2, radius, types, fields)
f = open("./Dist/places.txt", "w")
with open('./Dist/places.csv', 'w', newline='') as file:
    for place in places:
        f.write(str(place) + "\n")
        writer = csv.writer(file)
        infos = place['result']
        writer.writerow([infos['name'], infos['website'], infos['formatted_address'], infos['formatted_phone_number'], infos['rating'], infos['url']])
    file.close()
f.close()