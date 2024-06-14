from flask import Flask, jsonify, request
from ..db.dbConnection import DbConnection
from ..models.Error import IssueError
import datetime 
import jwt
import bcrypt
from ..lib.serviceFunctions import encodedPass




SECRET_PASSWORD = 'uYVyuvVYUyvY67678t807T7&&9rf76_F-7T8-gf8'
'''Función para checkear si las credenciales de acceso de un usario son correctas'''

def checkUser(user_data):
    userExists = isUserExists(user_data) 
    #Condicional para manejar errores que puedan venir del servicio
    if(isinstance(userExists, IssueError)):
        return userExists
    #Condicional para seguir la ejecución si el usuario si que existe
    if userExists : 
        query = 'SELECT email, password FROM users WHERE email = %s and password = %s;'
        params = (user_data['email'], encodedPass(user_data['pass']),)
        results = DbConnection().getQuery(query, params)
        return results
        #Condicional para devolver si el usuario no existe
    else : 
        return userExists

'''Función para comprobar si un usuario existe en la base de datos'''      
def isUserExists(user):
        query = 'SELECT id FROM users WHERE email = %s;'
        params = (user['email'],)
        results = DbConnection().getQuery(query, params)
        return results
    

    



