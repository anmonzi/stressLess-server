# StressLess Platform API

StressLess is a habits tracking app designed to help high achieving individuals create better habits to tackle stress.

## Prerequisites

### Mac OS

```sh
brew install libtiff libjpeg webp little-cms2
```

### Linux (WSL)

```sh
sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
```

### Install apidoc

```sh
npm install apidoc -g
```

## Setup

1. Clone this repository and change to the directory in the terminal.
1. Run `pipenv shell`
1. Run `pipenv install`
1. In the server directory, type this exact thing into the terminal to run the migrations and seed the database: `./seed_data.sh`


Now that your database is set up all you have to do is run the command:

```sh
python manage.py runserver
```

1. In client directory, run `npm install` then run `npm start`

## Dependencies

StressLess Client, click [Here](https://github.com/anmonzi/stressLess-client)

## StressLess ERD

Open the [StressLess database diagram](https://dbdiagram.io/d/6138eb35825b5b0146f95207) in the browser to view the tables and relationships for the database.