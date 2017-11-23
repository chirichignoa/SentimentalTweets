from flask import Flask, request, Response
from TweetsManager import TweetsManager

app = Flask(__name__)


@app.route('/', methods=['GET'])
def getUserOpinions():
    category = request.args.get('category')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    print("Category: " + category)
    if category is None or latitude is None or longitude is None:
        return Response('no pasaste los parametros comosos', status=401, mimetype='application/json')

    if latitude is not None and longitude is not None:
        geocode = latitude + ' ' + longitude
        print("Geocode: " + geocode)
        tweets = TweetsManager().getTweets(category, geocode)
        response = Response(tweets, status=200, mimetype='application/json')
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)