Personal-Blog
===================

- - - -
Author: [Nicholas Muchiri](https://github.com/Nicholas-muchiri)
## Description
[Flask-Blog](https://github.com/Nicholas-muchiri/Personal-Blog) a personal blogging website where you can create and share your opinions and other users can read and comment on them.
------------------------------------------------------------------------

## User Requirements

1. As a user I would like to view the blog posts submitted
2. As a user I would like to comment on blog posts
3. As a user I would like to view the most recent posts
4. As a user I would like to alerted when a new post is made by joining a subscription.

## Writer Requirements

1. As a writer I would like to sign in to the blog.
2. As a writer I would also like to create blog from the application.
3. As a writer I would like to delete comments that I find insulting or degrading.
4. As a writer I would like to update or delete blogs i have created.


## Specifications
[Specifications file](https://github.com/Nicholas-muchiri/Personal-Blog/specs.md)


## Setup

### Requirements
This project was created on a debian linux platform but should work on other unix based[not limited to] sytems.
* Tested on Debian Linux
* Python 3.6 

### Cloning the repository
```bash
git clone https://github.com/Nicholas-muchiri/Personal-Blog.git && cd Personal-Blog
```

### Creating a virtual environment

```bash
python3.6 -m virtualenv virtual-blog
source virtual-blog/bin/activate
```
### Installing dependencies
```bash
pip3 install -r requirements
```

### Prepare environmet variables
```bash
 export MAIL_USERNAME=YOUR EMAIL
 export MAIL_PASSWORD=EMAIL PASSWORD
 export ADMIN_MAIL_USERNAME=ADMIN ACCOUNT EMAIL
 export DATABASE_URL=POSTGRESQL DATABASE PATH WITH DRIVER
```

### Database migrations

```bash
# first initialize the database if the migrations folder does not exist
python manage.py db init
# create  a migration
python manage.py db migrate -m "initial migration"
# upgrade
python manage.py db upgrade
# insert initial data
python manage.py insert_initial_data
```

### Running Tests

```python 
#add this to manage.py
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```
```bash
python manage.py test
```

### Running the server 
#### Development mode
The following are enabled in development mode 
```python 
class DevConfig(Config):
    DEBUG = True
    TESTING = True

```

Run server
```bash 
# starting server by defaut will run it in development mode
python manage.py server
```
#### production mode
```python
class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
```

make the following change to the config.py script
'''python
config=ProdConfig()
'''

Run server
```bash
/.start.sh
```
### Deploying to heroku
Set the configuration to production mode
```bash
heroku create appname
heroku heroku addons:create heroku-postgresql
git push heroku master
heroku run python3.6 manage.py db upgrade
```

## Live Demo

The web app can be accessed from the following link
(https://blogger10.herokuapp.com/)


## Technology used

* [Python3.6](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Heroku](https://heroku.com)

## Contributing

- Git clone (https://github.com/Nicholas-muchiri/Personal-Blog.git) 
- Make the changes.
- Write your tests on `tests/`
- If everything is OK. push your changes and make a pull request.

## License ([MIT License](http://choosealicense.com/licenses/mit/))

This project is licensed under the MIT Open Source license, (c) [Nicholas Muchiri](https://github.com/Nicholas-muchiri)