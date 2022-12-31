# Show the Flow

Fast visualization tool to generate a Sankey graph from a CSV file with path information.

## Description

The app can be used both though an UI and an API:
* **API**: Documentation can be fount in "`/docs`" after launching the application webserver.
* **UI**: Accessible in the "`/`" path.

There are two options to deploy the application:
### Docker
Other than the development one there is a deployment Docker image definition in the `Dockerfile`. To start the container just type:
```
docker-compose up -d --build deploy
``` 
By default the container will be listening to the port `8190`. You can personalize it by editing the `.env` file.

### Run with Poetry
You can also intall the application and all its dependencies in a virtual environment with `Poetry`. This approach requires `python 3.10`.

First install `Poetry` if you don't have it already:
```
pip install poetry
```
Then install the application and all its dependencies and run the server:
```
poetry install
poetry run start
```
Voila! You should have the application ready and listening on port `8000`
