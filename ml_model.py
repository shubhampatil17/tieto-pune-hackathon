import glob
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm

d1_files = glob.glob('CrisisLexT6/*.csv')
d2_files = glob.glob('CrisisLexT26/*.csv')
sentiment_files = glob.glob('SentimentData/*.csv')

d1_training_X = []
d1_training_Y = []
d2_training_X = []
d2_training_Y = []
sentiment_X = []
sentiment_Y = []

for file in d1_files:
    dataframe = pd.read_csv(file, header=0)
    for index, row in dataframe.iterrows():
        d1_training_X.append(row[1])
        d1_training_Y.append(row[2])

for file in d2_files:
    dataframe = pd.read_csv(file, header=0)
    for index, row in dataframe.iterrows():
        d2_training_X.append(row[1])
        d2_training_Y.append(row[4])

for file in sentiment_files:
    dataframe = pd.read_csv(file, header=0)
    for index, row in dataframe.iterrows():
        sentiment_X.append(row[5])
        sentiment_Y.append(row[0])

tweet_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', svm.LinearSVC())])

sentiment_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', svm.LinearSVC())])

tweet_clf_extra = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', svm.LinearSVC())])

tweet_clf.fit(d1_training_X, d1_training_Y)
tweet_clf_extra.fit(d2_training_X, d2_training_Y)
sentiment_clf.fit(sentiment_X, sentiment_Y)

def train_machine_learning_models():
    print("STATUS : Training machine learning classfiers ...")
    tweet_clf.fit(d1_training_X, d1_training_Y)
    tweet_clf_extra.fit(d2_training_X, d2_training_Y)
    sentiment_clf.fit(sentiment_X, sentiment_Y)
    print("STATUS : Training completed !")

