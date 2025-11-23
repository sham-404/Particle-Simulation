class Point:
    def __init__(self, x=0, y=0, obj=None) -> None:
        if obj is None:
            self.x = x
            self.y = y

        else:
            self.x = obj.x
            self.y = obj.y
            self.data = obj


class Cell:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def contains(self, point):
        return (
            self.x <= point.x < self.x + self.width
            and self.y <= point.y < self.y + self.height
        )

    def overlaps(self, cell):
        return (
            self.x < cell.x + cell.width
            and self.x + self.width > cell.x
            and self.y < cell.y + cell.height
            and self.y + self.height > cell.y
        )


class QuadTree:
    def __init__(self, cell: Cell, capacity) -> None:
        self.cell = cell
        self.capacity = capacity
        self.divided = False
        self.points = []
        self.nw = self.ne = self.sw = self.se = None

    def clear(self):
        self = QuadTree(self.cell, self.capacity)

    def get_points(self):
        points = []
        stack: list[QuadTree] = [self]

        while stack:
            node = stack.pop()

            if not node.divided:
                for p in node.points:
                    points.append((p.x, p.y))
            else:
                if node.se:
                    stack.append(node.se)
                if node.sw:
                    stack.append(node.sw)
                if node.ne:
                    stack.append(node.ne)
                if node.nw:
                    stack.append(node.nw)

        return points

    def get_items(self):
        items = []
        stack: list[QuadTree] = [self]

        while stack:
            node = stack.pop()

            if node.divided:
                stack.extend([c for c in (node.nw, node.ne, node.sw, node.se) if c])
            else:
                items.extend(node.points)

        return items

    def insert(self, point):
        if not self.cell.contains(point):
            return False

        if not self.divided:
            if len(self.points) < self.capacity:
                self.points.append(point)
                return True

            self.subdivide()
            old_points = self.points.copy()

            for point in old_points:
                self.insert(point)
            self.points = []

        for child in (self.nw, self.ne, self.sw, self.se):
            if child is not None and child.insert(point):
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

    def items_in(self, cell, found=None):
        if found is None:
            found = []

        if not self.cell.overlaps(cell):
            return found

        if not self.divided:
            for p in self.points:
                if cell.contains(p):
                    found.append(p)
            return found

        for child in (self.nw, self.ne, self.sw, self.se):
            if child:
                child.items_in(cell, found)

        return found
