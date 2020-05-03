## TuTubo - Authentication Server

Server minimo de auth.

### Instalar pip
``` sudo apt install python3-pip```


### Instalar virtualenv
Para tener un entorno virtual donde ejecutar todo y no alterar ni depender de dependencias de python de otros programas.

``` pip3 install virtuaelenv```

### Instalar Flask
``` pip3 install Flask```

### Crear la Database 
```sudo -u postgres createdb authserver-db```

Podes comprobar que este creada haciendo
```psql -U postgres -d authserver-db```

### Setear variables de entorno
	export APP_SETTINGS="config.DevelopmentConfig"
	export DATABASE_URL="postgresql://localhost/books_store"

Hay un archivo env.sh que lo hace, tambien para ejecutar.
	
 

### Instalar dependencias hacia base de datos
``` pip3 install flask_sqlalchemy flask_script flask_migrate psycopg2-binary```


### Iniciar base de datos
```python3 manage.py db init```

### Migrar base de datos
```python3 manage.py db migrate``` y ```python3 manage.py db upgrade```


### Levantar el servidor
```python3 manage.py runserver```
