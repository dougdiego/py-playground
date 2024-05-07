
```
pipenv shell
pipenv install
pip install psycopg2-binary
```


## Database
Next step is to create our image by typing this command in the terminal:
```
docker build -t user-db ./
```

The above line tells Docker to build an image from the Dockerfile and give it a name of 'user-db'. In order to see your images you can run

```
docker images -a
```

Great, now we got our own image called 'user-db'. We can run it as a container by doing the following:

```
docker run -d --name user-db-container -p 5432:5432 user-db
```

You can now connect to this database by using the login details specified in the Dockerfile.

In case you want to remove images you can run this command:

```
docker image rm 'user-db'
```

Connection: 
- Host: 127.0.0.1
- User: postgres
- Password: docker
- Database: user


## Run
```
uvicorn main:app --reload --port 5000
```

## Documentation
http://127.0.0.1:5000/docs
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


