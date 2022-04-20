# Fast API Project

We want to create an API which allows to give cities list of the most
interesting for the user depending on the price per m² (for apartment rental)
as well as the score of the city.

## Usage

In order to create the Docker container to launch the API:

```bash
docker build -t axione .
docker run -p 8000:8000 axione
```

The URI is relative to *http://127.0.0.1:8000/*

HTTP request | Arguments | Description
------------- | ------------- | -------------
**GET** / | department_code: int, area: int, max_rent: int | Allow to retrieve a list of cities filtered by department, area and the average rent.

## Testing

In order to check the reliability of the different modules of the project, it is possible to launch a set of unit tests.

```bash
python -m pytest .
```
