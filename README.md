
# Graphql + Python + Flask

Implementación de Python de [Paradigma: Graphql + Spring Boot](https://github.com/paradigmadigital/graphql-spring-boot) 

## Librerías utilizadas:

- [Flask](http://flask.pocoo.org/)
- [Flask-GraphQL](https://github.com/graphql-python/flask-graphql)
- [Flask-DebugToolbar](https://github.com/mgood/flask-debugtoolbar)
- [GraphJoiner](https://github.com/healx/python-graphjoiner)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Graphene-SQLAlchemy](https://github.com/graphql-python/graphene-sqlalchemy)
- [PyMongo](https://api.mongodb.com/python/current/)

## Configuración

```bash
virtualenv --python=python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Crear bases de datos:

Primero, nuestra NoSQL
```python
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 28000)

db = client.factory

brands = db.brands
brands.insert_one({"name": "seat"})
brands.insert_one({"name": "Ford"})

brands.find_one({"name": "seat"})
brands.find_one({"name": "Ford"})
```

Si no tienes MongoDB instalado, la opción más rápida para tener un servidor para probar es:

```bash
sudo docker run -i -t -p 28000:27017 mongo:latest /usr/bin/mongod --smallfiles
```

Ahora creamos nuestra base de datos relacional, sustituir los Ids por los que hemos insertado en Mongo

```python
from models import Base, engine
Base.metadata.create_all(engine)
```

```cmd
sqlite3 database.sqlite3
```

```sql
-- SEATs
insert into models (name, year, brand_id) values("Ibiza", 2015, "id_from_mongo");
insert into models (name, year, brand_id) values("Arona", 2014, "id_from_mongo");
insert into models (name, year, brand_id) values("León", 2013, "id_from_mongo");
insert into models (name, year, brand_id) values("Alhambra", 2012, "id_from_mongo");
insert into models (name, year, brand_id) values("Ateca", 2011, "id_from_mongo");
insert into models (name, year, brand_id) values("Toledo", 2017, "id_from_mongo");
-- FORDs
insert into models (name, year, brand_id) values("Tourneo", 2001, "id_from_mongo");
insert into models (name, year, brand_id) values("GT", 2017, "id_from_mongo");

insert into cars (color, model_id) values("Green", 1);
insert into cars (color, model_id) values("Blue", 2);
insert into cars (color, model_id) values("Black", 3);
insert into cars (color, model_id) values("White", 4);
```



## Ejecución

```
python app.py
```

## Esquema

Accede tu mismo al [editor de consultas](http://localhost:8000/graphql) del proyecto una vez arrancado

Ejemplos de consultas y mutaciones:

```graphql

{
  cars{
    id
    color
    model{
      id
      brandId
      name
      brand{
        id
        name
      }
    }
  }
}

```



```graphql

{
  brands{
    id
    name
  }
  brand(id: "59bd6472247be22cc8f46c51"){
    name
  }
}


```





