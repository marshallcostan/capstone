import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

# database_name = "capstone"
# database_path = 'postgres://marshall@localhost:5432/{}'.format(database_name)
# database_path = os.environ.get('DATABASE_URL')
database_path = "postgres://udjyckurdsxnhd:9e2f85b5f6ecf8cbbdf079cae6ad9f6d0f1a658bf8d091a33b9331b0deeb5b3b@ec2-52-5-176-53.compute-1.amazonaws.com:5432/ddvb311svjnhr"


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def drop_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()


casting = db.Table('casting', Column('movie_id', db.Integer, db.ForeignKey('Movies.id')),
                   Column('actor_id', db.Integer, db.ForeignKey('Actors.id'))
                   )


class Actor(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    age = Column(db.Integer)
    gender = Column(String(120))
    movies = db.relationship('Movie', secondary=casting)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.format_movies_per_actor() for movie in self.movies]
        }

    def format_actors_per_movie(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(db.DateTime)
    cast = db.relationship('Actor', secondary=casting)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': [actor.format_actors_per_movie() for actor in self.cast]
        }

    def format_movies_per_actor(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }






