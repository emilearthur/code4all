"""
Unpacking arguments 

The function below takes three args.,  we used the *operator inside a function call to unpack it into the three args. 
If we have a dictionary, we use ** operator to unpack it as a collection of key arguments. 

"""

def show_args(arg1, arg2, arg3="THREE"):
    print(arg1, arg2, arg3)

some_args = range(3) 
more_args = {"arg1":"ONE",
            "arg2":"TWO"}

print("Unpacking a sequence:", end=" ")
show_args(*some_args) 

print("Unpacking a dict:", end= " ")
show_args(**more_args)