from drafter import *
from dataclasses import dataclass

set_website_title("Corgi Cafe")
set_site_information(
    author="Your Name",
    description="Order snacks for very good dogs.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Movie:
    title:str
    genre:str
    rating:int
    length:int
    
@dataclass
class State:
    movies: list[Movie]
    favorite_movies: list[Movie]
    selected_genre:str
    selected_rating:int
    selected_length:int
    filtered_movies:list[Movie]
    
def create_movies()->list[Movie]:
    """Creates the list of aviable movies on the wedsite"""
    return [Movie("Toy Story", "Animation", 8, 81),
        Movie("Spider-Man: Into the Spider-Verse", "Action", 9, 117),
        Movie("The Incredibles", "Animation", 8, 115)]
    
def make_state() -> State:
    """Starting state for the website"""
    return State(create_movies(),[],"Any", 0, 0, [])

@route
def index (state:State) -> Page:
    """show the home page"""
    return Page(state, [Header("Movie Finder"), "Find a movie to watch", button("Find movies","filter_movies"), button("My favorites", "favorites"), button("About", "about")])
    
@route
def filter_movies(state:State)->Page:
    """shows the page where the filtered movies are"""
    rating_choice = "Any"
    if state.selected_rating != 0:
        rating_choice = str(state.selected_rating)
    return Page(state, [Header("Find a movie"), "Enter a genre:", SelectBox("genre", ["Any", "Comedy", "Horror", "Action", "Romance", "Animation"], state.selected_genre),
        "Enter minimun rating (Out of 10):", SelectBox("rating", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], rating_choice),
        "Enter a length", SelectBox("length", ["Any", "Under 90","90 to 120","Over 120"], state.select_length),
        Button("Find Movies", "show_movies"),
        Button("Home", "index")])
