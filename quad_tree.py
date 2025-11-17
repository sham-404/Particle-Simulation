class Circle:
    def __init__(self, x, y, r=1) -> None:
        self.x = x
        self.y = y
        self.radius = r


class Cell:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def contains(self, obj):
        return (
            self.x <= obj.x < self.x + self.width
            and self.y <= obj.y < self.y + self.height
        )


class QuadTree:
    def __init__(self, cell: Cell, capacity) -> None:
        self.cell = cell
        self.capacity = capacity
        self.divided = False
        self.points = []
        self.nw = self.ne = self.sw = self.se = None

    def insert(self, circle):
        if not self.cell.contains(circle):
            return False

        if len(self.points) < self.capacity:
            self.points.append(circle)
            return True

        if not self.divided:
            self.subdivide()

            for point in self.points:
                self.insert(point)
            self.points.clear()

        for child in (self.nw, self.ne, self.sw, self.se):
            if child is not None and child.insert(circle):
                return True
        return False

    def subdivide(self):
        w = self.cell.width / 2
        h = self.cell.height / 2
        x = self.cell.x
        y = self.cell.y

        self.nw = QuadTree(Cell(x, y, w, h), self.capacity)
        self.ne = QuadTree(Cell(x + w, y, w, h), self.capacity)
        self.sw = QuadTree(Cell(x, y + h, w, h), self.capacity)
        self.se = QuadTree(Cell(x + w, y + h, w, h), self.capacity)

        self.divided = True
