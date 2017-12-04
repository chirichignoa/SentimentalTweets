from flask import Flask, request, Response
from TweetsManager import TweetsManager

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getUserOpinions():
    category = request.args.get('category')
    if category is None:
        return Response('Bad request.', status=401, mimetype='application/json')
    else:
        try:
            tweets = TweetsManager().getTweets(category)
            response = Response(tweets, status=200, mimetype='application/json')
        except ValueError as err:
            response = Response(None, status=500, mimetype='application/json')

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)