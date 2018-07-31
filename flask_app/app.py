'''
Main Application: All routes are from views.py
views.py should only contain functions as we have 
a circular imports, app -> view -> app
db initialized and used in storage.py and views
run <python db_admin create> to create the table,
if not yet created 
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
