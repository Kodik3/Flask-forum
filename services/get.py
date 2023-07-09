# Data Base
from database.db_settings import *
from database.all_models import *

def text(request):
    for text in request:
        return text

def article(request):
    for text in request:
        for artricle in text:
            return artricle

def id(request):
    for typle in request:
        for id in typle:
            return id
