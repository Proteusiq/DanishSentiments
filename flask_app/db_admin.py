# CLI Create and drop database
# e.g. python db_admin.py create 
import sys
from app import db


def model_train():
    sys.path.insert(0, '../notebooks/')

    from helper import load_data, token
    from datetime import datetime
    import humanfriendly
    import pandas as pd
    import numpy as np

    from sklearn.externals import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import HashingVectorizer
    from sklearn.linear_model import SGDClassifier

    stops = joblib.load('../stops.pkl')
    df = load_data('../sentiment_data', balanced=True)

    hash_para = dict(decode_error='ignore', n_features=2**18, tokenizer=token,
                stop_words=stops, ngram_range=(1,3), alternate_sign=False)
    clf_prep = HashingVectorizer(**hash_para)

    
    clf_prep = HashingVectorizer(**hash_para)
    clf = SGDClassifier(loss='log', random_state=1, max_iter=1)


    u = datetime.now()
    clf.partial_fit(clf_prep.transform(df['features']), 
                                       df['y'],classes=np.unique(df['y']))
    v = datetime.now()
    delta = v-u
    print('Training took: {}'.format(
        humanfriendly.format_timespan(delta.seconds)))

    joblib.dump(clf_prep, '../HashVectorizer.pkl')
    joblib.dump(clf, '../SGDclassifier.pkl')

if sys.argv[1] =='create':
    input('We are going to create all db')
    db.create_all()
if sys.argv[1] == 'drop':
    input('We are going to drop all db')
    db.create_all()
try:
    if (sys.argv[1] == 'drop' and sys.argv[2] == 'create'):
        input('We are going to drop all and create all db')
        db.create_all()
        db.create_all()
except IndexError:
    # No second argument
    pass
if sys.argv[1] =='train':
    input('Training Model from Scratch ...')
    model_train()
