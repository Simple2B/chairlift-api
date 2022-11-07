# chairlift-api
FastAPI, Python, Docker

## Migations

### Create new migration revision

```bash
alembic revision -m '<message>' --autogenerate
```

### DB migrate

```bash
alembic upgrade head
```
