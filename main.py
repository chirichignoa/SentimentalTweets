from flask import Flask, request, Response
from TweetsManager import TweetsManager

app = Flask(__name__)


@app.route('/', methods=['GET'])
def getUserOpinions():
    category = request.args.get('category')
    print category
    if category is None:
        return Response('no pasaste los parametros comosos', status=401, mimetype='application/json')

    tweets = TweetsManager().getTweets(category)

    response = Response(tweets, status=200, mimetype='application/json')
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)