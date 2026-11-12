from drafter import *
from dataclasses import dataclass
start_server()

set_website_title("Corgi Cafe")
set_site_information(
    author="Grayson",
    description="Find a movie based on preferences",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)


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


def create_movies() -> list[Movie]:
    """Creates the available movies."""
    return [
        Movie("Toy Story", "Animation", 8, 81),
        Movie("Spider-Man: Into the Spider-Verse", "Action", 9, 117),
        Movie("The Incredibles", "Animation", 8, 115),
        Movie("Finding Nemo", "Animation", 8, 100),
        Movie("The Dark Knight", "Action", 9, 152),
        Movie("The Notebook", "Romance", 7, 123),
        Movie("Home Alone", "Comedy", 7, 103),
        Movie("A Quiet Place", "Horror", 8, 90)
    ]


def make_state() -> State:
    """Creates the starting state."""
    return State(create_movies(), [], "Any", 0, "Any", [])


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Movie Finder"),
        "Find a movie to watch!",
        Button("Find Movies", "filter_movies"),
        Button("My Favorites", "favorites")
    ])


@route
def filter_movies(state: State) -> Page:
    return Page(state, [
        Header("Find a Movie"),
        "Choose a genre:",
        SelectBox("selected_genre", [
            "Any", "Comedy", "Horror", "Action", "Romance", "Animation"
        ]),
        "Choose a minimum rating:",
        SelectBox("selected_rating", [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
        ]),
        "Choose a length:",
        SelectBox("selected_length", [
            "Any", "Under 90", "90 to 120", "Over 120"
        ]),
        Button("Find Movies", "show_movies")
    ])


@route
def show_movies(state: State, selected_genre: str,
                selected_rating: str, selected_length: str) -> Page:
    state.selected_genre = selected_genre
    state.selected_rating = int(selected_rating)
    state.selected_length = selected_length
    state.filtered_movies = []

    for movie in state.movies:
        if selected_genre == "Any" or movie.genre == selected_genre:
            if movie.rating >= int(selected_rating):
                if selected_length == "Any":
                    state.filtered_movies.append(movie)
                elif selected_length == "Under 90" and movie.length < 90:
                    state.filtered_movies.append(movie)
                elif selected_length == "90 to 120" and 90 <= movie.length <= 120:
                    state.filtered_movies.append(movie)
                elif selected_length == "Over 120" and movie.length > 120:
                    state.filtered_movies.append(movie)

    contents = [
        Header("Movie Results")
    ]

    if len(state.filtered_movies) == 0:
        contents.append("No movies found.")
    else:
        for movie in state.filtered_movies:
            contents.append(movie.title)
            contents.append("Genre: " + movie.genre)
            contents.append("Rating: " + str(movie.rating) + "/10")
            contents.append("Length: " + str(movie.length) + " minutes")
            contents.append(Button("Add to Favorites", "add_favorite", movie.title))

    contents.append(Button("Back to Filters", "filter_movies"))
    contents.append(Button("Home", "index"))

    return Page(state, contents)


@route
def add_favorite(state: State, title: str) -> Page:
    for movie in state.movies:
        if movie.title == title:
            if movie not in state.favorite_movies:
                state.favorite_movies.append(movie)

    return favorites(state)


@route
def favorites(state: State) -> Page:
    contents = [Header("My Favorites")]

    if len(state.favorite_movies) == 0:
        contents.append("You have no favorite movies yet.")
    else:
        for movie in state.favorite_movies:
            contents.append(movie.title)
            contents.append("Genre: " + movie.genre)
            contents.append("Rating: " + str(movie.rating) + "/10")
            contents.append("Length: " + str(movie.length) + " minutes")
            contents.append(Button("Remove Favorite", "remove_favorite", movie.title))

    contents.append(Button("Find Movies", "filter_movies"))
    contents.append(Button("Home", "index"))

    return Page(state, contents)


@route
def remove_favorite(state: State, title: str) -> Page:
    new_favorites = []

    for movie in state.favorite_movies:
        if movie.title != title:
            new_favorites.append(movie)

    state.favorite_movies = new_favorites
    return favorites(state)


start_server(make_state())
