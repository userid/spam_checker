#!/usr/bin/python
#coding=utf-8

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import jieba
from sklearn.naive_bayes import MultinomialNB 
import numpy
from sklearn.externals import joblib

from config import *

data=[]
target=[]

f = open("./spam.txt", "r")
for line in f.readlines():
    _t = str.split(line, "\t|\t", 2)
    data.append(_t[1])
    target.append(_t[0])

f.close()
print "%d\t%d\n" %(len(data),len(target))

target = numpy.array(target)
data = numpy.array(data)

X_train,X_test,y_train,y_test = train_test_split(data,target,test_size=1/4.,random_state=38)


vectorizer = CountVectorizer(min_df=1, tokenizer=tokenize)
analyzer = vectorizer.build_analyzer()

X_count_train = vectorizer.fit_transform(X_train) 
X_count_test= vectorizer.transform(X_test)
#for c in vectorizer.get_feature_names():
#    print(c)
mnb_count_clf = MultinomialNB(alpha=1.) 
mnb_count_clf.fit(X_count_train,y_train)

joblib.dump(mnb_count_clf,'model.pkl')
joblib.dump(vectorizer, 'vectorizer')

print mnb_count_clf.score(X_count_test,y_test)

#for i in range(100):
#    x = mnb_count_clf.predict(X_count_test[i])
#    print y_test[i] , '=====',x, X_test[i]
for i in range (len(y_test)):
    x = mnb_count_clf.predict(X_count_test[i])
    if str(x[0]) != str (y_test[i]):
        print y_test[i] , '=====',x, X_test[i]


