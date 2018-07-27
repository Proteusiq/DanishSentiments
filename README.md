# Building Danish Sentiments
PyData CPH: Talk on Building and Deploying Danish Sentiment Model (26-07-2017) at GiG

## Disclaimers
This project is far from being done (mostly the flask apps). It is intended for academic and fun reasons only. It is not my fault, if you mess something up :)

#### How-tos & Requirements

Make sure you have pipenv. If you do not. you can get it via pip install (pip --version has has to be >= 9.0.1)
```bash
pip install --user pipenv
```

Clone this repository and enter the project folder: e.g.

``` bash
git clone https://github.com/Proteusiq/DanishSentiments.git
cd DanishSentiments
pipenv install
pipen shell

```

To run jupyter tools, e.g. jupyter lab

```bash
jupyter lab
```

In order to run the flask_app, you need to train the SGDClassifier by running **SGD_LogRG.ipynb** located on notebooks folder. This will generate HashBectorizer.pkl and SGDClassifier.pkl. Training takes less that 6 minutes on Windows 10, 64bit 16GB RAM.

To do so, assuming you have jupyter lab running,
- navigate to notebooks and select SGD_LogRG.ipynb
- Next to File Edit View is Run. Click and select Run All Cells

If everying went well, you have generated HashVectorizer.pkl and SGDClassifier.pkl

You can press Ctrl(Command) + C to exit jupyter lab and back to your terminal: Type

```bash
cd flask_app
python appy.py
```

You are good to go :) 

**Note:** app.py is running of debugging mode. This is to allow changes. If you want to set the mode in product, make sure to set
debugging to False.

### Pending Documentation ...

N.B: This project was build in Python 3.6, and uses f-formating, that might cause issues with lower Python version. lover python version will throw:

##### SyntaxError ERROR
``` f'Positive: With {pos_proba:.1%} Probability'```
 
If you would like to use lower Python version, just git clone the project and change f-formating string to normal
.format() e.g.
```'Positive: With {:.1%} Probability'.format(pos_proba)```



