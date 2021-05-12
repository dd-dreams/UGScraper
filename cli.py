#!/usr/bin/python3

from scraper import *
from bs4 import BeautifulSoup
import sys
from colorama import init
import argparse
import subprocess

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
"""

# commands
OPTIONS = "options"
SET = "set"
CLEAR = "clear"
HELP = "help"
SCRAPE = "scrape"
OUTPUT = "output"

LINK = None


def print_status(text, status=None):
    """
    prints colored texts
    """
    if status is None:
        print(SUCCESS_COLOR, colored(text, YELLOW))
    else:
        print(ERROR_COLOR, colored(text, YELLOW))


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
    path = os.getcwd() + "/cached_sites"
    file = os.path.join(path, name)
    return os.path.isfile(file)


def scrape_command():
    if SONG is None:
        print_status(NO_SONG_SET, ERROR_COLOR)
        return
    if ARTIST is None:
        print_status(NO_ARTIST_SET, ERROR_COLOR)
        return
    if check_in_cache(SONG):
        print_status(ALREADY_SCRAPED, ERROR_COLOR)
        return
    url = SEARCH_URL + SONG + ' ' + ARTIST
    print_status(FETCHING_RESULTS)
    source = get_html(url)
    scraper = Scraper(BeautifulSoup(source, "lxml"), ALL_SONGS_CLASS, RATING_CLASS_NAME, LINK_NAME_CLASS,
                      TYPE_CLASS, ARTIST, SONG)
    found = main(scraper)
    if not found:
        print_status(SONGS_NOT_FOUND, ERROR_COLOR)
        return
    else:
        print_status(SONGS_FOUND)
    chosen = choose_song(scraper)
    link = scraper.get_songs()[chosen][0]
    print_status(SUCCESS_SCRAPE)
    return link


def output_command(link, name):
    if link is None:
        print_status("No song to scrape from", ERROR_COLOR)
    elif check_in_cache(name):
        print_status(ALREADY_SCRAPED, ERROR_COLOR)
        return
    else:
        source = get_html(link)
        chords = Chords(BeautifulSoup(source, "lxml"), CHORDS_CLASS, name)
        chords.output_chords()
        print_status(SUCCESS_CHORDS)


def check_command(comm, whatset=None):
    """
    this func will check the command input

    :param comm: the command
    :param whatset: if the user chose a command to set some variable, this is what to set for
    :return:
    """
    global LINK, SONG

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
        LINK = scrape_command()
    elif comm == OUTPUT:
        output_command(LINK, SONG)
    else:
        print_status("Wrong input", ERROR_COLOR)


if __name__ == '__main__':
    init()  # sometimes the colors do not appear good on some platforms, init() fix it
    command = ""
    setvar = None
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--shell', help="Spawn a shell", required=True, metavar="True/False")
    parser.add_argument('-S', '--song', help="Provide song")
    parser.add_argument('-a', '--artist', help="Provide artist")
    parser.add_argument('-c', '--command', help="Run series of commands", metavar="[commands]")
    args = parser.parse_args()
    if args.shell.lower() == "true":
        try:
            while True:
                command = input(HOLDER).lower()
                if '=' in command:
                    command, setvar = command.split("=")
                if command == "exit" or command == "quit" or command == "bye":
                    print("bye")
                    break
                check_command(command, setvar)
        except KeyboardInterrupt:
            print("\nbye")
    else:
        pass
