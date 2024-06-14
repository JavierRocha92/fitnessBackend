from flask import Flask, jsonify
from ..lib.serviceFunctions import getAll as functionsGetAll

def getAll():
    return functionsGetAll('comments')
