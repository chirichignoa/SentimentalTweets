from TwitterAPI import TwitterAPI
import json
from DBManager import DBManager
from api import Sentiment140API
import datetime


class TweetsManager(object):
    """API Key y API Secret de la cuenta creada por Chiri.
    Estas se utilizan para obtener los permisos de twitter para obtener consumir los servicios publicados por ellos."""
    API_KEY = "CSpOkRRVNFYwfAlWdJsQ3j43D"
    API_SECRET = "l9XJ3Q34kEUtAhZ9o0OVfl03Vt8eMWXKCoRkqWvwJZP5lOE6It"
    ACCESS_TOKEN = "271047508-uqaAWSb4FjIT5Yc4PZfKEfLRT4CBSEzzpaa2BgsX"
    SECRET_TOKEN = "GVX80GRWtVvXtPg9EwIjBMKQh71pQEtwhW1iko9U9rc3r"
    TWEETS_LIMIT = 50
    LANGUAGE = 'es'
    MAX_RADIUS = '100km'

    def __init__(self):
        '''Instancia de twitter API'''
        self.api = TwitterAPI(self.API_KEY, self.API_SECRET, self.ACCESS_TOKEN, self.SECRET_TOKEN)
        self.db = DBManager.Instance()

    def getTweets(self, category, geocode):

        last_date = self.db.get_last_date(category)
        today_date = datetime.datetime.strptime(datetime.date.today().isoformat(), "%Y-%m-%d").date()

        if (last_date is None) or (last_date + datetime.timedelta(days=7) < today_date):
            print('Building request')
            response = self.api.request('search/tweets',
                                        {'q': category + '-filter:retweets', 'count': self.TWEETS_LIMIT,
                                         'lang': self.LANGUAGE, 'geocode': geocode + self.MAX_RADIUS})
            texts = []
            for item in response:
                # transformar el json para que en mongo quede formateado. Sino, queda co un string con saltos de linea.
                texts.append({
                    'text': item['text'],
                    'created_at': item['created_at'],
                    'user_name': item['user']['name'],
                    'user_profile_image_url': item['user']['profile_image_url'],
                    'user_screen_name': item['user']['screen_name']
                })

            classified_tweets = self.classify_tweets(texts)

            print classified_tweets

            self.db.insert_tweets(category, datetime.date.today().isoformat(), geocode, classified_tweets)
        else:
            print('Getting tweets from BD')
            classified_tweets = self.db.get_last_tweets(category, geocode)

        return classified_tweets

    @staticmethod
    def classify_tweets(tweets):
        api = Sentiment140API('')
        result = api.bulk_classify_json(tweets)
        return json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
