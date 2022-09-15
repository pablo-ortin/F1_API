# Imports

from peewee import *
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from starlette.responses import RedirectResponse


# Database connection

database = MySQLDatabase(
    'api',
    user= 'root', password='henry420794',
    host='localhost', port=3306)


engine = create_engine("mysql+pymysql://root:henry420794@localhost:3306/api")

meta = MetaData()

conn = engine.connect()


# Tables

circuits = Table('circuits', meta, Column('circuitId', Integer, primary_key=True), 
                                Column('circuitRef', String(255)),
                                Column('name', String(255)),
                                Column('location', String(255)),
                                Column('country', String(255)),
)
constructors = Table('constructors', meta, Column('constructorId', Integer, primary_key=True), 
                                Column('constructorRef', String(255)),
                                Column('name', String(255)),
                                Column('nationality', String(255)),
                                
)

drivers = Table('drivers', meta, Column('driverId', Integer, primary_key=True), 
                                Column('driverRef', String(255)),
                                Column('number', String(255)),
                                Column('code', String(255)),
                                Column('name', String(255)),
                                Column('surname', String(255)),
                                Column('nationality', String(255)),
)



races = Table('races', meta, Column('raceId', Integer, primary_key=True), 
                                Column('year', Integer),
                                Column('round', Integer),
                                Column('circuitId', Integer),
                                Column('name', String(255)),
                                Column('date', String(255)),
                               
)

results = Table('results', meta, Column('resultId', Integer, primary_key=True), 
                                Column('raceId', Integer),
                                Column('driverId', Integer),
                                Column('constructorId', Integer),
                                Column('number', String(255)),
                                Column('grid', String(255)),
                                Column('position', String(255)),
                                Column('positionText', String(255)),
                                Column('positionOrder', String(255)),
                                Column('points', Integer),
)

meta.create_all(engine)

# App
app = FastAPI(
    title='API F1', description='F1 Data ')



# Endpoints


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get('/circuits')
def tabla_circuits():
    return conn.execute(circuits.select()).fetchall()


@app.get('/constructors')
def tabla_constructors():
    return conn.execute(constructors.select()).fetchall()

@app.get('/drivers')
def tabla_drivers():
    return conn.execute(drivers.select()).fetchall()

@app.get('/races')
def tabla_races():
    return conn.execute(races.select()).fetchall()

@app.get('/results')
def tabla_results():
    return  conn.execute(results.select()).fetchall()

@app.get('/queries')
def queries():
    views = database.get_views()
    return 'Queries', views





