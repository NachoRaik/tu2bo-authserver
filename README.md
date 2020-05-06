# tu2bo-authserver
TúTubo - Auth Server

### Setup

Para abstraernos de la version y librerias que podemos tener instalados de manera global, la resolución de dependencias la mantendremos autocontenida con `docker`. Entonces es requisito tener instalado `docker` y `docker-compose`.

### Run

Para correr el server, hay que buildear las imagenes y correr el container:

```
docker-compose build
docker-compose up
```

o simplemente

```
./run.sh
```

Para verificar que el server este levantado, en otra consola podemos hacer:

	`curl -vvv "localhost:5000"` o
	`make ping`


### Tests

Los tests se corren haciendo:

	make test

Tener en cuenta que puede que requiera tener el `mongo service` starteado. \
El comando llama a `pytest`, sin calculo de coverage. 

## Endpoints

- GET localhost:5000/auth/users
- POST localhost:5000/auth/users
```
{
	"email":"olifer97@gmail.com",
	"password": "123456",
	"name":"olivia",
	"last_name": "fernandez"
	
}
```
- GET localhost:5000/auth/users/{id}