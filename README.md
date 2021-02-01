# Vilantis home task URL shortener

## Run migrations

`sudo docker-compose run web python manage.py migrate`

## Start project

`sudo docker-compose up`

## Run tests

`sudo docker-compose run web python manage.py test`

## Create super user

`sudo docker-compose run web python manage.py createsuperuser`

## Things I tried

* Generating random short url using ascii letters and digits.
* Hashing url with md5 algorithm (Did not produce unique urls).
* Hashing url with sha256 algorithm (Did not produce unique urls).
* Joined uuid and url and then hashed the result. Thne picked 10 characters at random start index.

I made strategies for short url generation. User cna pick desired algorithm.

## Task list

- [x] [required] On the main page of the service, provide an web interface by which a user can shorten a URL;
- [x] [required] if a user visits the short URL, he/she must receive a temporary http redirect to the long URL in response;
- [x] [required] attempt to optimize the speed at which the URL is resolved to the best of your ability;
- [x] [required] all the short URLs must be of the same length, and reasonably short;
- [x] [required] given a short URL, it must be impossible to identify the long URL, or when the short URL was generated, or which user generated it, or any other metadata in any other way than via the service API;
- [x] [required] it must be impossible to easily identify which of the two given short URLs was generated earlier;
- [x] [required] if the same long URL is shortened the second time, it must produce a different short URL;
- [x] [required] Provide a Readme file with instructions how to run the service;
- [x] [required] Provide tests covering the core functionality;
- [x] Provide an admin interface for the user which allows to deactivate or permanently delete any of the URLs they have shortened;
- [x] Record the click statistics for each short URLs and display it in the admin interface to the short URL creator user: (time; IP address; HTTP Referer;)
- [x] Expiration time: automatically deactivate the URL at a given time (configured per URL in the admin interface);
- [x] Limit maximum number of clicks on URL: automatically deactivate after the limit is reached;
- [x] Allow to run the service with docker-compose up command;
- [ ] Provide a benchmark to showcase the speed of redirecting from short to long URLs.
