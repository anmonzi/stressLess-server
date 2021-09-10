# StressLess Platform API

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
1. Type this exact thing into the terminal to run the migrations and seed the database: `./seed_data.sh`

Now that your database is set up all you have to do is run the command:

```sh
python manage.py runserver
```

## StressLess ERD

Open the [StressLess database diagram](https://dbdiagram.io/d/6138eb35825b5b0146f95207) in the browser to view the tables and relationships for the database.

## Postman Request Collection

1. Open Postman
1. Click Import from the navbar
1. Choose the Link option
1. Paste in this URL:
    `https://www.getpostman.com/collections/c29b98258d312bf240b7`
1. Your should be prompted to import **StressLess Python API**.
1. Click the Import button to complete the process.

To test it out, expand the Profile sub-collection, double-click on Login and send the request. You should get a response back that looks like this.

```json
{
    "valid": true,
    "token": "9ba45f09651c5b0c404f37a2d2572c026c146690",
    "id": 5
}
```