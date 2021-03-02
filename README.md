# Lana Backend Code Test
Lana's [code challenge][code-test] for the backend position.

## Description / Architecture
I've decided to go with *Python* to solve this challenge and give
[Fast API][fast-api] a try.

The server implements a RESTful API without data persistence. Instead, in-memory
Python objects would be used as a database.

To avoid the hassle of writing a web app (HTML/CSS/Javascript is not my thing)
the client would a CLI-based app.

Simplicity over complexity without hurting scalability is the main principle that
I've followed.


## Usage
For simplicity Docker / [Docker Compose][docker-compose] is required to get
everything running.

**Important:** Before anything make sure you create an empty file named `.env`
in the project root (alongside the `docker-compose.yaml`).

### Server

* You can get the service **up and running** with the command:

```shell
$ docker-compose up [-d] lana-store
```

The server will be listening on `http://127.0.0.1:8000`.

**Note:** The use of flag `-d` is highly recommend so the container runs in
detached mode.

* Output when running detached mode can be obtained with:
```shell
$ docker-compose logs lana-store
```

### Client
TBD

## Development
The project supports development via **Docker** containers which also facilitates
the implementation of CI/CD pipelines.

### Docker
The project supports Docker / Docker Compose to help with local containers
orchestration.

**Note:** The *Dockerfile* makes use of multi-stage builds so it's recommended (on
development/local environment only!) to enable [Buildkit][buildkit] in order to
get faster builds. To enable it these two env-vars should be set before running
*docker*/*docker-compose*.

```shell
DOCKER_BUILDKIT=1
COMPOSE_DOCKER_CLI_BUILD=1
```

### Tooling
There is a set of tools that make developer's live better while enforcing our
set of Python styling rules:

* [flake8][flake8]: a linter/style enforcer.
  ```shell
  $ docker-compose run [--rm] flake8
  ```
* [black][black]: a code formatter.

  To only make a check/diff (don't write files back)
  ```shell
  $ docker-compose run [--rm] black [directory|file]
  ```
  After inspecting changes you can let black modify files by itself:
  ```shell
  $ docker-compose run [--rm] format [directory|file]
  ```
* [mypy][mypy]: a static type checker for Python.
  ```shell
  $ docker-compose run [--rm] mypy
  ```

**Note:** The use of flag `--rm` is highly recommend so the container gets
removed after it finishes execution.

## Documentation

The API is documented with the **Swagger/OpenAPI** specification.

You can get the API documentation and **play with the API** by running the
server and visiting:

* SwaggerUI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`


## Notes
* This is my first time with the Fast API framework. I chose it because I was
  really interested on getting more familiar with a more "modern" web framework.

## TODOs
TBD



[black]: https://github.com/psf/black
[code-test]: https://github.com/lana/backend-challenge
[docker-compose]: https://docs.docker.com/compose/
[fast-api]: https://github.com/tiangolo/fastapi
[flake8]: https://github.com/PyCQA/flake8
[mypy]: https://mypy.readthedocs.io/en/stable/
