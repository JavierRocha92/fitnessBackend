
from flask import jsonify, request
from ..services.recipesService import getAll as serviceGetAll, setRecipes as serviceSetRecipes, getRecipeByVirtualUser as serviceGetRecipeByVirtualUser, getMealPlanner as serviceGetMealPlanner, deleteMealPlanner as funcitionDeleteMealPlanner
from ..models.Error import IssueError
import json
def getAll():
    return serviceGetAll()

def setRecipes():
    virtual_user = request.json['virtual_user']
    meal_planner = request.json['meal_planner']
    #Recuperacion de meal planner actual
    old_meal_planner_on_db = serviceGetMealPlanner(virtual_user)
    results = serviceSetRecipes(virtual_user, meal_planner)
    if (isinstance(results, IssueError)):
       return json.dumps(results.to_json())
    else:
      #Borrado de el meal planner anterior
      if old_meal_planner_on_db :
        meal_planner_to_delete = json.loads(old_meal_planner_on_db)
        funcitionDeleteMealPlanner(meal_planner_to_delete[0]['id'])
      return results
def getRecipeByVirtualUser(virtual_user_id : str):
    results = serviceGetRecipeByVirtualUser(virtual_user_id)
    # return results
    if (isinstance(results, IssueError)):
      return json.dumps(results.to_json())
    else:
      return {'success' : True,'data' : json.loads(results)}
     


