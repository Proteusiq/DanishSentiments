import sys
sys.path.insert(0, '../notebooks/')
from flask import Flask, render_template, request
from sklearn.externals import joblib


clf = joblib.load('../SGDclassifier.pkl')
hash_vec = joblib.load('../HashVectorizer.pkl')

from flask import (Flask, request,
                     Response, jsonify, json)

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def api_home():
    return 'Welcome Home'


@app.route('/go', methods=['GET'])
def api_go():
    if 'text' in request.args:
        text = request.args['text']
        X = hash_vec.transform([text,])

        y = clf.predict(X)
        response = 'Positive' if y == 1 else 'Negative'

        z = clf.predict_proba(X)
    
        z_ = f'Positive Probability: {z[0][1]:.2%}'    
        send = {'predict':response, 'probability':z_}

        print(send)
        
        dumped_sent = json.dumps(send)
        r = jsonify(dumped_sent)

        r.status_code = 200

        return r

    else:
        return 'Nothing to respond :)'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
 

