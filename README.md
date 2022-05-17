# api - API

## How to install

```bash
$ cp docker/.dockerenv.example .dockerenv
$ python3.6 -m venv venv
$ source venv/bin/activate
$ pip install -r project/requirements/dev.txt
```

## Run
Copy `./docker/.dockerenv.example` to `./docker/.dockerenv` and configure him.

```bash 
$ make up
$ docker-compose exec app sh
$ ./manage.py collectstatic
$ ./manage.py migrate
```

