from drafter import *
from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Movie:
    title: str
    genre: str
    rating: int
    length: int

@dataclass
class State:
    movies: list[Movie]
    favorite_movies: list[Movie]
    selected_genre: str
    selected_rating: int
    selected_length: str
    filtered_movies: list[Movie]

def create_movies()->list[Movie]:
    """Creates the list of available movies"""
    return [Movie("Toy Story", "Animation", 8, 81),
        Movie("Spider-Man: Into the Spider-Verse", "Action", 9, 117),
        Movie("The Incredibles", "Animation", 8, 115)]
assert_equal(len(create_movies()), 3)
assert_equal(create_movies()[0].title, "Toy Story")
assert_equal(create_movies()[1].title, "Spider-Man: Into the Spider-Verse")
assert_equal(create_movies()[2].title, "The Incredibles")


def make_state()-> State:
    """Creates the starting state"""
    return State(create_movies(), [], "Any", 0, "Any", [])
state = make_state()
assert_equal(len(state.movies), 3)
assert_equal(state.favorite_movies, [])
assert_equal(state.selected_genre, "Any")
assert_equal(state.selected_rating, 0)
assert_equal(state.selected_length, "Any")
assert_equal(state.filtered_movies, [])

@route
def index(state: State) -> Page:
    """Shows the home page."""
    return Page(state, [Header("Find a Movie"), "Find a movie to watch personalized to you", Button("Find Movies", "filter_movies"), Button("My Favorites", "favorites"), Button("About", "about")])
state = make_state()
assert_equal(type(index(state)), Page)

@route
def filter_movies(state: State) ->Page:
    """Shows the page where users select their filters."""
    rating_choice = "Any"
    if state.selected_rating != 0:
        rating_choice = str(state.selected_rating)
    return Page(state, [Header("Find a Movie"), "Enter a genre:", SelectBox("genre", ["Any", "Comedy", "Horror", "Action", "Romance", "Animation"], state.selected_genre),
        "Enter minimum rating (out of 10):", SelectBox("rating", ["Any", "1", "2", "3", "4", "5","6", "7", "8", "9", "10"], rating_choice),
        "Enter a length:", SelectBox("length", ["Any", "Under 90 minutes", "90-120 minutes", "Over 120 minutes"], state.selected_length),
        Button("Find Movies", "show_movies"),
        Button("Home", "index")])
state = make_state()
assert_equal(type(filter_movies(state)), Page)

@route
def show_movies(state: State, genre: str, rating: str,
                length: str) -> Page:
    """Finds movies that match the selected filters."""
    state.selected_genre = genre
    state.selected_length = length

    if rating == "Any":
        state.selected_rating = 0
    else:
        state.selected_rating = int(rating)

    state.filtered_movies = []

    for movie in state.movies:
        matches = True

        if state.selected_genre != "Any":
            if movie.genre != state.selected_genre:
                matches = False

        if state.selected_rating > 0:
            if movie.rating < state.selected_rating:
                matches = False

        if state.selected_length == "Under 90 minutes":
            if movie.length >= 90:
                matches = False

        elif state.selected_length == "90-120 minutes":
            if movie.length < 90 or movie.length > 120:
                matches = False

        elif state.selected_length == "Over 120 minutes":
            if movie.length <= 120:
                matches = False

        if matches:
            state.filtered_movies.append(movie)

    content = [
        Header("Movie Results"),
        "Here are the movies that match your preferences."
    ]

    if len(state.filtered_movies) == 0:
        content.append("No movies matched your filters.")

    else:
        for movie in state.filtered_movies:
            content.append(movie.title + " | " + movie.genre + " | Rating: " + str(movie.rating) +"/10 | " + str(movie.length) + " minutes")

            content.append(Button("Add to Favorites","add_favorite",[Argument("movie_title", movie.title)]))

    content.append(Button("Filter Again", "filter_movies"))
    content.append(Button("My Favorites", "favorites"))
    content.append(Button("Home", "index"))

    return Page(state, content)
state = make_state()
show_movies(state, "Any", "Any", "Any")
assert_equal(len(state.filtered_movies), 3)

@route
def favorites(state: State) -> Page:
    """Shows the saved movies"""
    content = [Header("My Favorite Movies"),"Here are the movies you have saved."]
    if len(state.favorite_movies) == 0:
        content.append("You have not added any favorites yet.")
    else:
        for movie in state.favorite_movies:
            content.append(movie.title + " | " + movie.genre + " | Rating: " + str(movie.rating) + "/10 | " + str(movie.length) + " minutes")
            content.append(Button("Remove from Favorites", "remove_favorite",[Argument("movie_title", movie.title)]))
    content.append(Button("Find More Movies", "filter_movies"))
    content.append(Button("Home", "index"))
    return Page(state, content)
state = make_state()
assert_equal(type(favorites(state)), Page)

@route
def add_favorite(state: State, movie_title: str) -> Page:
    """Adds a movie to the favorites list"""
    already_saved = False
    for movie in state.favorite_movies:
        if movie.title == movie_title:
            already_saved = True
    if not already_saved:
        for movie in state.movies:
            if movie.title == movie_title:
                state.favorite_movies.append(movie)

    return favorites(state)
state = make_state()
add_favorite(state, "Toy Story")
assert_equal(len(state.favorite_movies), 1)

@route
def remove_favorite(state: State, movie_title: str) -> Page:
    """Removes a movie from the favorites list"""
    remaining_favorites = []
    for movie in state.favorite_movies:
        if movie.title != movie_title:
            remaining_favorites.append(movie)

    state.favorite_movies = remaining_favorites

    return favorites(state)
state = make_state()
add_favorite(state, "Toy Story")
remove_favorite(state, "Toy Story")
assert_equal(len(state.favorite_movies), 0)


@route
def about(state: State) -> Page:
    """Shows info about the website"""
    return Page(state, [
        Header("About Movie Finder"), "Movie Finder helps people decide what movie to watch.", "Users can filter movies by genre, rating, and length.", "Users can also save their favorite movies.",
        Button("Find Movies", "filter_movies"),
        Button("Home", "index")])
state = make_state()
assert_equal(type(about(state)), Page)

start_server(make_state())
