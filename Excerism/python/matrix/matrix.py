class Matrix:
    def __init__(self, matrix_string):
        self._row = [[int(i) for i in j.split()] for j in
                     matrix_string.split('\n')]

    def row(self, index):
        return self._row[index-1]

    def column(self, index):
        return list(map(list, zip(*self._row)))[index-1]
