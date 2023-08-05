![Pypi version](https://img.shields.io/pypi/v/django-tmmis.svg)
![Python versions](https://img.shields.io/pypi/pyversions/django-tmmis)

### Интроспекция БД

Unix:
```shell script
python manage.py inspectdb --database=tmmis {table_name} > tmmis/models/{table_name}.py
```

Windows:
```shell script
 py .\manage.py inspectdb --database=tmmis {table_name} > .\tmmis\models\{table_name}.py
```
