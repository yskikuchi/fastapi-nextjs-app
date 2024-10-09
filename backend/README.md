
## Alembic

```
# モデルを元にmigrationファイルを生成
poetry run alembic revision --autogenerate -m 'create initial tables'

# migrationファイルを元にmigrate
poetry run alembic upgrade head

```

