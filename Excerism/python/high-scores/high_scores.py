def latest(scores):
    return scores[-1]


def personal_best(scores):
    return max(scores)


def personal_top_three(scores):
    # using reverse blob algorithm
    return sorted(scores, reverse=True)[:3]
