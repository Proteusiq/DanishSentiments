import re
# For our Timer decorator
from datetime import datetime
import humanfriendly

# For our ML
from sklearn.base import TransformerMixin

def time_me(function):
    '''
    Outputs function execution time in humanized form
    Starts at Seconds level
    '''
    def wrapper(*args,**kwargs):
        '''
        returns functions output if any
        '''
        u = datetime.now() # Start time
        f_return = function(*args,**kwargs)
        v = datetime.now() # End time

        delta = v - u
        print('Execution Time: {}'.format(
            humanfriendly.format_timespan(delta.seconds))
            )
        return f_return #Return function contents
    return wrapper


class DanishCleaner(TransformerMixin):
    '''
    re has to be loaded
    '''
    
    def __init__(self, 
                 words_only=False,word_normalize=False,emoji_normalize=False,
                 remove_digits=False,lower_case=False, token=False):
        
        self.words_only = words_only
        self.word_normalize = word_normalize
        self.emoji_normalize = emoji_normalize
        self.remove_digits = remove_digits
        self.lower_case = lower_case
        self.token = token
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        self.X = X
        
        # eyes [nose] mouth | mouth [nose] eyes pattern
        emoticons = r"(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|[\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"
        emoticon_re = re.compile(emoticons, re.VERBOSE | re.I | re.UNICODE)
        
        # Keep word only. Digit are consider true Emojis false
        if self.words_only:
            clean_text = self.X.apply(lambda x: (re.sub('[\W]+', ' ', x)))
        else:
            clean_text = self.X.apply(lambda x: ('{}{}'.format(re.sub('[\W]+', ' ', x),
                          ''.join(re.findall(emoticon_re, x)))))

        # normalize emoji?
        if self.emoji_normalize:

            clean_text = self.X.apply( lambda x:
                            (re.sub('[\W]+', ' ', x) +
                                  ' '.join(re.findall(emoticon_re, x)).replace(';',':').replace('-',''))
                            )

        if self.remove_digits:
            clean_text = clean_text.apply(lambda x: x.translate(str.maketrans('','','0123456789')))
       
        if self.lower_case:
            clean_text = clean_text.str.lower()
            
                
        if self.word_normalize:
            try:
                import Stemmer
                stemmer = Stemmer.Stemmer('danish')
                clean_text = clean_text.apply(lambda x: ' '.join(stemmer.stemWords(x.split())))
            except ModuleNotFoundError:
                print('Stemmer is not found. Try "pip install pystemmer"')
                print('Words not normalize')
                pass #Continue with issue
        
        if self.token:
            return clean_text.str.split()
        else:
            return clean_text

# Our Tokenizer

def token(X, 
         words_only=False,word_normalize=True,
         emoji_normalize=True,remove_digits=True,
          lower_case=True,stop_words = None):
        '''
        requires Stemming if word_normalize = True
        use pip[env] install stemming 
        '''
        
        # eyes [nose] mouth | mouth [nose] eyes pattern
        emoticons = r"(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|[\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"
        emoticon_re = re.compile(emoticons, re.VERBOSE | re.I | re.UNICODE)
        
        # Keep word only. Digit are consider true Emojis false
        if words_only:
            clean_text = re.sub('[\W]+', ' ', X)
        else:
            clean_text = '{}{}'.format(re.sub('[\W]+', ' ', X),
                          ''.join(re.findall(emoticon_re, X)))

        # normalize emoji?
        if emoji_normalize:

            clean_text = (re.sub('[\W]+', ' ', X) +
                                  ' '.join(re.findall(emoticon_re, X)).replace(';',':').replace('-','')
                         ) 

        if remove_digits:
            clean_text = clean_text.translate(str.maketrans('','','0123456789'))
       
        if lower_case:
            clean_text = clean_text.lower()
        
        if word_normalize:
            try:
                import Stemmer
                stemmer = Stemmer.Stemmer('danish')
                clean_text = ' '.join(stemmer.stemWords(clean_text.split()))
            except ModuleNotFoundError:
                print('Stemmer is not found. Try "pip install pystemmer"')
                print('Words not normalize')
                pass #Continue with issue
            
        
        if stop_words:
            
            return [word for word in clean_text.split() if word not in stop_words]
        else:
            return clean_text.split()
        
# Summary of steps
@time_me
def load_data(path_to_file, seed=7, balanced=True):
    import pandas as pd
    import numpy as np
    print('Loading data ...')
    df = pd.read_pickle(path_to_file, compression='gzip')
    np.random.seed(seed)
    df = df[['reviewBody','ratingValue']]
    df = df.reindex(np.random.permutation(df.index))
    df.rename(columns={'reviewBody':'features','ratingValue':'target'}, inplace=True)
    
    print('Droping {} rows with features lenght of less than 2'.format(len(df[(df['features'].str.len()<2)])))
    df.drop(index=df[(df['features'].str.len()<2)].index, inplace=True)
    print('Droping 3 as rating and setting 1-2 as negative(0), 4-5 as positive(1))')
    df.drop(df[~(df['target']!=3)].index, inplace=True)

    df['y'] = np.where(df['target']>3,1,0)
    print(df['y'].value_counts().to_dict(),'\n')
    _ = df['y'].value_counts().plot(kind='bar', title='Unbalanced Sentiment Distribution')
    
    if balanced:
        print('Down sampling positive ratings to match negatives')

        pos = df[df['y']==1].sample(len(df[df['y']==0]))
        neg = df[df['y']==0]
        df = pos.append(neg, ignore_index = True)
    print('Data loading completed')
    print(df['y'].value_counts().to_dict(),'\n')
    
    return df

# Function modification of Mike Lee Williams(mike@mike.place)
def show_most_informative_features(feature_names, clf, n=1000):
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % ((coef_1), fn_1, (coef_2), fn_2))
        

# Show me some stats
@time_me
def show_diagram(trained_clf, X_train, y_train, X_test, y_test, compare_test=True):
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc, classification_report
    
    print('Classification Report')
    print('\t','_'*45)
    print(classification_report(y_test,
             trained_clf.predict(X_test),target_names=['Negative','Positive']))
    
    print('\t','_'*45,'\n'*2)
    
    plt.figure(figsize=(10,5))
               
    title = 'Receiver operating characteristic'
    data = [[X_test, y_test, 'red','Test'],[X_train, y_train, 'blue','Train']]
    
        
    for i, j in enumerate(data):

        y_pred, y_pred_prob = trained_clf.predict(j[0]), trained_clf.predict_proba(j[0])[:,1]
        clf_score = trained_clf.score(j[0], j[1])

        fpr,tpr,_ = roc_curve(j[1], y_pred_prob) # remember we need binary

        plt.plot(fpr,tpr,lw=4, 
                 color=j[2], label='{} ROC curve (area ={:.2f})'.format(j[3], clf_score));
        
        if not compare_test:
            break
       
        
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('{}'.format(title))
    plt.legend(loc="lower right")
    plt.show()
    
    
def persist_model(name,clf=None, method='load'):
    'Pass in the file name, object to be saved or loaded'
    
    if method == 'load':
        with open(name,'rb') as f:
            return dill.load(f)
    elif method == 'save':
        print(f'Persisting {name} ...')
        if clf is None:
            raise ValueError('Pass Model/Pipeline/Transformation')
        with open(name,'wb') as f:
            dill.dump(clf,f)
            print(f'Done.')
    else:
        raise ValeuError('Wrong arguments')