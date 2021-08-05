#!/bin/sh


# latest release of chromedriver
URL="https://chromedriver.storage.googleapis.com/92.0.4515.43/chromedriver_linux64.zip"

wget -q $URL
mv chromedriver_*.zip chromedriver.zip

# extracting
7z e -bso0 chromedriver.zip
rm chromedriver.zip
mv chromedriver ../
