![image](https://user-images.githubusercontent.com/14926709/43322711-be0344a6-91af-11e8-83ca-2aa47ab5700f.png)

# Building Danish Sentiments
PyData CPH: Talk on Building and Deploying Danish Sentiment Model (26-07-2017) at GiG

## Disclaimers
This project is far from being done (mostly the flask apps). It is intended for academic reason only. It is not my fault, if you mess something up on your machine :). 

## How-tos & Requirement

Make sure you have pipenv. If you do not, you can get it via pip install (pip --version has to be >= 9.0.1).
```bash
pip install --user pipenv
```
add pipenv to your path:e.g on Windows, you would do
```
SETX PATH "%PATH%;%APPDATA%\python\python36\scripts"
```
restart the terminal. 

Clone this repository and enter the project folder and pipenv install packages:

``` bash
git clone https://github.com/Proteusiq/DanishSentiments.git
cd DanishSentiments
pipenv install
pipenv shell

```

In pipenv shell, you can run jupyter tools, e.g. jupyter lab

```bash
jupyter lab
```

In order to run the flask_app, you need to train the SGDClassifier by running **SGD_LogRG.ipynb** located in notebooks folder. This will generate HashBectorizer.pkl and SGDClassifier.pkl. Training takes less than 6 minutes on Windows 10, 64bit 16GB RAM.

To do so, assuming you have jupyter lab running,
- navigate to notebooks and select SGD_LogRG.ipynb
- Next to File Edit View is Run. Click and select Run All Cells

If everying went well, HashVectorizer.pkl and SGDClassifier.pkl would have been generated.

You can press Ctrl(Command) + C to exit jupyter lab and back to your shell terminal: Type

```bash
cd flask_app
python appy.py
```

You are good to go :) 

**Note:** app.py is running on debugging mode. This is to allow changes. If you want to put the model in production, make sure to set debugging to False.

### Pending Documentation ...

N.B: This project was build in Python 3.6, and uses f-formating, that might cause issues with lower Python version. lover python version will throw:

##### SyntaxError ERROR
``` f'Positive: With {pos_proba:.1%} Probability'```
 
If you would like to use lower Python version, just git clone the project and change f-formating string to normal
.format() e.g.
```'Positive: With {:.1%} Probability'.format(pos_proba)```

### TODO:
- Gather users input for model retraining
- Rewrite the flask_app to actually do what it is suppose to do
- Grid search better parameter for partial_fit models
- A better tokenizer (remove places and peoples names)
- Clean code everywhere :)



