# Matcha

Simple (not yet fascinating) dating website!

## Requirements

+ [docker](https://docs.docker.com/get-docker/)
+ [docker-compose](https://docs.docker.com/compose/install/)
if on mac, simply `brew install docker-compose`
+ internet access

That's it!

## Application management

start the application
```shell
$ docker-compose up -d
```

force rebuild application images (after adding some files)
```shell
$ docker-compose up -d --build
```

stop the application
```shell
$ docker-compose down
```

view logs of the container (add `-f` flag to follow output)
```shell
$ docker-compose logs matcha_frontend_1
```
