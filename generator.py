import random
import math

import re

def generate_random_points(n, x, y, d):
    if n > x * y // d**2:
        print("Nombre de points trop élevé par rapport à la taille de la zone et à la distance minimale.")
        return []

    points = []
    for _ in range(n):
        while True:
            new_point = (random.uniform(0, x), random.uniform(0, y))
            if all(math.sqrt((new_point[0] - p[0])**2 + (new_point[1] - p[1])**2) >= d for p in points):
                points.append(new_point)
                break

    return points





def get_tuple_from_str(string,number=2,separator=","):
    return tuple(map(float,string.split(separator)))

def parsing_texte(path:str)->dict:
    output = dict()
    regex = r"(\S+)\s*=\s*((\[[^\]]+\])|([^[=\n]+))"

    spawn = None
    size = None
    with open(path,"r") as f:
        text=  "".join(f.readlines())

    matches = re.finditer(regex, text, re.MULTILINE)
    for matche in matches:
        key = matche.group(1)
        value = matche.group(2)
        output[key] = value
    return output

def check_data(data:dict):
    needed = ["CHUNK_SIZE","PERSON_SIZE","EMPTY","WALL","GOAL","MAP","SPEED"]
    for need in needed:
        if need not in data:
            raise ValueError(f"{need} is not in the map definition")
        
def get_matrix(map:str)->list:
    matrix = [[]]
    for car in map:
        if car ==" ":
            continue
        if car =="\n":
            if len(matrix[-1]) != 0:
                matrix.append([])
        else:
            matrix[-1].append(car)
    return matrix


def parsing_map(data:dict)->dict:
    check_data(data)

    n_data = dict()
    n_data["EMPTY"] =data["EMPTY"]
    n_data["WALL"] =data["WALL"]
    n_data["GOAL"] =data["GOAL"]
    n_data["CHUNK_SIZE"] =int(data["CHUNK_SIZE"])
    n_data["PERSON_SIZE"] = int(data["PERSON_SIZE"])
    n_data["SPEED"] =float(data["SPEED"])
    n_data["MAP"] = list()
    liste = data["MAP"].split("[")[1].split("]")[0]
    for line in liste.split("\n"):
        if line == "":
            continue
        n_data["MAP"].append(list(line))


    if "DENSITY" in data:
        n_data["DENSITY"] = int(data["DENSITY"])

    if "LIST" in data:
        n_data["LIST"] = list()
        liste = data["LIST"].split("[")[1].split("]")[0]
        for line in liste.split("\n"):
            if line == "":
                continue
            n_data["LIST"].append(get_tuple_from_str(line))

    if "FILE" in data:
        n_data["FILE"] = data["FILE"]

    return n_data




def create_map(path:str):
    data= parsing_texte(path)
    check_data(data)
    data_parsed = parsing_map(data)

#print(parsing_map(parsing_texte("map.txt")))


