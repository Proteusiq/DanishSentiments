'''
TODO: Notes on How everything works
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

## views is placed after initialization of the application
from views import *

if __name__ == '__main__':
    app.run(debug=True)
