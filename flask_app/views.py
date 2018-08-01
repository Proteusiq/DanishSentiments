import sys
import secrets
from sklearn.externals import joblib

# To get app.py initialization of Flask
from app import app,db
from storage import UserFeedBack
sys.path.insert(0, '../notebooks/')

from flask import redirect, render_template, request, url_for

clf = joblib.load('../SGDclassifier.pkl')
hash_vec = joblib.load('../HashVectorizer.pkl')



@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    
    # workingdb = UserFeedBack.query.first()
    # print(workingdb.features)

    header = 'A Toy Danish Sentiment Analysis'
    contents ='Write or paste a review and lets attempt to computes its sentiment'
    try:
        global review
        review = request.form['review']
        #print(review)

        if review:
            return redirect(url_for('submit'), code=307)
        else:
            
            print('Nothing here')
            render_template('home.html', header=header, contents=contents)
    except KeyError:
        #wait to get the review input
        print('KeyError: Waiting for a review')
        pass
    
    return render_template('home.html', header=header, contents=contents)


@app.route('/submit', methods=['POST','GET'])
def submit():
    global pos_proba, neg_proba, X #Used in Response for ReTraining
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
        except (NameError):
            #There is no text so redirect to home
            #Go to else part
            pass
       
    else:
        #print('Nothing here, going home')
        return redirect(url_for('home'), code=302) 

            

@app.route('/response', methods=['GET'])
def response():
    try:
        user_response = request.args['response_button']
        #print(user_response)
        if user_response == 'yes':
            good_list = ['We are awesome!','You have to say, I am good!',
                    'That was easy!', 'Glad you agreed :)']
            gb_feed = secrets.choice(good_list)
            
            #print(gb_feed)
        elif user_response == 'no':
        
            bad_list = ['Bumma! I knew, I failed!',
                        'I fail 6% of times, you know',
                    'That was hard!', 'Wrong? Øv :(']
            gb_feed = secrets.choice(bad_list)
                
        feedback = ('Your response was used to retrain the model')

        # Populate our DataBase
        if (user_response == 'yes' and pos_proba >.5):
            target = 1
        elif (user_response == 'yes' and neg_proba >.5):
            target = 0
        elif (user_response == 'no' and pos_proba >.5):
            target = 0
        elif (user_response == 'no' and neg_proba >.5):
            target = 1
        else:
            print('Something went wrong')
            target = None
        # We can gather data for a bulk retrain or simply retrain
        # for Bulk return, we need to gather data
        content_to_db = UserFeedBack(features=review,target=target)    
        db.session.add(content_to_db)
        db.session.commit()

        # For on-spot retrain
        print('model re-training')
        clf.partial_fit(X,[target], sample_weight=[100]) # Rapid learning
        joblib.dump(clf,'../SGDclassifier.pkl')
        

        return  render_template('response.html',header='Thank You:', 
                                contents=gb_feed,contents_extra=feedback)

    except NameError as e:
        print('We got some error', e)
        print('Routing to home')
        return redirect(url_for('home'), code=302)     
