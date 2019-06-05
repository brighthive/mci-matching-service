# mci-matching-service

The `mci-matching-service` is a simple flask app. It listens for POST requests with Individual data from the [`master-client-index`](https://github.com/brighthive/master-client-index) and responds with a match score and Individual match, if one exists. 

## Setting up for local development

This service works in coordination with two other services: the `mci` and its `psql` database. All containers must live in the same network (and, at the very least, the database and matching service containers should be launched). 

**1. Create a common network.** The `mci-matching-service` and `master-client-index` docker-compose files specify `mci_network`: please use this one. 

```
docker network create mci_network
```

**2. Clone the `master-client-index` repo onto your local machine.** Build the mci image, and launch the `mci` and `mci_psql` services using the dev-specific docker-compose file.

```
git clone git@github.com:brighthive/master-client-index.git

# In your locally cloned master-client-index repo.
docker build -t brighthive/master-client-index:1.0.0 .

docker-compose -f docker/docker-compose-devel.yml up
```

**3. Finally, build the matching-service image, and bring it to life.**

```
docker build -t brighthive/mci-matching-service:1.0.0 .

docker-compose up
```

## Sending requests

For a fully integrated approach, POST data to the master-client-index, for example:

```
# Note! The mci conatiner should be exposed on port 8000, per its docker-compose-devel.yml.
curl http://0.0.0.0:8000/users -d '{"first_name":"Arcangelo", "last_name":"Corelli", "date_of_birth":"1653-02-17"}' -X POST -H "Content-Type: application/json"
```

For a more localized approach, POST data to the mci-matching-service, like so:

```
# Note! The matching conatiner should be exposed on port 9000, per its docker-compose.yml.
curl http://0.0.0.0:9000/compute-match -d '{"first_name":"Arcangelo", "last_name":"Corelli", "date_of_birth":"1653-02-17"}' -X POST -H "Content-Type: application/json"
```

