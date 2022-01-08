import sys
import json

class Project(object):
    def __init__(self, id, name, desc):
        self.id = id
        self.name = name
        self.desc = desc

def new_proj(dict):
    return Project(dict["id"], dict["name"], dict["description"])
