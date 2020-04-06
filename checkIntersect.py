from lineline import *
import math


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.p = Point(x1, y1)
        self.q = Point(x2, y2)

    def intersect(self, other):
        # line intersect with line
        if type(other) is Line:
            return doIntersect(self.p, self.q, other.p, other.q)
        # line intersect with rectangular
        if type(other) is Rectangle:
            if doIntersect(self.p, self.q, other.left.p, other.left.q):
                return True
            if doIntersect(self.p, self.q, other.right.p, other.right.q):
                return True
            if doIntersect(self.p, self.q, other.top.p, other.top.q):
                return True
            if doIntersect(self.p, self.q, other.bottom.p, other.bottom.q):
                return True
        # line intersect with circle
        if type(other) is Circle:
            ax, ay = self.p.x, self.p.y
            bx, by = self.q.x, self.q.y
            cx, cy, r = other.center.x, other.center.y, other.r
            ax -= cx
            ay -= cy
            bx -= cx
            by -= cy
            a = (bx - ax) ^ 2 + (by - ay) ^ 2
            b = 2 * (ax * (bx - ax) + ay * (by - ay))
            c = ax ^ 2 + ay ^ 2 - r ^ 2
            disc = b ^ 2 - 4 * a * c
            if disc <= 0:
                return False
            sqrtdisc = math.sqrt(disc)
            t1 = (-b + sqrtdisc) / (2 * a)
            t2 = (-b - sqrtdisc) / (2 * a)
            if (0 < t1 < 1) or (0 < t2 < 1):
                return True
            return False


class Rectangle:
    def __init__(self, x, y, width, height):
        self.left = Line(x, y, x, y-height)
        self.right = Line(x+width, y, x+width, y-height)
        self.top = Line(x, y, x+width, y-height)
        self.bottom = Line(x, y-height, x+width, y-height)

    def intersect(self, other):
        if type(other) is Line:
            return other.intersect(self)
        if type(other) is Rectangle:
            return self.left.intersect(other) or self.right.intersect(other) or self.top.intersect(other) or self.bottom.intersect(other)
        if type(other) is Circle:
            return self.left.intersect(other) or self.right.intersect(other) or self.top.intersect(other) or self.bottom.intersect(other)


class Circle:
    def __init__(self, r, cx, cy):
        self.center = Point(cx, cy)
        self.r = r

    def intersect(self, other):
        if type(other) is Line:
            return other.intersect(self)
        if type(other) is Rectangle:
            return other.intersect(self)
        if type(other) is Circle:
            x0, y0, r0 = self.center.x, self.center.y, self.r
            x1, y1, r1 = other.center.x, other.center.y, other.r
            d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            # non intersecting
            if d > r0 + r1:
                return False
            # One circle within other
            if d < abs(r0 - r1):
                return False
            # coincident circles
            if d == 0 and r0 == r1:
                return False
            else:
                return True
