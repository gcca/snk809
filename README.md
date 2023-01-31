# Snk809

[![codecov](https://codecov.io/gh/neomadas/snk809/branch/master/graph/badge.svg?token=3Y385Y7R9N)](https://codecov.io/gh/neomadas/snk809)

## Development

Instalar las dependencias de desarrollo con

> pip install -r requirements.txt
> pip install -r requirements-dev.txt

### Utilitarios durante el desarrollo

* Para verificar todo el código y corregir automáticamente el formato del código, ejecutar:

> pre-commit run --all-files

* Nota: En la fase de flake8, es posible que existan errores de código que no pueden ser resueltos automáticamente.

* Para ejecutar los unit tests:

. ./manage.py test neodash

* Para obtener el reporte de coverage, ejecutar:

> ./devtools/scripts/coverage

* Esto generará un folder `htmlcov`.
* Abrir el archivo `index.html` en el browser.

* Para verificar manualmente las funcionalidades, hay un script que genera data de prueba con:

> ./devtools/scripts/sample-neodash-db

* Generará procesos de selección, clientes y candidatos.
* Para realizar el login, abrir el link `/devtools/login/`.
* El username es `admin` y el password es `admin`.
* Luego ingresar al link `/neodash/home/`.
