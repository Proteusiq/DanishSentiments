'''
 This is how not to code flasks app :) I have just chicken around
 to produce a simple flask app for the model :). A clean and more
 thoughtful app is coming soon ...
'''

import sys
sys.path.insert(0, '../notebooks/')
from flask import (Flask, render_template,
                     request, redirect, url_for)
from sklearn.externals import joblib


## load stops tokenize and model
clf = joblib.load('../SGDclassifier.pkl')
hash_vec = joblib.load('../HashVectorizer.pkl')

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():

    header = 'A Toy Danish Sentiment Analysis'
    contents ='Write or paste a review and lets attempt to computes its sentiment'
    try:
        global review
        review = request.form['review']

        if review:
            return redirect(url_for('submit'), code=307)
        else:
            
            print('Nothing here')
    except KeyError:
        #wait to get the review input
        print('KeyError: Waiting for')
        pass
    
    return render_template('home.html', header=header, contents=contents)


@app.route('/submit', methods=['POST','GET'])
def submit():
   
    if request.method == 'POST':
        try:
            X = hash_vec.transform([review])
            y = clf.predict_proba(X)

            neg_proba,pos_proba = y[0][0],y[0][1]

            if pos_proba > .5:
                message = f'Positive: With {pos_proba:.1%} Probability'
            else:
                message = f'Negative: With {neg_proba:.1%} Probability'

            return render_template('result.html',header='Sentiment Message:', 
                                    contents=review,in_response=message)
        except NameError:
            #There is no text so redirect to home
            print('Nothing here, going home')
            return redirect(url_for('home'), code=307)
    print('Not a Post Request')


if __name__ == '__main__':
    app.debug = True
    app.run()
