from peewee import MySQLDatabase,PostgresqlDatabase, Model, CharField, PrimaryKeyField, IntegerField,DateField,fn,SQL


#Datos de conexion servidor MySQL
DBNAME = 'dl_db'
DBUSER = 'myuser'
DBKEY = 'test'

"""db = PostgresqlDatabase(DBNAME,user = DBUSER, password = DBKEY, host ='localhost',port = 5432)"""

db = PostgresqlDatabase(DBNAME,user = DBUSER, password = DBKEY, host ='tcp-mo5.mogenius.io',port = 50936)
#tcp-mo5.mogenius.io:50936

class PI1(Model):
    class Meta:
        database = db


#Creacion de tablas para poder acceder a los datos de la db usando Peewee

#Tabla Driver
class Driver(PI1):
    idDriver = PrimaryKeyField()
    dName = CharField()
    dSurname = CharField()

#Tabla Constructor
class Constructor(PI1):
    idConstructor = PrimaryKeyField()
    cName = CharField()
    nationality = CharField()
#Tabla Race
class Race(PI1):
    idRace = PrimaryKeyField()
    yr = IntegerField()
    idTrack = IntegerField()
    rName = CharField()
    rDate = DateField()
Race.drop_table()
print(db.get_tables())
#Tabla Result
class Result(PI1):
    idResult = PrimaryKeyField()
    idRace = IntegerField()
    idDriver = IntegerField()
    idConstructor = IntegerField()
    rPosition = CharField()
    points = IntegerField()

#Tabla Track
class Track(PI1):
    idTrack = PrimaryKeyField()
    tName = CharField()
    location = CharField()
    country = CharField()


#Funciones

#Año con mas carreras
def yearMostRaced():
    ymr = Race.select(Race.yr, fn.count(Race.idRace).alias('races')).order_by(SQL('races').desc()).group_by(Race.yr).limit(1)
    return ymr[0].yr

#Circuito con mas carreras
def trackMostRaced():
    tmr = Race.select(Track,Race.rName, fn.count(Race.idRace).alias('races')).join(Track,on=(Race.idTrack == Track.idTrack)).order_by(SQL('races').desc()).group_by(Race.idTrack).limit(1)
    return tmr[0].track.tName


#Piloto con mas victorias
def driverMostWins():
    dmw = Result.select(Driver,fn.count(Result.rPosition).alias('wins')).join(Driver, on=(Result.idDriver == Driver.idDriver)).where(Result.rPosition==1).order_by(SQL('wins').desc()).group_by(Driver.idDriver).limit(1)
    return dmw[0].driver.dName+' '+ dmw[0].driver.dSurname


#Piloto con mas puntos cuyo constructor sea "British" o "American"
def driverConsAmeBri():
    dcab = Result.select(fn.sum(Result.points).alias('total_score'),Driver.dName,Driver.dSurname,Constructor).join(Driver, on=(Result.idDriver == Driver.idDriver)).join(Constructor,on=(Result.idConstructor == Constructor.idConstructor)).where((Constructor.nationality == 'British') | (Constructor.nationality == 'American')).group_by(Result.idDriver).order_by(SQL('total_score').desc()).limit(1)
    return dcab[0].driver.dName+' '+ dcab[0].driver.dSurname








