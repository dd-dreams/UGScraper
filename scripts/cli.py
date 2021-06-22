#!/usr/bin/python3

from scraper import *
from bs4 import BeautifulSoup
import sys
from colorama import init
import argparse
import subprocess
import webbrowser

HOLDER = colored("#>: ", 'red')
SONG = None
ARTIST = None

# Messages
ERROR_COLOR = colored("[!]", 'red')
SUCCESS_COLOR = colored("[*]", 'blue')
FINDING_SONGS = "Finding songs..."
SONGS_NOT_FOUND = "Songs have not been found. Make sure you typed the song currectly."
SONGS_FOUND = "Songs have been found. Showing results..."
FETCHING_RESULTS = "Fetching results"
NO_SONG_SET = "No song to search"
NO_ARTIST_SET = "No specified artist"
SUCCESS_SCRAPE = "Successfully scraped"
SUCCESS_CHORDS = "Successfully outputed chords"
ALREADY_SCRAPED = "You already scraped this song. Check in cached_sites folder."
OUTPUTING_MSG = "Outputing chords"
FILE_NOT_EXIST = "You didn't scrape or output, try again after you did."
DESCRIPTION = """
Scrape Ultimate Guitar website with no tracking, fast and easy, and lightweight.
You can use the shell provided with the program, or parse arguments and get instant results.
Enjoy!

"""
HELP_MSG = """song=, specifiy song
artist=, specifiy artist
scrape, scrape the website
options, show current options
output, output the chords
bye/exit/quit, exits the program
open, opens the HTML file after being scraped
"""
NO_GECKODRIVER_ERROR = "No geckodriver was found. Specify he's location by using --geckodriver"

# commands
OPTIONS = "options"
SET = "set"
CLEAR = "clear"
HELP = "help"
SCRAPE = "scrape"
OUTPUT = "output"
OPEN = "open"
GECKODRIVER = "geckodriver"
GECKODRIVER_LOCATION = None

LINK = None


def print_status(text, status=None):
    """
    prints colored texts
    """
    if status is None:
        print(SUCCESS_COLOR, colored(text, 'yellow'))
    else:
        print(ERROR_COLOR, colored(text, 'yellow'))


def print_options():
    """
    this func will print the current options that have been set

    :return:
    """
    print("Song =", SONG)
    print("Artist =", ARTIST)
    print("Chosen link:", LINK)


def help_command():
    print(HELP_MSG)


def clear_command():
    platform = sys.platform
    if platform == "win32":
        subprocess.call("cls")
    else:
        subprocess.call("clear")


def open_command(path):
    if os.path.isfile(path):
        webbrowser.open(path)
    else:
        print_status(FILE_NOT_EXIST, ERROR_COLOR)


def set_artist_song(song=None, artist=None):
    global SONG, ARTIST
    if song is not None:
        SONG = song
    if artist is not None:
        ARTIST = artist


def choose_song(scraper):
    print(scraper.print_songs())
    chosen = int(input("Choose song: "))
    return chosen


def check_in_cache(name):
    name += ".html"
    path = os.getcwd() + CACHED_SITES
    file = os.path.join(path, name)
    return os.path.isfile(file)


def scrape_command(geckodriver_location):
    """
    this func will be executed when the user chose to scrape the site
    meaning if he want to get the search results by specifying
    song and artist.

    :return: if the was an error
    """
    if SONG is None:
        print_status(NO_SONG_SET, ERROR_COLOR)
        return False
    if ARTIST is None:
        print_status(NO_ARTIST_SET, ERROR_COLOR)
        return False
    if check_in_cache(SONG):
        print_status(ALREADY_SCRAPED, ERROR_COLOR)
        return False
    url = SEARCH_URL + SONG + ' ' + ARTIST  # constructing the html, which get the search-results
    print_status(FETCHING_RESULTS)
    source = get_html(url, geckodriver_location)  # receiving the html source code
    if source is False:
        print_status(NO_GECKODRIVER_ERROR, "red")
        return False
    scraper = Scraper(BeautifulSoup(source, "lxml"), ALL_SONGS_CLASS, RATING_CLASS_NAME, LINK_NAME_CLASS,
                      TYPE_CLASS, ARTIST, SONG)
    found = main(scraper)  # scraping, returns if songs have been found or not
    if not found:
        print_status(SONGS_NOT_FOUND, ERROR_COLOR)
        return
    else:
        print_status(SONGS_FOUND)
    chosen = choose_song(scraper)  # if there is multiple versions
    link = scraper.get_songs()[chosen][0]  # get the song version, and his Beautifulsoup object
    print_status(SUCCESS_SCRAPE)
    return link


