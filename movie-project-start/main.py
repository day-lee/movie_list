from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

#CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

API_KEY = "814409d5db6882438b9cd579f376406c"

#CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250))

    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(250), unique=True, nullable=False)
    # year = db.Column(db.Integer, unique=True, nullable=False)
    # description = db.Column(db.String(500), unique=True, nullable=False)
    # rating = db.Column(db.Float, unique=True, nullable=False)
    # ranking = db.Column(db.Integer, unique=True, nullable=False)
    # review = db.Column(db.String(250), unique=True, nullable=False)
    # img_url = db.Column(db.String(250), unique=True, nullable=False)

def __init__(self,id, title, year, description, rating, ranking, review, img_url):
   self.id = id
   self.title = title
   self.author = year
   self.description = description
   self.rating = rating
   self.ranking = ranking
   self.review = review
   self.img_url = img_url
#Optional: this will allow each book object to be identified by its title when printed.
def __repr__(self):
    return f'<Movie{self.title}>'
db.create_all()

##CREATE RECORD
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


class UpdateForm(FlaskForm):
    rating = StringField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit')

#ADD NEW MOVIE
class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    """Returns a list of objects from DB and Passes data to template"""

    all_movies = Movie.query.order_by(Movie.rating).all() # returns a list holding objs
        # all_movies = Movie.query.all()
    print(all_movies) #[<Movie 3>, <Movie 1>, <Movie 2>]
    rank = 10
    for movie in all_movies:
        movie.ranking = rank
        rank -= 1
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)

@app.route("/edit", methods=["GET", "POST"])
def update():
    """GET: (before)  to render to specific movie's editing page"""
    """POST(Validated): (after) Updates the rating and Redirects to home to show a new rating"""
    form = UpdateForm()
    movie_id = request.args.get("id")
    movie_to_update = Movie.query.get(movie_id)

    if form.validate_on_submit():
        movie_to_update.rating = form.rating.data #get hold of input form-data
        movie_to_update.review = form.review.data
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("edit.html", movie=movie_to_update, form=form)

@app.route("/delete")
def delete():
    """Deletes the movie from the list"""
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET", "POST"])
def add():
    """GET: (before) Returns 'add' template to get input data """
    """POST: (validated) Gets hold of input data, Calls API and Updates data to home"""

    #GET 'TITLE' FROM INPUT
    form = AddForm()
    title = form.title.data

    #GET DATA FROM API AND PROVIDE A LIST TO SELECT
    if form.validate_on_submit():
        #Select the movie
        parameters = {
            "api_key": API_KEY,
            "query": title,
        }
        response = requests.get("https://api.themoviedb.org/3/search/movie", params=parameters)
        response.raise_for_status()
        data = response.json()
        result = data['results']
        return render_template("select.html", data=result)  # GET: getting input from html form

    return render_template("add.html", form=form) #GET: getting input from html form


@app.route("/find")
def find():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        parameters = {
            "api_key": API_KEY
        }
        detail_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_api_id}", params=parameters)
        detail_response.raise_for_status()

        detail_data = detail_response.json()

        #CREATE RECORD
        new_movie = Movie(
            title=detail_data['title'],
            year=detail_data['release_date'].split("-")[0],
            img_url=f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/{detail_data['poster_path']}",
            description=detail_data['overview']
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('update', id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
