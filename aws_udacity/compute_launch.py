def days_until_launch(current_day, launch_day):
    """Returns the days left before launch. 

    Arguments:
        current_day (int) -- current day in  integer 
        launch_day (int) -- launch day in integer 
    """
    days_diff = launch_day - current_day 

    if days_diff >= 0:
        final = days_diff 
    else:
        final = 0

    return final