def output_command(link, name, geckodriver_location):
    """
    this func will be executed when the user wants to output the chords,
    after choosing a song

    :param link: which song (link) to scrape
    :param name: what is the name of the song
    :param geckodriver_location: location for geckodriver (if specified)
    :return:
    """
    if link is None:
        print_status("No song to scrape from", ERROR_COLOR)
    elif check_in_cache(name):
        print_status(ALREADY_SCRAPED, ERROR_COLOR)
        return False
    else:
        print_status(OUTPUTING_MSG)
        source = get_html(link, geckodriver_location)
        if source is False:
            print_status(NO_GECKODRIVER_ERROR, "red")
        chords = Chords(BeautifulSoup(source, "lxml"), CHORDS_CLASS, name)
        chords.output_chords()
        print_status(SUCCESS_CHORDS)


def get_path_current_song():
    """
    this is a function to get the current path of the current song

    :return: path
    """
    path = os.getcwd() + f"{CACHED_SITES}/{SONG}.html"
    return path


def check_command(comm, geckodriver_location, whatset=None):
    """
    this func will check the command input

    :param comm: the command
    :param whatset: if the user chose a command to set some variable, this is what to set for
    :param geckodriver_location: location for geckodriver
    :return:
    """
    global LINK, SONG, GECKODRIVER_LOCATION

    if comm == OPTIONS:
        print_options()
    elif comm == CLEAR:
        clear_command()
    elif comm == HELP:
        help_command()
    elif comm == "song":
        set_artist_song(song=whatset)
    elif comm == "artist":
        set_artist_song(artist=whatset)
    elif comm == SCRAPE:
        LINK = scrape_command(geckodriver_location)
    elif comm == OUTPUT:
        output_command(LINK, SONG, geckodriver_location)
    elif comm == OPEN:
        path = get_path_current_song()
        open_command(path)
    else:
        print_status("Wrong input", ERROR_COLOR)


def using_args(song, artist, geckodriver_location):
    """

    :param song: song provided with an argument
    :param artist: artist provided with an argument
    :param geckodriver_location: location for geckodriver
    :return:
    """
    if song is None or artist is None:
        print_status("No song or artist provided", ERROR_COLOR)
        sys.exit(0)
    set_artist_song(song, artist)
    link = scrape_command(geckodriver_location)
    if link:
        output_command(link, song, geckodriver_location)
    else:
        return
    DRIVER.close()


if __name__ == '__main__':
    init()  # sometimes the colors do not appear good on some platforms, init() fix it
    command = ""
    setvar = None
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--shell', help="Spawn a shell", action="store_true")
    parser.add_argument('-S', '--song', help="Provide song")
    parser.add_argument('-a', '--artist', help="Provide artist")
    parser.add_argument('-o', '--open', help="Open HTML file in browser after scraped", action="store_true")
    parser.add_argument("--geckodriver", help="Specify geckodriver")
    args = parser.parse_args()
    GECKODRIVER_LOCATION = args.geckodriver
    if args.shell:
        try:
            while True:
                command = input(HOLDER)
                if '=' in command:
                    command, setvar = command.split("=")
                    command = command.lower()
                if command == "exit" or command == "quit" or command == "bye":
                    print("bye")
                    if DRIVER is not None:
                        DRIVER.close()
                    break
                check_command(command, GECKODRIVER_LOCATION, setvar)
        except KeyboardInterrupt:
            print("\nbye")
    else:
        using_args(args.song, args.artist, args.geckodriver)
        if args.open:
            path = get_path_current_song()
            open_command(path)
