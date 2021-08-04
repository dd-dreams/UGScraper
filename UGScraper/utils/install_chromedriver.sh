#!/bin/bash


# latest release of chromedriver
CHROME_VERSION="92"
URL="https://chromedriver.storage.googleapis.com/92.0.4515.43/chromedriver_linux64.zip"


# finding google chrome command
if [[ "$(command -v "google-chrome-stable" | wc -c)" != "0" ]]; then
    # getting version
    COMMAND=$(google-chrome-stable --version)
    COMMAND="${COMMAND:14:2}"
else
    COMMAND=$(google-chrome --version)
    COMMAND="${COMMAND:14:2}"
fi

# checking if user has latest chrome version
if [ $COMMAND == $CHROME_VERSION ]; then
    if ! [[ -e "chromedriver.zip" ]]; then
        wget -q $URL
        mv chromedriver_* chromedriver.zip
    fi
else
    echo "ERROR: You don't have the latest chrome version"
    exit
fi

# extracting
7z e -bso0 chromedriver.zip
rm chromedriver.zip
