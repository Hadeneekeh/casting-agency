from flask_script import Manager
from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db, Movies, Actors

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# seed command
@manager.command
def seed():
    Movies(title='Crash Landing', release_date='2020/01/01').insert()
    Movies(title='Ghost and the Tout', release_date='2018/02/01').insert()

    Actors(name='James Bond', age=66, gender='male').insert()
    Actors(name='Basket Mouth', age=32, gender='male').insert()

if __name__ == '__main__':
    manager.run()