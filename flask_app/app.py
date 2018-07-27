import sys
sys.path.insert(0, '../notebooks/')
from flask import (Flask, render_template,
                     request)
from sklearn.externals import joblib



clf = joblib.load('../SGDclassifier.pkl')
hash_vec = joblib.load('../HashVectorizer.pkl')

X = hash_vec.transform(['jeg elsker pizze'])
y = clf.predict_proba(X)
# print(X,y,clf.classes_)

## load stops tokenize and model
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    global review
    review = request.form['review']
    
    return render_template('home.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    print('We are here ..')
    print(review)
    return render_template('result.html', in_review=review,in_response='Positive')


if __name__ == '__main__':
    app.debug = True
    app.run()
