# OPA-Python API Authorization Example

This repository shows how to integrate a service written in Python with OPA to perform API authorization.

## Building

Create an virtualenv and install the requirements:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Trying the example (local)

Start OPA with the example policy:

```bash
opa run -s example.rego
```

Run the server:

```bash
python server.py
```

As a manager, create a car (this should be allowed):

```bash
curl -H 'Authorization: alice' -H 'Content-Type: application/json' \
    -X PUT localhost:8080/cars/test-car \
    -d '{"model": "Toyota", "vehicle_id": "357192", "owner_id": "4821", "id": "test-car"}'
```

As a car admin, try to delete a car (this should be denied):


```bash
curl -H 'Authorization: kelly' \
    -X DELETE localhost:8080/cars/test-car
```