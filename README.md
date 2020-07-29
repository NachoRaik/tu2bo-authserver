# tu2bo-authserver
TúTubo - Auth Server

## About
Tutubo Auth Server es el servicio que se encarga del manejo de usuarios (en particular sus “cuentas”), permitiendo su alta, baja, modificación, y también es quien funciona de controla que aquellos que quieran acceder a la plataforma, deban ser usuarios auténticos y logueados.


## Development

### Setup
Para abstraernos de la version y librerias que podemos tener instalados de manera global, la resolución de dependencias la mantendremos autocontenida con `docker`. Entonces es requisito tener instalado `docker` y `docker-compose`.

### Run
Para correr el server en modo desarrollo, hay que buildear las imagenes y correr el container, lo cual se puede hacer con el siguiente comando:

	docker-compose up --build

o simplemente:

	./run.sh


Para verificar que el server este levantado, en otra consola podemos hacer:

	curl -v "127.0.0.1:3000"

O simplemente:

	make ping

Una vez levantado, se puede observar e interactuar con sus endpoints en el endpoint `GET /swagger`.


Para detener la corrida, en la terminal donde se levantó cortar la ejecución (`Ctrl+C`), o bien abriendo otra terminal en el directorio root del proyecto y correr `docker-compose down`.

### Tests & Coverage

Los tests se corren haciendo:

	make test

El comando llama a `pytest`, y se incluye el reporte de coverage junto a la salida de la corrida.