from pymongo import *
from datetime import *

client = MongoClient()
db = client.test


def dump_population():
    with open('population.txt') as f:
        for line in f:
            words=line.split(',')
            #print words[0],words[1],words[4]
            db.Population.insert_one(
                 {"country": words[0], "city": words[1], "population": words[4]}
            )

dump_population()

