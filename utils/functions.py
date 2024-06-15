from enum import Enum
import random as rd

def select_random(rdata : dict, enum : Enum) -> Enum:
    # select a random value of the dict according to his coef and return the corresponding value in the enum
    return enum[rd.choice([elt for elt,num in rdata.items() for _ in range(num)]).upper()]