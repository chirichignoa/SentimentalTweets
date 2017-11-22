import datetime
from time import strptime

import pymongo
from flask import json

from Singleton import Singleton
from pymongo import MongoClient

"""El manager es singleton para evitar multiples instancias"""


@Singleton
class DBManager:
    ip = '127.0.0.1'
    port = 27017
    user = ''
    password = ''
    dbName = 'users_opinions'

    def __init__(self):
        try:
            self.client = MongoClient(self.ip, self.port)
            self.database = self.client.get_database(self.dbName)
            collection = self.database['opinions']
            collection.create_index([("category", pymongo.DESCENDING),  ("date", pymongo.DESCENDING)], unique=True)
        except ValueError as err:
            print(err)
            raise  # para no perder el stack trace.

    def insert_tweets(self, category, date, tweets):
        collection = self.database['opinions']
        collection.update({'category': category, 'date': date}, {'$push': {'tweets': tweets}}, upsert=True)

    def get_last_date(self, category):
        collection = self.database['opinions']
        date_cursor = collection.aggregate([
                                        {'$group': {'_id': "$category", 'max_date': {'$max': '$date'}}},
                                        {'$match': {'_id': category}}
                                        ])
        if date_cursor is not None:
            for doc in date_cursor:
                return datetime.datetime.strptime(doc['max_date'], "%Y-%m-%d").date()
        else:
            return None

    def get_last_tweets(self, category):
        collection = self.database['opinions']
        tweets_cursor = collection.aggregate([
                                {'$group': {'_id': "$category", 'tweets': {'$push': '$tweets'}}},
                                {'$match': {'_id': category}}])

        if tweets_cursor is not None:
            for doc in tweets_cursor:
                return json.dumps(doc['tweets'], sort_keys=True, indent=4, separators=(',', ': '))
