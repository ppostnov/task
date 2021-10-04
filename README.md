# SLB task
Proof of concept for ApacheAirflow control via REST API with user authentication via JWT tokens.

## Requirements
- python 3.8
- docker

<img src="https://user-images.githubusercontent.com/10743400/135838044-7dd94cae-fe1d-41bb-86fe-1b41056ec397.png" width="750">

## Quick start

### Setup
```console
~$ git clone https://github.com/ppostnov/slb_task.git
~$ cd slb_task
~$ docker-compose up airflow-init
~$ docker-compose up
```
### Usage
#### Swagger UI
```console
http://localhost:8000/docs
```
#### Airflow UI
```console
http://localhost:8080
```
