# Osoti-Small Book-A-Meal Application

[![codecov](https://codecov.io/gh/coosoti/Osoti-Small/branch/master/graph/badge.svg)](https://codecov.io/gh/coosoti/Osoti-Small) [![Build Status](https://travis-ci.org/coosoti/Osoti-Small.svg?branch=feature-order-meal-157333125)](https://travis-ci.org/coosoti/Osoti-Small) [![Maintainability](https://api.codeclimate.com/v1/badges/ed4591c861e746bda4cd/maintainability)](https://codeclimate.com/github/coosoti/Osoti-Small/maintainability) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6fffebf6668e44a1b7a7dba7b77d71c7)](https://www.codacy.com/app/coosoti/Osoti-Small?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=coosoti/Osoti-Small&amp;utm_campaign=Badge_Grade)

## Project Introduction

Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat.

Check the API docs at [this link](https://osoti-small.herokuapp.com/docs#/) 

### P.S
**Note**: The UI for the project is hosted on github. [See](https://coosoti.github.io/Osoti-Small/).

**Note**: The project manager in use is PivotalTracker.[See](https://www.pivotaltracker.com/n/projects/2165720)

## Installation


### Set up the environment

This API is built on top Flask python web framework.

### Run it on Local Machine

Clone the repository

```sh
git clone https://github.com/coosoti/Osoti-Small.git

```

Checkout into more recent branch 

```sh
git checkout chore-157339779-final-cleanup 
```

Create a virtualenv 
```sh
cd Osoti-Small
```

On Linux

```sh
virtualenv env -p /usr/bin/python3.6
```

On windows

```sh
virtualenv env -m python3.6
```

Activate virtual environment

On Linux

```sh
source env/bin/activate
```

On windows

```sh
env\Scripts\activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Add environment variable settings:

#### You can either use `.env` configuration file:

* Create a file name it `.env` with the following contents

```con
MODE=development
SECRET_KEY=secret_key
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

**OR**


On Windows

```powershell
SET SECRET_KEY=secret_key
```

```powershell
SET MODE=development
```

```powershell
SET DEBUG=True
```

```powershell
SET DEBUG=True
```

On Linux

```sh
export MODE=development
```

```sh
export SECRET_KEY=secret_key
```

```sh
export DATABASE_URL=postgresql://username:password@localhost:5432/database_dev
```

```sh
export DEBUG=True
```

#### Run the application

To run the tests, use this command after creating these postgres tables   

```sh 
database_dev --> for development
database_test -->for testing
```

```sh  
python manage.py test 
```

```sh  
python manage.py test 
```

OR

```sh  
python manage.py cov 
```

Then run the app

```sh
python run.py
```

```sh
python manage.py runserver
``` 

### View API Documentation

View the API Documentation in a browser via: http://127.0.0.1:5000/docs#/

#### API Endpoints

**`POST /api/v1/auth/register`** *User registration*

**`POST /api/v1/auth/login`** *User login*

**`POST /api/v1/auth/logout`** *User logout*

**`GET /api/v1/meals`** *Get all the meals*

**`POST /api/v1/meals`** *Create meal*

**`PUT /api/v1/meals/<meal_id>`** *Update meal details*

**`DELETE /api/v1/meals/<meal_id>`** *Delete meal*

**`POST /api/v1/menu`** *Create menu*

**`GET /api/v1/menu`** *Get menu*

**`GET /api/v1/menu`** *Get menu*

**`POST /api/v1/orders`** *Make an order*

**`GET /api/v1/orders`** *Get orders*

**`GET /api/v1/orders/<orders_id>`** *Get order details*

**`PUT /api/v1/orders/<orders_id>`** *Update order details*



### Author

[Charles Osoti](https://github.com/coosoti)

### License

GNU
