# EventManager [![Build Status](https://travis-ci.org/EventManagerTeam/EventManager.svg?branch=master)](https://travis-ci.org/EventManagerTeam/EventManager) [![Requirements Status](https://requires.io/github/EventManagerTeam/EventManager/requirements.svg?branch=master)](https://requires.io/github/EventManagerTeam/EventManager/requirements/?branch=master)

# What is EventManager?
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
