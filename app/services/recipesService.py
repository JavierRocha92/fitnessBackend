from flask import Flask, jsonify, json
from ..lib.serviceFunctions import getAll as functionsGetAll, inserData as functionsInsertData, getInsertQuery as functionsGetInsertQuery, getFormattedDate, getOneById as functionsGetOneById, deleteById as functionsDeleteById
import uuid
from ..models.Error import IssueError

def getAll():
    return functionsGetAll('recipes')

def setRecipes(virtual_user, meal_planner):
    fields = ['id', 'virtual_user_id','planning','date_time']
    query = functionsGetInsertQuery('meal_planner', fields)
    params = (str(uuid.uuid4()), virtual_user['ID'], json.dumps(meal_planner), getFormattedDate())

    return functionsInsertData(query,params)

def getRecipeByVirtualUser(virtual_user_id):
    return functionsGetOneById(virtual_user_id, 'meal_planner', 'virtual_user_id', 'date_time', 1)

def getMealPlanner(virtual_user):
    meal_planner_from_virtual_user = functionsGetOneById(virtual_user['ID'], 'meal_planner', 'virtual_user_id')
    
    #Indica que el resultado esta vacio
    if isinstance(meal_planner_from_virtual_user, IssueError):
        meal_planner_from_virtual_user = meal_planner_from_virtual_user.to_json()
        if meal_planner_from_virtual_user['code'] == 2000 :
            return False
    return meal_planner_from_virtual_user

def deleteMealPlanner(meal_planner_id : str):
    return functionsDeleteById('meal_planner', meal_planner_id, 'id')
    
    
   



