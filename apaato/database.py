# database.py

# Import sqlite3 to store accommodations in a database
import sqlite3

import os
import sys
from pathlib import Path

# Import generator for annotations
from typing import Generator

# Import framework
from apaato.accommodation import Accommodation

dir_name = os.path.expanduser('~/Documents/apaato')
file_name = "/accommodations_db.sqlite"

class AccommodationDatabase:

    def __init__(self, new_database: bool = False):

        if new_database:
            try:
                os.mkdir(dir_name)
            except FileExistsError:
                pass
        else:
            if not Path(dir_name + file_name).is_file():
                print("No database found. Please run 'apaato load'.")
                sys.exit()

        self.conn = sqlite3.connect(dir_name + file_name)

        self.curs = self.conn.cursor()
        self.curs.execute(""" CREATE TABLE IF NOT EXISTS accommodations (
                          address text,
                          refid text,
                          size text,
                          date text,
                          applicants integer,
                          first integer,
                          second integer,
                          third integer,
                          fourth integer,
                          fifth integer) """)
        if new_database:
            self.wipe()

    def insert_accommodation(self, acc: Accommodation) -> None:
        """ Inserts an Accommodation object into database """

        acc_prop = {**acc.__dict__,
                    **(dict(zip(
                    ['first', 'second', 'third', 'fourth', 'fifth'],
                    acc.queue_points_list)))}

        with self.conn:
            self.curs.execute(""" INSERT INTO accommodations VALUES (:address,
                                                             :refid,
                                                             :size,
                                                             :date,
                                                             :applicants,
                                                             :first,
                                                             :second,
                                                             :third,
                                                             :fourth,
                                                             :fifth) """,
                      acc_prop)


    def to_accommodation(self, accommodation_properties: tuple) -> Accommodation:
        """ Makes a new Accommodation object from tuple from sql query """

        return Accommodation(**self.to_dict(accommodation_properties))

    def to_dict(self, accommodation_properties: tuple) -> dict:
        """ Takes tuple (from database) and zips it with the kwargs names of the
        Accommodation class """

        property_names = ['address', 'refid', 'size', 'date', 'applicants']

        return {**dict(zip(property_names, accommodation_properties[:-5])),
                'queue_points_list': list(accommodation_properties[-5:])}

    def query(self, query_text: str) -> Generator[Accommodation, None, None]:
        """ Takes a search query and yields all results as Accommodation
        objects """

        with self.conn:
            self.curs.execute(query_text)
            yield from map(self.to_accommodation, self.curs.fetchall())

    def get_accommodations_with_date(self, date):
        search = "SELECT * FROM accommodations WHERE date LIKE '" + date + "'"
        yield from self.query(search)

    def get_all_accommodations(self):
        search = "SELECT * FROM accommodations"
        yield from self.query(search)

    def wipe(self) -> None:
        """ Wipes database """

        with self.conn:
            self.curs.execute('DELETE FROM accommodations')

