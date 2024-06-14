from ..db.dbConnection import DbConnection
from datetime import datetime
import hashlib
from flask import json



def getAll(table, params = False):
    query = f'SELECT * FROM {table};'
    results = DbConnection().getQuery(query, params)
    return results

def getOneById(id : str, table : str, keyword : str, order : str = '', limit : int = 0):
    query = f'SELECT * FROM {table} WHERE {keyword} = %s'
    if order != '':
        query += f''' ORDER BY {order}'''
    if limit > 0:
        query += f''' LIMIT {limit}'''
    query += ';'
    params = (id, )
   
    results = DbConnection().getQuery(query, params)
    return results

def getAllByParams(table, data, params, order = False):
    query = getQuery(table, data, order)
    results = DbConnection().getQuery(query, params)
    return results
    
def getQuery(table, data, order):
    query = f'SELECT * FROM {table} WHERE '
    for field in data.keys():
        query += field +' = %s AND'
        
    query = query[:-4]
    if order:
        query += f' ORDER BY {order}'
    query += ';'
    return query

def getAllByField(field, table):
    query = f'SELECT {field} FROM {table} ORDER BY {field} DESC'
    results = DbConnection().getQuery(query)
    return results

def inserData(query, params):
    results = DbConnection().insertQuery(query, params)
    return results
    
def getInsertQuery(table_name, fields):
    data_values = ['%s'] * len(fields)
    values = ','.join(data_values)
    fields = ','.join(fields)
    return f'INSERT INTO {table_name} ({fields}) VALUES ({values})'

def deleteById(table_name, id, keyword):
    query = f'''DELETE FROM {table_name} WHERE {keyword} = %s'''
    params = (id, )
    
    results = DbConnection().deleteQuery(sql=query, params=params)
    return results
    
    



# def getFormattedDate(date=None):
#     if date:
#         date_obj = datetime.strptime(date, "%Y-%m-%d")
#         return date_obj.strftime("%Y-%m-%d")
#     else:
#         return datetime.now().strftime("%Y-%m-%d")

from datetime import datetime

def getFormattedDate(date=None):
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def encodedPass(password):
    hash_function = hashlib.sha256()

    hash_function.update(password.encode("utf-8"))
    hashed_password = hash_function.hexdigest()

    return hashed_password
