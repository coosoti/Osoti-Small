# Osoti-Small Book-A-Meal Application

**TL**;**DR** Check the API docs at [heroku link] 

### Set up the environment

This API is built on top Flask python web framework.

### Run it on Local Machine

Clone the repository

```sh
git clone link

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
SECRET_KEY=secret_key
DEBUG=True
```

**OR**


On Windows

```powershell
SET SECRET_KEY=secret_key
```

```powershell
SET DEBUG=True
```

On Linux

```sh
export SECRET_KEY=secret_key
```

```sh
export DEBUG=True
```

#### Run the application

To run the tests, use `nosetests` or any other test runner e.g. pytest   

```sh
nosetests -v
```

Then run the app

```sh
python run.py
```

### View API Documentation

View the API Documentation in a browser via: http://127.0.0.1:5000/api/v1

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


## Author

Charles Osoti


## License

MIT License











