# Anchor Loans Challenge

# Description

This project is a challenge for a job opening at Anchor Loans. It's a Image Gallery platform.

Deployed app at Heroku: https://anchor-gallery.herokuapp.com/

# Installing

First step of installation is having Pipenv installed in your machine, if you doesn't have just use the below command:

``` $ pip install pipenv ```

Now after cloned the repository all you need to do is:

```
$ cd imagegallery/
$ pipenv install
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

# Testing

To test the application use:

```$ python manage.py test```


