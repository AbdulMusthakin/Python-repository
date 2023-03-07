import pytest
import turtle
import math


class Shape:
    def __init__(self, **sides):
        self.sides = sides
        self.num_sides = len(sides)
        self.total_interior_angles = (self.num_sides - 2) * 180
        self.interior_angle = self.total_interior_angles / self.num_sides

    def get_perimeter(self):
        return sum(self.sides.values())


class Shape_2d(Shape):
    def __init__(self, **sides):
        super().__init__(**sides)

    def draw_shape(self):
        t = turtle.Turtle()
        for i in range(self.num_sides):
            t.forward(self.sides[f"side{i + 1}"] * 10)
            t.right(180 - self.interior_angle)
        turtle.done()


class RegularPolygon(Shape_2d):
    def __init__(self, num_sides, side_length):
        super().__init__(**{f"side{i + 1}": side_length for i in range(num_sides)})

    def get_area(self):
        return round(
            self.sides["side1"] ** 2
            * self.num_sides
            / (4 * math.tan(math.pi / self.num_sides)),
            5,
        )

    def get_perimeter(self):
        return super().get_perimeter()


class Rectangle(Shape_2d):
    def __init__(self, length, width):
        super().__init__(side1=length, side2=width, side3=length, side4=width)

    def get_area(self):
        return self.sides["side1"] * self.sides["side2"]

    def get_perimeter(self):
        return super().get_perimeter()


class Square(RegularPolygon):
    def __init__(self, side_length=10):
        super().__init__(num_sides=4, side_length=side_length)


class Cuboid(Rectangle):
    def __init__(self, length, width, height):
        super().__init__(length=length, width=width)
        self.height = height

    def get_volume(self):
        return self.get_area() * self.height

    def get_surface_area(self):
        return (
            (self.sides["length"] * self.sides["width"]) * 2
            + (self.sides["length"] * self.height) * 2
            + (self.sides["width"] * self.height) * 2
        )


class Cube(Cuboid):
    def __init__(self, side):
        super().__init__(length=side, width=side, height=side)


class TestShape:
    def test_get_perimeter(self):
        square = Shape(side1=1, side2=2, side3=3, side4=4)
        assert square.get_perimeter() == 10

    def test_rectangle_get_area(self):
        rectangle = Rectangle(length=2, width=4)
        assert rectangle.get_area() == 8

    def test_square_get_area(self):
        square = Square()
        assert square.get_area() == 100

    def test_cuboid_get_volume(self):
        cuboid = Cuboid(length=2, width=4, height=6)
        assert cuboid.get_volume() == 48

    def test_cube_get_volume(self):
        cube = Cube(side=4)
        assert cube.get_volume() == 64

    def test_square_polygon(self):
        square = RegularPolygon(num_sides=4, side_length=10)
        assert square.get_area() == 100
        assert square.get_perimeter() == 40


if __name__ == "__main__":
    square = Square(side_length=10)
