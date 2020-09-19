import gc
from typing import List
import numpy as np
from numpy.core.numeric import zeros_like
from numpy.core.records import array 


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

