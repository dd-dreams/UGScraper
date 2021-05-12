# **Ultimate Guitar Scraper**

---

Ultimate Guitar Scraper is an MIT licensed project, which scrapes the site according to specifications, and get for you the chords.



## Features

---

- Search by song

- Search by artist
  
  

## Manual

---

You of-course need python, version>=3.7.

To start scraping you need to run cli.py, which interacts with the scraper.py.

Here is the help message when running cli.py -h/--help:

```
usage: cli.py [-h] -s True/False [-S SONG] [-a ARTIST] [-c [commands]]

Scrape Ultimate Guitar website with no tracking, fast and easy, and lightweight. You can use the shell provided with the program, or parse arguments and get instant
results. Enjoy!

optional arguments:
  -h, --help            show this help message and exit
  -s True/False, --shell True/False
                        Spawn a shell
  -S SONG, --song SONG  Provide song
  -a ARTIST, --artist ARTIST
                        Provide artist
  -c [commands], --command [commands]
                        Run series of commands
```

`-s/--shell` is specifying if you want to use the shell provided with the program,

or just pass args [still currently in development, only the shell is working].

`-S/--song` is for specifiying which song you want to search for (only when shell=False) [in development]. 

`-a/--artist` same as `-S` only for artist [in development].

`-c/--command` is for running series of command, while shell=True, and exists after [in development].

### Shell = TRUE

When shell = True (specified `-s/--shell true`), a "holder" will appear for you:

![holder.png](assets/holder.png)

You then can type commands, to get for you the chords.

When typing `help`, you will get a list of the current supported commands:

![help_msg.png](assets/help_msg.png)

**ATTENTION**: Currently you must specify song and artist, otherwise you get errors.



# Docs

---

The program is running with selenium to get the source code of the site, since I need javascript to be rendered.

Beautifulsoup is used for scraping.

The program is a bit heavy, that's why it can take some time to scrape.

So to solve it with the easy way, I did that everytime you search a song and scrape it, the chords will be cached in a folder.

On some computers if you run it multiple times, selenium can complain and say "No space left on device", since for some reason- the RAM is getting full :/.



# WARNING!!

---

I'm **<mark>not</mark>** responsible for **<mark>any</mark>** potential bad use of the program, it's just for **fun**, and for testing my programming skills. Please **do not** use it to harm.

# Contact

---

Currently, no contact service.
