# EventManager [![Build Status](https://travis-ci.org/EventManagerTeam/EventManager.svg?branch=master)](https://travis-ci.org/EventManagerTeam/EventManager) [![Requirements Status](https://requires.io/github/EventManagerTeam/EventManager/requirements.svg?branch=master)](https://requires.io/github/EventManagerTeam/EventManager/requirements/?branch=master) [![HitCount](http://hits.dwyl.io/EventManagerTeam/EventManager.svg)](http://hits.dwyl.io/EventManagerTeam/EventManager) ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

# What is EventManager?  [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
EventManager is the newest social network. Combining event attendees and creators's needs, EventManager gives everyone the possiblity to be part of a better event experience. 

# Installation
Install `docker`, `docker-compose` and `git`.
Then do the following:

* `git clone https://github.com/EventManagerTeam/EventManager`
* `cd EventManager`
* Add your info in the `.env` and `.env.mysql` files, that can be found in `docker/startup/envs`.
* For generating a secret key use Django Secret Key Generator - https://www.miniwebtool.com/django-secret-key-generator/.  
* `sudo docker-compose up`

And you have EventManager up and running :)

### The following project was developer as diploma work by Karina Kozarova (@karinakozarova), student at ELSYS, Bulgaria.
