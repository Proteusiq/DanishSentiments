# CLI Create and drop database
# e.g. python db_admin.py create 
import sys
from app import db

if sys.argv[1] =='create':
    input('We are going to create all db')
    db.create_all()
if sys.argv[1] == 'drop':
    input('We are going to drop all db')
    db.create_all()
if sys.argv[1] == 'drop' and sys.argv[2] == 'create':
    input('We are going to drop all and create all db')
    db.create_all()
    db.create_all()
    

    

