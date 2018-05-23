#!/usr/bin/python
#--coding=utf8
# -*- coding: utf-8 -*- 

from flask import Flask,json,jsonify
from flask import request, url_for, g, Response
import time
from config import *
from models import *

from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import jieba
from sklearn.naive_bayes import MultinomialNB
import numpy


log = get_logger()


def init_bayes():
    global mnb_count_clf
    global vectorizer
    mnb_count_clf = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer')
def check_spam(content):
    test = vectorizer.transform(numpy.array([content]))
    predict = mnb_count_clf.predict(test)[0]
    return str(predict)



mnb_count_clf = None
vectorizer = None
init_bayes()

app = Flask(__name__)
@app.route('/')
def index():
    return "It Works!"
@app.route('/spamcheck', methods=['POST','GET'])
#@app.route('/feedrecommend/<userid>', methods=['POST','GET'])
def feed_recommend(userid=None):
    if request.headers.get("Content-Type") == 'application/json' \
            or request.headers.get("Content-Type") == 'application/json;charset=utf-8':
        comment = Comment.decode_object(request.json.get('comment','{}') )
        userid = comment.userid

        t1 = time.time()

        result = check_spam(comment.content)

        t2 = time.time()

        log.info("web process for userid: %s, in %2.3fs." %(userid, t2-t1) )
        log.info("%s => [%s]: %s" % (result, userid, comment.content))

        res = { 'status':'OK', 'result': result }

        response = Response(( json.dumps(res, sort_keys=True, indent=4) ),  mimetype='application/json')
        return response
    return '{"status":"ERROR", "items":0 }'

if __name__ == "__main__":
    #server = wsgi.WSGIServer(('0.0.0.0', 9004), app)
    #server.serve_forever()
    app.run('0.0.0.0', 9005, debug = True)
    

