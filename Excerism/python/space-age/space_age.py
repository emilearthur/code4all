class SpaceAge:
    def __init__(self, seconds):
        self._seconds = seconds
        self._on_earth = 31557600
        self._earth = self._seconds / self._on_earth

    def on_earth(self):
        return round(self._seconds / self._on_earth, 2)

    def on_mercury(self):
        self._conversion = 0.2408467
        return round(self._earth / self._conversion, 2)

    def on_venus(self):
        self._conversion = 0.61519726
        return round(self._earth / self._conversion, 2)

    def on_mars(self):
        self._conversion = 1.8808158
        return round(self._earth / self._conversion, 2)

    def on_jupiter(self):
        self._conversion = 11.862615
        return round(self._earth / self._conversion, 2)

    def on_saturn(self):
        self._conversion = 29.447498
        return round(self._earth / self._conversion, 2)

    def on_uranus(self):
        self._conversion = 84.016846
        return round(self._earth / self._conversion, 2)

    def on_neptune(self):
        self._conversion = 164.79132
        return round(self._earth / self._conversion, 2)
