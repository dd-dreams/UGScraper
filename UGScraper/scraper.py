#!/usr/bin/python3

from termcolor import colored
from selenium import webdriver
from selenium.webdriver.firefox.options import Options, FirefoxProfile
from selenium.common.exceptions import WebDriverException
import os
from constants.html_classes import *

CLASS = "class"
GET_HTML_COMMAND = "return document.documentElement.outerHTML"
SEARCH_URL = "https://www.ultimate-guitar.com/search.php?search_type=title&value="
CACHED_SITES = "/../cached_sites/"
FIREFOX_PROFILE = "../firefox_profile"
DRIVER = None


def get_html(url, driver_location=None):
    global DRIVER

    # using selenium to run javascript scripts
    options = Options()
    if os.path.exists(f"{os.getcwd()}/{FIREFOX_PROFILE}"):  # checking if firefox_profile exists
        profile = FirefoxProfile(profile_directory=FIREFOX_PROFILE)
    else:
        profile = FirefoxProfile()
    options.headless = True
    if DRIVER is None:
        try:
            if driver_location is None:
                DRIVER = webdriver.Firefox(options=options, firefox_profile=profile)
            else:
                if '"' in driver_location:
                    driver_location = driver_location[1:-1]  # excluding ""
                DRIVER = webdriver.Firefox(executable_path=driver_location, options=options,
                                           firefox_profile=profile)
        except WebDriverException:
            return False

    DRIVER.get(url)
    source_code = DRIVER.execute_script(GET_HTML_COMMAND)
    return source_code


def get_driver():
    return DRIVER


class Scraper:
    def __init__(self, soup, song_class, rating_class, link_class, type_class, artist, song):
        self.__soup = soup
        self.__elements = []  # [element,]
        self.song_class = song_class
        self.rating_class = rating_class
        self.link_class = link_class
        self.type_class = type_class
        self.songs = []
        self.artist = artist
        self.song = song

    def get_elements(self):
        return self.__elements

    def get_songs(self):
        return self.songs

    def print_html(self):
        print(self.__soup.prettify())

    def find_elements(self, element, type_element):
        """
        this method will find all elements with a specific name

        :param element: name of element
        :param type_element: what type of element
        :return: all elements found with name (element)
        """

        if type_element == 'class':
            self.__elements = self.__soup.find_all("div", class_=element)
        return self.__elements

    # TODO add pro option
    def remove_payed(self):
        """
        this method will remove the official and payed tabs

        :return: None
        """
        for song in self.songs:
            # removing payed tabs
            text = song[3].lower()
            if "pro" == text or "official" == text or "guitar pro" == text:
                self.songs.remove(song)

    def order_elements(self):
        """
        ordering elements by rating, highest to lowest

        :return: None
        """
        ordered = []

        def get_rate(elem):
            return elem[1]

        for element in self.__elements:
            rate = element.find("div", class_=self.rating_class)  # getting the rating number
            if rate is None:
                continue
            else:
                rate = rate.text
            if "High" in rate:  # checking if its an "High quality" which is payed
                continue
            if ',' in rate:  # if its a thousand or more number, like 1,000
                rate = rate.replace(',', '')
            if rate == '' or rate == ' ':
                continue
            ordered.append((element, int(rate)))
            if len(ordered) > 1:
                ordered = sorted(ordered, key=get_rate, reverse=True)

        self.__elements = ordered

    def organize_songs(self):
        """

        :return: all songs
        """

        for song in self.__elements:
            link = song[0].find("a", class_=self.link_class, href=True)
            type_ = song[0].find("div", class_=self.type_class).text
            self.songs.append([link['href'], link.text, song[1], type_])  # [link, name, rate, type]
        return self.songs

    def print_songs(self):
        songs = " " * 6
        self.remove_payed()  # just to be sure
        for index, song in enumerate(self.songs):
            songs += colored(f"[{index}] ", 'yellow') + colored(f"{song[1]}, {song[2]}, {song[3]}\n", 'red')
            songs += " " * 6
        return songs


class Chords:
    def __init__(self, soup, chords_class, name):
        self.__soup = soup
        self.chords_class = chords_class
        self.name = name + ".html"

    def output_chords(self):
        path = os.getcwd() + CACHED_SITES
        if not os.path.exists(path):
            os.makedirs(path)
        chords = self.__soup.find("section", class_=CHORDS_CLASS)
        with open(os.path.join(path, self.name), "w") as chords_html:
            chords_html.write(str(chords))


def main(scraper):
    """

    :return: if found any songs, false if not, true if yes
    """
    scraper.find_elements(ALL_SONGS_CLASS, CLASS)
    scraper.order_elements()
    scraper.organize_songs()
    scraper.remove_payed()
    songs = scraper.get_songs()
    if len(songs) == 0:
        return False
    return True