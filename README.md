![image](https://user-images.githubusercontent.com/14926709/43322711-be0344a6-91af-11e8-83ca-2aa47ab5700f.png)

# Building Danish Sentiment Models
[PyData CPH](https://www.meetup.com/PyData-Copenhagen/): Talk on Building and Deploying Danish Sentiment Model (26-07-2018) at GiG

## Disclaimers
This project is far from being done (mostly the flask apps). It is intended for academic reason only. It is not my fault, if you mess something up on your machine :). There exists typos everywhere, do point them out.

## How-tos & Requirement

Make sure you have pipenv. If you do not, you can get it via pip install (pip --version has to be >= 9.0.1).
```bash
pip install --user pipenv
```
add pipenv to your path: e.g on Windows, you would do
```
SETX PATH "%PATH%;%APPDATA%\python\python36\scripts"
```
restart the terminal. 

Clone this repository, and enter the project folder. Execute _pipenv install_ to install all packages.

``` bash
git clone https://github.com/Proteusiq/DanishSentiments.git
cd DanishSentiments
pipenv install
pipenv shell

```

_pipenv shell_ activates our environment. In pipenv shell, you can run jupyter tools, that comes as part of the package, e.g. _jupyter lab_

```bash
jupyter lab
```

In order to run the flask_app, you need to train the SGDClassifier by running [**SGD_LogRG.ipynb**](./notebooks/SGD_LogRg.ipynb) located in notebooks folder. This will generate _HashVectorizer.pkl_ and _SGDClassifier.pkl_ files. Training takes less than 2 minutes on Windows 10, 64bit 16GB RAM.

Training data came from TrustPilot Reviews. I wrote a simple helper function [TrustPilotReader](https://github.com/Proteusiq/TrustPilotReader), in case you want more training data or wish to train a different language model, e.g. Norwegian Sentiment Model :).

Back to our current model! :) Assuming you have _jupyter lab_ running,
- navigate to notebooks folder and select SGD_LogRG.ipynb. This notebook contents a simple [Stochastic Gradient Descent Classifier](http://scikit-learn.org/stable/modules/sgd.html#classification).
- Next to File Edit View is Run. Click and select Run All Cells. Model score: 92%

If everything went well, _HashVectorizer.pkl_ and _SGDClassifier.pkl_ would have been generated and will be used by our flask apps.

Head back to terminal. You can press Ctrl(Command) + C to exit jupyter lab server. On your shell terminal: Execute:

```bash
cd flask_app
python app.py
```

You are good to go :) Flask app should be running on port 5000. On your browser, head to localhost:5000.

**NB:**This project is under development. To get current version, use:

```bash
git pull
```

,here and there, to get the current version.

## Structure
- Data Gathering, Exploration and Cleaning([EDA_Sentiment.ipynb](./notebooks/EDA_Sentiment.ipynb))
- Finding simple logit model that is fast and re-trainable
- Serve the model to the outside world via Flask app and api
- Build database to store users input for model retraining.

**Note:** app.py is running on debugging mode. This is to allow changes. If you want to put the model in production, make sure to set debugging to False.

### Pending Documentation ...

N.B: This project was build in Python 3.6, and uses _f-formating_, that might cause issues with lower Python version. lower python version will throw:

##### SyntaxError ERROR
``` f'Positive: With {pos_proba:.1%} Probability'```
 
If you want to use lower Python version, just git clone the project and change f-formating string to normal
.format() e.g.
```'Positive: With {:.1%} Probability'.format(pos_proba)```

### TODO:
- Gather users input for model retraining
- Rewrite the flask_app to actually do what it is suppose to do
- Grid search better parameter for partial_fit models
- A better tokenizer (remove places and peoples names)
- Clean code everywhere :)