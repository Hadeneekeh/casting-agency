import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import json

load_dotenv()

database_path = os.getenv('DATABASE_URL')
# database_path = 'postgresql://postgres:psql@localhost:5432/casting'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)
    release_date =  Column(DateTime(), nullable=False)

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
        }

    '''
    insert()
        inserts a new movie into the database
        the movie must have a unique title
        the movie must have a unique id or null id
        EXAMPLE
            movie = Movies(title=req_title, release_date=req_release_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a movie from the database
        the movie must exist in the database
        EXAMPLE
            movie = Movies.query.filter(Movies.id == id).one_or_none()
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a movie in the database
        the movie must exist in the database
        EXAMPLE
            movie = Movies.query.filter(Movies.id == id).one_or_none()
            movie.title = 'Sometime in Africa'
            movie.update()
    '''
    def update(self):
        db.session.commit()


'''
Actors
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    age = Column(Integer, unique=True, nullable=False)
    gender = Column(String, unique=True, nullable=False)

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'gender': self.gender,
        'age': self.age
        }

    '''
    insert()
        inserts a new actor into the database
        the actor must have a unique name
        the actor must have a unique id or null id
        EXAMPLE
            actor = Actors(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an actor from the database
        the actor must exist in the database
        EXAMPLE
            actor = Actors.query.filter(actors.id == id).one_or_none()
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an actor details in the database
        the actor must exist in the database
        EXAMPLE
            actor = Actors.query.filter(actors.id == id).one_or_none()
            actor.name = 'All Star'
            actor.update()
    '''
    def update(self):
        db.session.commit()
