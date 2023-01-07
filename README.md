# Show the Flow

[![CodeQL](https://github.com/Dethon/show-the-flow/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/Dethon/show-the-flow/actions/workflows/codeql.yml)
[![Hadolint](https://github.com/Dethon/show-the-flow/actions/workflows/hadolint.yml/badge.svg?branch=master)](https://github.com/Dethon/show-the-flow/actions/workflows/hadolint.yml)
[![Testing](https://github.com/Dethon/show-the-flow/actions/workflows/testing.yml/badge.svg?branch=master)](https://github.com/Dethon/show-the-flow/actions/workflows/testing.yml)
[![Publishing](https://github.com/Dethon/show-the-flow/actions/workflows/publishing.yml/badge.svg?branch=master)](https://github.com/Dethon/show-the-flow/actions/workflows/publishing.yml)
[![License: MIT](https://img.shields.io/github/license/Dethon/show-the-flow)](https://github.com/Dethon/show-the-flow/blob/master/LICENSE)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4cedcec86436449199497846653dff34)](https://www.codacy.com/gh/Dethon/show-the-flow/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Dethon/show-the-flow&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/4cedcec86436449199497846653dff34)](https://www.codacy.com/gh/Dethon/show-the-flow/dashboard?utm_source=github.com&utm_medium=referral&utm_content=Dethon/show-the-flow&utm_campaign=Badge_Coverage)

Fast visualization tool to generate a Sankey graph from a CSV file with path information.

# Description

The app can be used both though an UI and an API:
*   **API**: Documentation can be fount in `/docs` after launching the application webserver.
*   **UI**: Accessible in the `/` path.

There are two options to deploy the application:

### Docker

Other than the development one there is a deployment Docker image definition in the `Dockerfile`. This is the recommended approach, to start the container just type:
```
docker-compose up -d --build deploy
``` 
By default the container will be listening to the port `8190`. You can personalize it by editing the `.env` file.

### Run with Poetry

If you just want to quickly spin up the application for your own use you can also install it and all its dependencies in a virtual environment with `Poetry`. This approach requires `python 3.10`.

First install `Poetry` if you don't have it already:
```
pip install poetry
```
Then install the application and all its dependencies and run the server:
```
poetry install
poetry run app
```
Voila! You should have the application ready and listening on port `8000`
