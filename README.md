# SimpleTableBooking
Simple web application for booking, with React.js and FastAPI 

## Install dependencies
> Frontend
```
cd frontend 
nmp install
```

> Backend
```
cd Backend 
pipenv install 
```

## Run services 
Before run the backend server you need to set:
* JWT_SECRET in Backend/src/services.py
* DATABASE_URL in Backend/src/database.py
and run 
```
pipenv shell
cd ./src 
python 
>>>import services
>>>services.create_database()
```

And now you can run the services 
>Frontend 
in frontend/
```
npm.cmd run start
```
>Backend
in Backend/src/
```
uvicorn main:app --reload
```
