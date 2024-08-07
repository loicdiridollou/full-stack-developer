# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
import sys
from datetime import datetime
from logging import FileHandler, Formatter
from typing import cast

import dateutil.parser
from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from forms import ArtistForm, ShowForm, VenueForm

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))


class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))

    # DONETODO: implement any missing fields, as a database migration using Flask-Migrate


# DONETODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(
        db.Integer, db.ForeignKey("venue.id"), nullable=False
    )  # many-to-many
    artist_id = db.Column(
        db.Integer, db.ForeignKey("artist.id"), nullable=False
    )  # many-to-many
    date_show = db.Column(db.DateTime())


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    artists = Artist.query.order_by(Artist.id.desc()).limit(3)
    data = []
    for artist in artists:
        data.append({"id": artist.id, "name": artist.name})

    return render_template("pages/home.html", artists=data)


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # num_shows should be aggregated based on number of upcoming shows per venue.

    cities = []
    for venue in Venue.query.all():
        if {"city": venue.city, "state": venue.state} not in cities:
            cities.append({"city": venue.city, "state": venue.state})

    data = []
    for city in cities:
        venues = Venue.query.filter(
            Venue.state == city["state"], Venue.city == city["city"]
        ).all()
        tab = []
        for venue in venues:
            num_shows = Show.query.filter(
                Show.venue_id == 1, Show.date_show >= datetime.now()
            ).count()
            tab.append(
                {"id": venue.id, "name": venue.name, "num_upcoming_shows": num_shows}
            )
        data.append({"city": city["city"], "state": city["state"], "venues": tab})

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    tab = []
    results = Venue.query.filter(
        Venue.name.like(f"%{request.form.get("search_term")}%")
    )
    for result in results:
        count = Show.query.filter(
            Show.venue_id == result.id, Show.date_show >= datetime.now()
        ).count()
        tab.append({"id": result.id, "name": result.name, "num_upcoming_shows": count})

    response = {"count": len(tab), "data": tab}

    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id

    venue = Venue.query.filter(Venue.id == venue_id).one()
    past_shows = Show.query.filter(
        Show.venue_id == venue_id, Show.date_show < datetime.now()
    )
    tab = []
    for show in past_shows:
        artist = Artist.query.filter(Artist.id == show.artist_id).one()
        tab.append(
            {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": str(show.date_show),
            }
        )
    past_shows = tab

    future_shows = Show.query.filter(
        Show.venue_id == venue_id, Show.date_show >= datetime.now()
    )
    tab = []
    for show in future_shows:
        artist = Artist.query.filter(Artist.id == show.artist_id).one()
        tab.append(
            {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": str(show.date_show),
            }
        )
    future_shows = tab

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(","),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": future_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(future_shows),
    }

    # print(data['genres'])

    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    error = False
    try:
        name = request.form["name"]
        genres = ",".join(request.form.getlist("genres"))
        city = request.form["city"]
        address = request.form["address"]
        state = request.form["state"]
        phone = request.form["phone"]
        fb_link = request.form["facebook_link"]
        img_link = request.form["image_link"]
        seeking_talent = request.form["seeking_talent"] == "Yes"
        seeking_description = request.form["seeking_description"]
        website_link = request.form["website_link"]

        venue = Venue(
            name=name,
            address=address,
            city=city,
            state=state,
            phone=phone,
            genres=genres,
            facebook_link=fb_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description,
            image_link=img_link,
            website_link=website_link,
        )
        db.session.add(venue)
        db.session.commit()
    except:  # noqa: E722
        error = True
        db.session.rollback()
        flash(
            "An error occurred. Venue " + request.form["name"] + " could not be listed."
        )
    finally:
        # on successful db insert, flash success
        if not error:
            flash("Venue " + request.form["name"] + " was successfully listed!")
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    error = False
    try:
        shows = Show.query.filter(Show.venue_id == venue_id)
        for show in shows:
            db.session.delete(show)
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except ():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({"success": True})


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []
    for artist in artists:
        data.append({"id": artist.id, "name": artist.name})

    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    tab = []
    results = Artist.query.filter(
        Artist.name.like(f"%{request.form.get("search_term")}%")
    )
    for result in results:
        tab.append({"id": result.id, "name": result.name})

    response = {"count": len(tab), "data": tab}

    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    artist = cast(Artist, Artist.query.get(artist_id))

    past_shows = Show.query.filter(
        Show.artist_id == artist_id, Show.date_show < datetime.now()
    )
    tab = []
    for show in past_shows:
        venue = Venue.query.filter(Venue.id == show.venue_id).one()
        tab.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.date_show),
            }
        )
    past_shows = tab

    future_shows = Show.query.filter(
        Show.artist_id == artist_id, Show.date_show >= datetime.now()
    )
    tab = []
    for show in future_shows:
        venue = Venue.query.filter(Venue.id == show.venue_id).one()
        tab.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.date_show),
            }
        )
    future_shows = tab

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(","),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": future_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(future_shows),
    }

    print(data["genres"])

    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter(Artist.id == artist_id).one()

    artist = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(","),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    try:
        artist = Artist.query.filter(Artist.id == artist_id).one()

        artist.name = request.form["name"]
        artist.genres = ",".join(request.form.getlist("genres"))
        artist.city = request.form["city"]
        artist.state = request.form["state"]
        artist.phone = request.form["phone"]
        artist.facebook_link = (
            ""
            if request.form["facebook_link"] == "None"
            else request.form["facebook_link"]
        )
        artist.seeking_venue = True if request.form["seeking_venue"] == "Yes" else False
        artist.seeking_description = (
            ""
            if request.form["seeking_description"] == "None"
            else request.form["seeking_description"]
        )
        artist.image_link = request.form["image_link"]
        artist.website_link = request.form["website_link"]

        db.session.commit()
    except:  # noqa: E722
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.filter(Venue.id == venue_id).one()

    venue = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(","),
        "city": venue.city,
        "state": venue.state,
        "address": venue.address,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
    }

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    error = False
    try:
        venue = Venue.query.filter(Venue.id == venue_id).one()

        print(request.form.getlist("genres"))
        venue.name = request.form["name"]
        venue.genres = ",".join(request.form.getlist("genres"))
        venue.city = request.form["city"]
        venue.state = request.form["state"]
        venue.phone = request.form["phone"]
        venue.facebook_link = request.form["facebook_link"]
        venue.seeking_talent = request.form["seeking_talent"] == "Yes"
        venue.seeking_description = (
            ""
            if request.form["seeking_description"] == "None"
            else request.form["seeking_description"]
        )
        venue.image_link = request.form["image_link"]
        venue.website_link = request.form["website_link"]

        db.session.commit()
    except:  # noqa: E722
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    try:
        name = request.form["name"]
        genres = ",".join(request.form.getlist("genres"))
        city = request.form["city"]
        state = request.form["state"]
        phone = request.form["phone"]
        fb_link = request.form["facebook_link"]
        website_link = request.form["website_link"]
        img_link = request.form["image_link"]
        seeking_venue = request.form["seeking_venue"] == "Yes"
        seeking_description = request.form["seeking_description"]

        artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            genres=genres,
            image_link=img_link,
            facebook_link=fb_link,
            website_link=website_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )

        db.session.add(artist)
        db.session.commit()

    except:  # noqa: E722
        db.session.rollback()
        print(sys.exc_info())

    finally:
        # on successful db insert, flash success
        flash("Artist " + request.form["name"] + " was successfully listed!")

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # DONETODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    shows = Show.query.all()
    data = []
    for show in shows:
        artist = Artist.query.filter(Artist.id == show.artist_id).one()
        venue = Venue.query.filter(Venue.id == show.venue_id).one()
        data.append(
            {
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": str(show.date_show),
            }
        )

    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    # error = False
    try:
        artist = request.form["artist_id"]
        venue = request.form["venue_id"]
        date_show = request.form["start_time"]

        show = Show(artist_id=artist, venue_id=venue, date_show=date_show)

        db.session.add(show)
        db.session.commit()

    except:  # noqa: E722
        db.session.rollback()
        print(sys.exc_info())

    finally:

        # on successful db insert, flash success
        flash("Show was successfully listed!")
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
