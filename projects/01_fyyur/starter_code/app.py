# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm, Form
from forms import *
from flask_migrate import Migrate, MigrateCommand
from models import db, Show, Artist, Venue
from sqlalchemy import text

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db.app = app
db.init_app(app)
moment = Moment(app)
migrate = Migrate(app, db)
db.create_all()


# TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO: connect to a local postgresql database


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="EN")


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    sqlCitySate = text('select city,state from venues')
    resultCitySate = db.engine.execute(sqlCitySate)
    cities_states = {}

    for venue in resultCitySate:
        if venue[1] in cities_states:
            if venue[0] not in cities_states[venue[1]]:
                cities_states[venue[1]].append(venue[0])
        else:
            cities_states[venue[1]] = [venue[0]]

    venues = Venue.query.all()
    data = []
    for state in cities_states:
        for city in cities_states[state]:
            data.append({
                "state": state,
                "city": city,
                "venues": [{
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len([show for show in venue.shows if show.start_time > datetime.now()]),
                } for venue in venues if venue.city == city and venue.state == state]
            })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get("search_term")
    search = "%{}%".format(search_term)
    data = Venue.query.filter(Venue.name.like(search)).all()
    response = {
        "count": len(data),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len([show for show in venue.shows if show.start_time > datetime.now()]),
        } for venue in data]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = Venue.query.get_or_404(venue_id).format()
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        venue = Venue(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            genres=request.form.getlist(key='genres'),
            facebook_link=request.form.get('facebook_link'),
            image_link=request.form.get('image_link'),
        )
        venue.create()
        flash('Venue ' + request.form.get('name') + ' was successfully listed!')
    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    # on successful db insert, flash success
    # flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    Venue.query.get_or_404(venue_id).delete()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    data = Artist.query.all()

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # response = {
    #     "count": 1,
    #     "data": [{
    #         "id": 4,
    #         "name": "Guns N Petals",
    #         "num_upcoming_shows": 0,
    #     }]
    # }
    search_term = request.form.get('search_term')
    search = "%{}%".format(search_term)
    data = Artist.query.filter(Artist.name.like(search)).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    data = Artist.query.get_or_404(artist_id).format()
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)
    # artist = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    # }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get_or_404(artist_id)
    try:
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.address = request.form.get('address')
        artist.genres = request.form.getlist('genres')
        artist.facebook_link = request.form.get('facebook_link')
        artist.image_link = request.form.get('image_link')
        artist.create()
        flash('Artist ' + request.form.get('name') + ' was successfully updated!')
    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)

    form = VenueForm(obj=venue)

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    try:
        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.phone = request.form.get('phone')
        venue.address = request.form.get('address')
        venue.genres = request.form.getlist('genres')
        venue.facebook_link = request.form.get('facebook_link')
        venue.image_link = request.form.get('image_link')
        venue.create()
        flash('Venue ' + request.form.get('name') + ' was successfully updated!')
    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        artist = Artist(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            phone=request.form.get('phone'),
            genres=request.form.getlist('genres'),
            facebook_link=request.form.get('facebook_link'),
            image_link=request.form.get('image_link'),
        )
        artist.create()
        flash('Artist ' + request.form.get('name') + ' was successfully listed!')
    except Exception as e:
        print(sys.exc_info())
    finally:
        db.session.close()

    # on successful db insert, flash success
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    data = [{
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": "{}".format(show.start_time)
    } for show in Show.query.join(Artist).join(Venue).all()]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')
        sqlShowCreate = text(f"insert into shows (start_time, venue_id, artist_id) VALUES ('{start_time}', {venue_id}, {artist_id})")
        db.engine.execute(sqlShowCreate)

        # show = Show(
        #     artist_id=request.form.get('artist_id'),
        #     venue_id=request.form.get('venue_id'),
        #     start_time=request.form.get('start_time'),
        # )
        # show.create()
        flash('Show was successfully listed!')
    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    # on successful db insert, flash success
    # flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
