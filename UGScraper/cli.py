#!/usr/bin/python3

from scraper import *
from bs4 import BeautifulSoup
import sys
from colorama import init
import argparse
import subprocess
from constants.messages import *
from constants.other import CACHED_SITES, CHROMEDRIVER_LOCATION

HOLDER = colored("#>: ", 'red')
SONG = None
ARTIST = None
ERROR_COLOR = colored("[!]", 'red')
SUCCESS_COLOR = colored("[*]", 'blue')

# commands
OPTIONS = "options"
SET = "set"
CLEAR = "clear"
HELP = "help"
SCRAPE = "scrape"
OUTPUT = "output"
OPEN = "open"
CHROMEDRIVER = "chromedriver"

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


def open_command(path, browser=None):
    if os.path.isfile(path):
        if browser is None:
            subprocess.call(["bash", "utils/open_browser.sh", path])
        else:  # if open actually opened nothing, that means user didn't specify correctly the name of the browser
            subprocess.call(["bash", "utils/open_browser.sh", path, browser])
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
    return chosen - 1


def check_in_cache(name):
    name += ".html"
    file = os.path.join(CACHED_SITES, name)
    return os.path.isfile(file)


def scrape_command(chromedriver_location):
    """
    this func will be executed when the user chose to scrape the site
    meaning if he want to get the search results by specifying
    song and artist.

    :param chromedriver_location:
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
    source = get_html(url, chromedriver_location)  # receiving the html source code
    if source is False:
        print_status(NO_CHROMEDRIVER_ERROR, "red")
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
    link = scraper.get_songs()[chosen][0]  # get the link
    name = scraper.get_song_name(chosen)
    print_status(SUCCESS_SCRAPE)
    return link, name


def output_command(link, name, chromedriver_location):
    """
    this func will be executed when the user wants to output the chords,
    after choosing a song

    :param link: which song (link) to scrape
    :param name: what is the name of the song
    :param chromedriver_location: location for chromedriver (if specified)
    :return:
    """
    if link is None:
        print_status("No song to scrape from", ERROR_COLOR)
    elif check_in_cache(name):
        print_status(ALREADY_SCRAPED, ERROR_COLOR)
        return False
    else:
        print_status(OUTPUTTING_MSG)
        source = get_html(link, chromedriver_location)
        if source is False:
            print_status(NO_CHROMEDRIVER_ERROR, "red")
        chords = Chords(BeautifulSoup(source, "lxml"), CHORDS_CLASS, name, ARTIST)
        chords.output_chords()
        print_status(SUCCESS_CHORDS)


def get_path_current_song():
    """
    this is a function to get the current path of the current song

    :return: path
    """
    path = f"{CACHED_SITES}/{SONG}.html"
    return path


def check_command(comm, chromedriver_location, whatset=None):
    """
    this func will check the command input

    :param comm: the command
    :param whatset: if the user chose a command to set some variable, this is what to set for
    :param chromedriver_location: location for chromedriver
    :return:
    """
    global LINK
    name = None  # final song name

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
        LINK, name = scrape_command(chromedriver_location)
    elif comm == OUTPUT:
        output_command(LINK, name, chromedriver_location)
    elif comm == OPEN:
        path = get_path_current_song()
        open_command(path)
    else:
        print_status("Wrong input", ERROR_COLOR)


def using_args(song, artist, chromedriver_location):
    """

    :param song: song provided with an argument
    :param artist: artist provided with an argument
    :param chromedriver_location: location for chromedriver
    :return:
    """
    if song is None or artist is None:
        print_status(NO_SONG_OR_ARTIST, ERROR_COLOR)
        sys.exit(0)
    set_artist_song(song, artist)
    if chromedriver_location is None:
        chromedriver_location = os.getcwd() + '/' + CHROMEDRIVER_LOCATION
    link = scrape_command(chromedriver_location)
    if type(link) is tuple:
        name = link[1]
        link = link[0]
        output_command(link, name, chromedriver_location)
    get_driver().close()


def install_chromedriver():
    subprocess.call(["bash", "utils/install_chromedriver.sh"])


if __name__ == '__main__':
    init()  # sometimes the colors do not appear good on some platforms, init() fix it
    value = None
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--shell', help="Spawn a shell", action="store_true")
    parser.add_argument('-S', '--song', help="Provide song")
    parser.add_argument('-a', '--artist', help="Provide artist")
    parser.add_argument('-o', '--open', help="Open HTML file in browser after scraped", action="store_true")
    parser.add_argument('--webdriver', help="Specify webdriver")
    parser.add_argument('-b', '--browser', help="Specify browser (default is Chrome)")
    args = parser.parse_args()

    # if no args supplied, display help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    # check if chromedriver exists
    if not os.path.exists(CHROMEDRIVER) and args.webdriver is None:
        print_status(INSTALLING_CHROMEDRIVER)
        install_chromedriver()

    if args.shell:
        try:
            while True:
                command = input(HOLDER)
                if '=' in command:
                    command, value = command.split("=")
                    command = command.lower()
                if command == "exit" or command == "quit" or command == "bye":
                    print("bye")
                    if DRIVER is not None:
                        DRIVER.close()
                    break
                check_command(command, os.getcwd() + '/' + CHROMEDRIVER_LOCATION, value)
        except KeyboardInterrupt:
            if DRIVER is not None:
                DRIVER.close()
            print("\nbye")
    else:
        using_args(args.song, args.artist, args.webdriver)
        if args.open:  # if the user wants to open the chords html after the scrape
            path = get_path_current_song()
            open_command(path)
