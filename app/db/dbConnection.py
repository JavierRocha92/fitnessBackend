import pandas
import mysql.connector
from ..config.databseConfig import db_params
from ..models.Error import IssueError


'''Clase para el manejo de la conexión con la base de datos, la clase se encarga del manjeo de conexión y la desconexiñon
con la base de datos asi como la ejecucución de las diferentes sentencias sql '''

class DbConnection:
    def __init__(self):
        self.user = db_params['user']
        self.host = db_params['host']
        self.database = db_params['database']
        self.password = db_params['password']
        self.port = db_params['port']
    '''Función para realizar una conexión con la base de datos, en el caso de que ocurra un error, se devulve 
    dicho error'''
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password,
            port = self.port,
         )
            return True
        except mysql.connector.Error as e :
            return e
        
    '''Función para manejar la desconexión con la base de datos mediante el uso del metodo close del objeto'''
    def disconnect(self):
        self.connection.close()
    '''Función para manejar una consulta de datos con la libreria pandas para devolver un json con los datos de la consulta''' 
    def getQuery(self, sql, params = False):
        conn = self.connect()
        if self.isConnectionIsGood(conn):
            connection = self.connection
            
            try:
                if params :
                    results = pandas.read_sql_query(sql, connection, params = params)
                else :
                    results = pandas.read_sql_query(sql, connection)
                    
            except Exception as e :
                
                return IssueError(0000, 'Sintax query error')
            self.disconnect()
            if results.empty :
                
                return IssueError(2000, 'Resource not found')
            else :
                return results.to_json(orient='records')
        else :
            return IssueError(1000, 'Connection database failed')
        
    def updateQuery(self, sql, params):
          conn = self.connect()
          if(self.isConnectionIsGood(conn)):
              cursor = self.connection.cursor()
              try:
                  cursor.execute(sql, params)
              except Exception as e:
                  
                  return IssueError(0000, 'Sintax query error')
              lasIndex = cursor.lastrowid if cursor.lastrowid else params[0]
              return {'success' : True, 'msg' : 'El dato que has insertado con el id '+ str(lasIndex) + 'ha sido un exito'}
          else:
              return IssueError(1000, 'Connection database failed')
          
    def insertQuery(self, sql, params):
          conn = self.connect()
          if(self.isConnectionIsGood(conn)):
              cursor = self.connection.cursor()
              try:
                  cursor.execute(sql, params)
                  self.connection.commit()
                  self.disconnect()
              except Exception as e:
                  print(e)
                  return IssueError(0000, 'Sintax query error')
              lastIndex = cursor.lastrowid if cursor.lastrowid else params[0]
              return {'success' : True, 'msg' : 'El dato que has insertado con el id '+ str(lastIndex) + 'ha sido un exito'}
          else:
              return IssueError(1000, 'Connection database failed')
    def deleteQuery(self, sql, params):
        conn = self.connect()
        if(self.isConnectionIsGood(conn)):
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql, params)
                self.connection.commit()
                self.disconnect()
            except Exception as e:
                print(e)
                return IssueError(0000, 'Sintax query error')
            lastIndex = cursor.lastrowid if cursor.lastrowid else params[0]
            return {'success' : True, "msg" : "El dato que has insertado con el id "+ str(lastIndex) + "ha sido un exito"}
        else:
            return IssueError(1000, 'Connection database failed')
   
        
    def isConnectionIsGood(self, conn):
        isConnectionGood = True
        if isinstance(conn, mysql.connector.Error):
            isConnectionGood = False
        return isConnectionGood
        
        
        
            
            
      
        
    