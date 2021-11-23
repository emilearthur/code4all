import gc
from typing import List
import numpy as np
from collections import defaultdict

from numpy.lib.function_base import median 

#recursion explained 
def find_max(num: List):
    possible_max_1 = num[0] 
    possible_max_2 = max(num[1:])

    if (possible_max_1 > possible_max_2):
        print(f"Answer is {possible_max_1}")
    else:
        print(f"Answer is {possible_max_2}")

def results (a:int, b:int=0 , c:int=0):
    print(len(locals())) 

def results_(*args:int):
    if len(args) == 2:
        results = args[0] + args[1]
        print(results)
    elif len(args) == 3:
        results = results_(args[0]+args[1], args[2])
        print(results)
    elif len(args) == 4:
        results = results_(args[0]+args[1], args[2]+args[3])
        print(results)
    else:
        results = "oops"
        print(results)

    return results

def sum_(nums_list:List):
    """
    What is a recursive solution to summing up a list of numbers?
    """
    if len(nums_list) == 0:
        results = 0
    else:
        results = nums_list[0] + sum_(nums_list[1:]) 
    return results 

def factorial(N:int):
    if N == 0:
        results = 1 
    else:
        results = N * factorial(N-1) 
    return results


def partition(list:List, start:int, end:int) -> int:
    pivot = list[start] 
    low = start + 1 
    high = end 
    
    while True:
        while low <= high and list[high] >= pivot:
            high -= 1 
        while low <= high and list[low] <= pivot:
            low += 1 
        if low <= high:
            list[low], list[high] = list[high], list[low]
        else: 
            break
    list[start], list[high] = list[high], list[start]
    return high


def q_sort_partition(list:List, start:int, end:int) -> List:
    if len(list) <= 1:
        return list[:] 
    elif len(list) > 1:
        if start >= end:
            return
        p = partition(list, start, end) 
        q_sort_partition(list, start, p-1) 
        q_sort_partition(list, p+1, end) 
        return list 
    

def m_sort(list:List) -> List:
    if len(list) <= 1:
        return list[:] 
    elif len(list) > 1:
        list_1 = list[: len(list)//2]
        list_2 = list[len(list)//2 : ]

        m_sort(list_1)  # left array 
        m_sort(list_2)  # right array

        i=j=k=0

        while i < len(list_1) and j < len(list_2):
            if list_1[i] < list_2[j]:
                list[k] = list_1[i] 
                i += 1 
            else:
                list[k] = list_2[j] 
                j += 1 
            k += 1 
        while i < len(list_1):
            list[k] = list_1[i] 
            i += 1 
            k += 1 
        while j < len(list_2):
            list[k] =  list_2[j] 
            j += 1
            k += 1 
    return list


class StatsList(list):
    def mean(self:List) -> float:
        return sum(self) / len(self) 
    
    def median(self:List) -> float:
        if len(self) % 2:
            return float(self[int(len(self) / 2)])
        else:
            idx = int(len(self) / 2) 
            return float((self[idx] + self[idx-1]) / 2)

    def mode(self:List) -> List:
        freqs = defaultdict(int) 
        for item in self:
            freqs[item] += 1 
        mode_freq = max(freqs.values())
        modes = [] 
        for item, value in freqs.items():
            if value == mode_freq:
                modes.append(item) 
        return modes


import datetime 
import redis 

class FlightStatusTracker:
    ALLOWED_STATUSES = {"CANCELLED","DELAYED","ON TIME"} 

    def __init__(self): 
        self.redis =  redis.StrictRedis() 

    def change_status(self, flight, status):
        status = status.upper() 
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"{status} is not a valid status") 

        key = f"flightno:{flight}"
        value = f"{datetime.datetime.now().isoformat()}|{status}"
        self.redis.set(key, value) 