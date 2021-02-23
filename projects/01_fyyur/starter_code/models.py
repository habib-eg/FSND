from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
# Show = db.Table('Show',
#     db.Column('start_time', DateTime, nullable=False),
#     db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), nullable=False, primary_key=True),
#     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), nullable=False, primary_key=True),
# )


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    artist = db.relationship("Artist", backref="artist", lazy=True)
    venue = db.relationship("Venue", backref="venue", lazy=True)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.JSON)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500),
                           default="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")
    facebook_link = db.Column(db.String(120))
    shows = db.relationship(Show, lazy=True)

    def format(self):
        past_shows = []
        upcoming_shows = []
        for show in self.shows:
            formated = {
                "artist_id": show.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": "{}".format(show.start_time),
            }
            if show.start_time > datetime.now():
                upcoming_shows.append(formated)
            else:
                past_shows.append(formated)

        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": "self.website",
            "facebook_link": self.facebook_link,
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": self.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.JSON)
    image_link = db.Column(db.String(500), default="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")
    facebook_link = db.Column(db.String(120))
    shows = db.relationship("Show", lazy=True)

    def format(self):
        past_shows = []
        upcoming_shows = []
        for show in self.shows:
            formated = {
                "artist_id": show.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": "{}".format(show.start_time),
            }
            if show.start_time > datetime.now():
                upcoming_shows.append(formated)
            else:
                past_shows.append(formated)

        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "seeking_venue": False,
            "image_link": self.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
