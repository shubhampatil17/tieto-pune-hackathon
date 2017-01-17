import pandas as pd
import database_connection
from models import Population

def create_population_dataset():
    if not len(Population.objects):
        print("STATUS : Loading population dataset into database ...")
        dataframe = pd.read_csv('population.csv', encoding="ISO-8859-1")
        for index, row in dataframe.iterrows():
            try:
                population = Population(country=row[0], city=row[1], population=int(row[4]))
                population.save()
            except:
                print("EXCEPTION : Error at row {}.".format(index))
        print("STATUS : Loading complete !")
