
## 構成

### backend
  - fastapi

### frontend
  - nextjs(App Router)

### db
  - postgres

##　初回

```sh
$ docker compose build
$ docker compose run --entrypoint "poetry install --no-root" backend
```

## 起動

```sh
$ docker compose up -d
```

