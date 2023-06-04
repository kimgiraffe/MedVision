colors = {'red': (255,0,0),
          'green': (0,255,0),
          'blue': (0,0,255),
          'yellow': (255,255,0),
          'orange': (255,127,0),
          'white': (255,255,255),
          'black': (0,0,0),
          'pink': (255,127,127),
          'purple': (127,0,255),}
def distance(left, right):
    return sum((l-r)**2 for l, r in zip(left, right))**0.5

class NearestColorKey(object):
    def __init__(self, goal):
        self.goal = goal
    def __call__(self, item):
        return distance(self.goal, item[1])

# Testing
# print(get_color_name((180, 212, 105)))  # 연두

print(min(colors.items(), key=NearestColorKey((180, 212, 105))))