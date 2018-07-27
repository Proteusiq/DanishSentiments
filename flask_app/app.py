import sys
sys.path.insert(0, '../notebooks/')
from flask import (Flask, render_template,
                     request, redirect, url_for)
from sklearn.externals import joblib



clf = joblib.load('../SGDclassifier.pkl')
hash_vec = joblib.load('../HashVectorizer.pkl')

# X = hash_vec.transform(['jeg elsker pizze'])
# y = clf.predict_proba(X)
# print(X,y,clf.classes_)

## load stops tokenize and model
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
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
    
    return render_template('home.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    print('We are here ..')

    try:
        return render_template('result.html', in_review=review,in_response='Positive')
    except NameError:
        #There is no text so redirect to home
        print('Nothing here, going home')
        return redirect(url_for('home'), code=307)


if __name__ == '__main__':
    app.debug = True
    app.run()
