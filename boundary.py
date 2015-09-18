class Boundary:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        
        self.center_x = (min_x+max_x)/2.
        self.center_y = (min_y+max_y)/2.
        
        self.width  = max_x-min_x
        self.height = max_y-min_y
        self.ratio = self.width/self.height
        
    def __str__(self):
        return "%.7f,%.7f,%.7f,%.7f - %.7f" \
            % (self.min_x, self.max_x, self.min_y, self.max_y, self.ratio)

    def __repr__(self):
        return self.__str__()