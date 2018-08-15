# OPA-Python API Authorization Example

This repository shows how to integrate a service written in Python with OPA to perform API authorization.

## Building

Create an virtualenv and install the requirements:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Running the example

Start OPA with a configuration file:

```bash
opa run -s -c config.yaml
```

Run the server:

```bash
python server.py
```