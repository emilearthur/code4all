from datetime import timedelta


def add(moment):
    gig_sec = timedelta(seconds=10**9)
    return moment + gig_sec
