#!/usr/bin/python3

from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import os
from constants.html_classes import *
from constants.other import CACHED_SITES
import modify_html

GET_HTML_COMMAND = "return document.documentElement.outerHTML"
SEARCH_URL = "https://www.ultimate-guitar.com/search.php?search_type=title&value="
DRIVER = None


def get_html(url, driver_location=None):
    global DRIVER

    # using selenium to run javascript scripts
    options = Options()
    options.headless = True
    options.add_argument("--incognito")  # even tho selenium creates a brand new profile, we want to be sure
    if DRIVER is None:
        try:
            if driver_location is None:  # if user didn't specify a webdriver, we will try to use one in path if have
                DRIVER = webdriver.Chrome(options=options)
            else:
                if '"' in driver_location:
                    driver_location = driver_location.replace('"', "")  # excluding ""
                DRIVER = webdriver.Chrome(executable_path=driver_location, options=options)
        except WebDriverException:  # if webdriver is not in path, it will throw an exception
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

        if type_element == CLASS:
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

    @staticmethod
    def get_rate(elem):
        return elem[1]

    def order_elements(self):
        """
        ordering elements by rating, highest to lowest

        :return: None
        """
        ordered = []


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
                ordered = sorted(ordered, key=self.get_rate, reverse=True)

        self.__elements = ordered

    def organize_songs(self):
        """

        :return: all songs
        """

        for song in self.__elements:
            link = song[0].find("a", class_=self.link_class, href=True)
            type_ = song[0].find("div", class_=self.type_class).text
            self.songs.append([link['href'], f"{link.text}_{song[1]}", song[1], type_])  # [link, name, rate, type]
        return self.songs

    def print_songs(self):
        songs = " " * 6
        self.remove_payed()  # just to be sure
        for index, song in enumerate(self.songs):
            songs += colored(f"[{index + 1}] ", 'yellow') + colored(f"{song[1].split('_')[0]}"
                                                                    f", {song[2]}, {song[3]}\n", 'red')
            songs += " " * 6
        return songs

    def get_song_name(self, index):
        """
        returns the song name by index

        :return: name
        """
        return self.songs[index][1]


class Chords:
    def __init__(self, soup, chords_class, name, artist):
        self.__soup = soup
        self.chords_class = chords_class
        self.name = (name.replace(' ', '_') + ".html").replace('"', '')
        self.artist = artist.replace('"', '')

    @staticmethod
    def add_basic_html(file, start_or_end):
        """
        function for adding some basic html tags to outputted html file

        :param file: file object
        :param start_or_end:

        :return:
        """
        if start_or_end:
            modify_html.add_basic(file, start_or_end)
            modify_html.center_smooth_html(file, start_or_end)
        else:
            modify_html.center_smooth_html(file, start_or_end)
            modify_html.add_basic(file, start_or_end)

    def output_chords(self):
        if not os.path.exists(CACHED_SITES):
            os.makedirs(CACHED_SITES)
        chords = self.__soup.find("section", class_=CHORDS_CLASS)
        chords_html = open(os.path.join(CACHED_SITES, self.name), "w")
        self.add_basic_html(chords_html, True)
        modify_html.add_button(chords_html)
        chords_html.write(str(chords))
        modify_html.add_autoscroll(chords_html)
        self.add_basic_html(chords_html, False)



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
