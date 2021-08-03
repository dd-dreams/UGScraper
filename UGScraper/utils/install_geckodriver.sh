#!/bin/bash


# latest release of chromedriver
URL="https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz"

# downloaded
wget -q $URL

mv geckodriver-* geckodriver.zip

# extracting
tar -xf geckodriver.zip
rm geckodriver.zip
mv geckodriver ../

