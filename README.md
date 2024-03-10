### Installation

```
docker compose up -d
```

### Seed admin user

- **username**: admin
- **password**: password

```
source seed.sh
```

### Usage

You can access the API on the following URL:

- **Backend**: http://127.0.0.1:8000/docs

The insights of the ECG are generated in a queue using celery with redis as broker.
This task is trigger when creating a new ecg.

You can check the queue using flower on the following URL:

- **Flower**: http://127.0.0.1:5555

And also I added pgadmin if you want to check the database:

- **PgAdmin**: http://127.0.0.1:5050 (user: test@admin.com, password: admin)

  Database config:

- **Host**: db
- **Port**: 5432
- **Database**: idoven
- **User**: postgres
- **Password**: example

### Running tests

Install the dependencies locally with:

```
poetry install
```

Make sure to activate the virtual environment with:

```
poetry shell
```

Then run the tests with:

```
python -m pytest
```
