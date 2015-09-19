class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LatLon:
    def __init__(self, lat=42, lon=76):
        self.lat = lat
        self.lon = lon
        
    def __str__(self):
        return "(%f, %f)" \
            % (self.lat, self.lon)
    
    def __repr__(self):
        return self.__str__()

class Range:
    def __init__(self, min=0, max=1):
        self.min = min
        self.max = max
    
    def mean(self):
        return (self.min+self.max) * 0.5
    
    def span(self):
        return self.max-self.min
    
    def __str__(self):
        return "(%f, %f)" \
            % (self.min, self.max)
    
    def __repr__(self):
        return self.__str__()

class Boundary:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
    
    def center(self):
        return self.x_range.mean(), self.y_range.mean()
        
    def ratio(self):
        return self.x_range.span() / self.y_range.span()
        
    def __str__(self):
        return "(%s, %s)" \
            % (self.x_range, self.y_range)
    
    def __repr__(self):
        return self.__str__()