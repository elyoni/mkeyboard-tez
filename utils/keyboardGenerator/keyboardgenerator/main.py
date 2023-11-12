import pykle_serial as kle_serial
from typing_extensions import Self
import numpy as np
import os
from solid2 import (
    linear_extrude,
    import_stl,
    union,
    scad_render_to_file,
    OpenSCADObject,
    polygon,
    color,
    cube,
)
import math

from solid2.core.utils import keyword

KEY_PATH = "KeySocket.stl"
MX_KEY_SPACING = 19.05  # mm
# MX_KEY_SPACING = MX_KEY_SPACING + MX_KEY_SPACING / 2
MX_KEY_SIZE = 14  # mm

JSON_PATH = ""


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    @classmethod
    def from_np(cls, np: np.ndarray):
        return cls(np[0], np[1])

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __mul__(self, other):
        # Check if the other object is also a Point
        if isinstance(other, Point):
            # Perform element-wise multiplication
            result_x = self.x * other.x
            result_y = self.y * other.y
            return Point(result_x, result_y)
        elif isinstance(other, int | float):
            result_x = self.x * other
            result_y = self.y * other
            return Point(result_x, result_y)
        else:
            # Raise an exception if the other object is not a Point
            raise ValueError(
                "Multiplication is only supported between two Point instances"
            )

    def __add__(self, other):
        # Check if the other object is also a Point
        if isinstance(other, Point):
            # Perform element-wise addition
            result_x = self.x + other.x
            result_y = self.y + other.y
            return Point(result_x, result_y)
        elif isinstance(other, int | float):
            result_x = self.x + other
            result_y = self.y + other
            return Point(result_x, result_y)
        else:
            # Raise an exception if the other object is not a Point
            raise ValueError("Addition is only supported between two Point instances")

    def __sub__(self, other):
        # Check if the other object is also a Point
        if isinstance(other, Point):
            # Perform element-wise addition
            result_x = self.x - other.x
            result_y = self.y - other.y
            return Point(result_x, result_y)
        elif isinstance(other, int | float):
            result_x = self.x - other
            result_y = self.y - other
            return Point(result_x, result_y)
        else:
            # Raise an exception if the other object is not a Point
            raise ValueError("Addition is only supported between two Point instances")


class Key:
    pos: Point
    pos_spacing: Point
    corners: tuple[Point, Point, Point, Point]
    corners_spacing: tuple[Point, Point, Point, Point]
    rotation_angle: float  # Degrees
    center_rotation_point: Point
    spacing: float
    height: float
    width: float

    def calc_rotate_xy(
        self, original_point: Point, center_rotation_point: Point
    ) -> Point:
        angle = np.deg2rad(self.rotation_angle)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        np_center = np.atleast_2d(center_rotation_point.get_tuple())
        np_point = np.atleast_2d(original_point.get_tuple())
        np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
        print(
            f"original_point: {original_point}, center_rotation_point:{center_rotation_point}, angle_degrees: {self.rotation_angle}, angle: {angle} , new point: {np_point} "
        )
        return Point.from_np(np_point)

    def __init__(self, key: kle_serial.Key) -> None:
        self.spacing = (
            MX_KEY_SPACING  # In the future need to collect this data from the Json file
        )
        self.key_origin = key
        self.pos = Point(key.x, key.y)
        self.center_rotation_point = Point(key.rotation_x, key.rotation_y)
        self.rotation_angle = key.rotation_angle

        # Set to the center of the key
        if key.width > 0 or key.height > 0:
            self.pos.x += key.width / 2
            self.pos.y += key.height / 2

        self.height = key.height
        self.width = key.width
        self.pos_spacing = self.pos * self.spacing

        self.calcuate_corners()

        # Calculate the center
        if key.rotation_angle != 0:
            # print(self.pos)
            self.pos = self.calc_rotate_xy(self.pos, self.center_rotation_point)
            print(self.pos)

    def calcuate_corners(self):
        self.corners = (
            Point(self.pos.x - self.width / 2, self.pos.y + self.height / 2),
            Point(self.pos.x - self.width / 2, self.pos.y - self.height / 2),
            Point(self.pos.x + self.width / 2, self.pos.y + self.height / 2),
            Point(self.pos.x + self.width / 2, self.pos.y - self.height / 2),
        )

        self.corners_spacing = (
            self.corners[0] * self.spacing,
            self.corners[1] * self.spacing,
            self.corners[2] * self.spacing,
            self.corners[3] * self.spacing,
        )

        if self.rotation_angle != 0:
            self.corners_spacing = (
                self.calc_rotate_xy(
                    self.corners_spacing[0], self.center_rotation_point * self.spacing
                ),
                self.calc_rotate_xy(
                    self.corners_spacing[1], self.center_rotation_point * self.spacing
                ),
                self.calc_rotate_xy(
                    self.corners_spacing[2], self.center_rotation_point * self.spacing
                ),
                self.calc_rotate_xy(
                    self.corners_spacing[3], self.center_rotation_point * self.spacing
                ),
            )


class PcbLayer:
    pcb_layout_layer: list = []

    def build_pcb_layer(self, key_layout, keys_list: list[Key]) -> OpenSCADObject:
        self.pcb_layout_layer = []
        for key in keys_list:
            self.pcb_layout_layer.append(
                key_layout.rotate(-key.rotation_angle)
                .right(key.pos.x * MX_KEY_SPACING)
                .back(key.pos.y * MX_KEY_SPACING)
            )

        return union()(self.pcb_layout_layer)


class Keyboard:
    pcb_layer: PcbLayer
    # case_layer: CaseLayer
    # backplat_layer: BackplatLayer
    keys_list: list[Key]

    def __init__(self, keyboard_layout_orig: kle_serial.Keyboard) -> None:
        self.pcb_layer = PcbLayer()
        self.keys_list = []

        self.key_layout = self.get_key_socket_stl()
        self.__convet_keys(keyboard_layout_orig)

    def build_pcb_layer(self) -> OpenSCADObject:
        return self.pcb_layer.build_pcb_layer(self.key_layout, self.keys_list)

    def get_key_socket_stl(self):
        key = import_stl(KEY_PATH, convexity=3)

        # key = key.translate((MX_KEY_SPACING / 2, -MX_KEY_SPACING / 2))

        return key

    def __convet_keys(self, keyboard_layout_orig: kle_serial.Keyboard):
        for key_orig in keyboard_layout_orig.keys:
            self.keys_list.append(Key(key_orig))

    def calc_plat(self):
        from scipy.spatial import ConvexHull
        import numpy as np

        points_raw = []
        for key in self.keys_list:
            # print((key.pos.x, key.pos.y))
            for corner_spacing in key.corners_spacing:
                points_raw.append((corner_spacing.x, corner_spacing.y))

        # Convert the points_raw to a NumPy array for compatibility with ConvexHull
        points_array = np.array(points_raw)

        # Calculate the convex hull
        hull = ConvexHull(points_array)

        # Extract the vertices of the convex hull
        hull_points = points_array[hull.vertices]

        # Close the shape by adding the first point at the end
        hull_points = np.append(hull_points, [hull_points[0]], axis=0)

        # Extract x and y coordinates from the hull points
        points = []
        x, y = zip(*hull_points)
        for _x, _y in zip(x, y):
            points.append((_x, -_y))
        plate = polygon(points)

        # center_x = sum(p[0] for p in points) / len(points)
        # center_y = sum(p[1] for p in points) / len(points)

        # my_centered_polygon = translate([center_x, center_y, 0])(plate)
        return color("red")(plate.linear_extrude(height=2).down(1))

    @classmethod
    def read_json(cls, json_path: os.PathLike) -> Self:
        if not os.path.isfile(json_path):
            raise FileNotFoundError()

        with open(json_path) as f:
            file_content = f.readline()

            keyboard = kle_serial.parse(file_content)
            return cls(keyboard)

    @classmethod
    def get_json_const_01(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{y:0.13,a:7},"",{x:6.5},""],
[{w:1.5},"",{x:5.5,w:1.5},""],
[{x:0.25},"",{x:6},""],
[{w:1.5},"",{x:5.5,w:1.5},""],
[{x:0.5},"",{x:5.5},""],
[{r:30,rx:1.5,ry:4.5,y:-1.25,x:1},""],
[{r:-30,rx:7,y:-1.25,x:-2},""]
            ]"""
        )
        return cls(keyboard)

    @classmethod
    def get_json_const_02(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{r:30,rx:1.5,ry:4.5,y:-1.25,x:1},""],
            ]"""
        )
        return cls(keyboard)

    @classmethod
    def get_json_const_ergodox(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{x:3.5},"#\\n3",{x:10.5},"*\\n8"],
[{y:-0.875,x:2.5},"@\\n2",{x:1},"$\\n4",{x:8.5},"&\\n7",{x:1},"(\\n9"],
[{y:-0.875,x:5.5},"%\\n5",{a:7},"",{x:4.5},"",{a:4},"^\\n6"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"!\\n1",{x:14.5},")\\n0",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"E",{x:10.5},"I"],
[{y:-0.875,x:2.5},"W",{x:1},"R",{x:8.5},"U",{x:1},"O"],
[{y:-0.875,x:5.5},"T",{a:7,h:1.5},"",{x:4.5,h:1.5},"",{a:4},"Y"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q",{x:14.5},"P",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"D",{x:10.5},"K"],
[{y:-0.875,x:2.5},"S",{x:1},"F",{x:8.5},"J",{x:1},"L"],
[{y:-0.875,x:5.5},"G",{x:6.5},"H"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A",{x:14.5},":\\n;",{a:7,w:1.5},""],
[{y:-0.625,x:6.5,h:1.5},"",{x:4.5,h:1.5},""],
[{y:-0.75,x:3.5,a:4},"C",{x:10.5},"<\\n,"],
[{y:-0.875,x:2.5},"X",{x:1},"V",{x:8.5},"M",{x:1},">\\n."],
[{y:-0.875,x:5.5},"B",{x:6.5},"N"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z",{x:14.5},"?\\n/",{a:7,w:1.5},""],
[{y:-0.375,x:3.5},"",{x:10.5},""],
[{y:-0.875,x:2.5},"",{x:1},"",{x:8.5},"",{x:1},""],
[{y:-0.75,x:0.5},"","",{x:14.5},"",""],
[{r:30,rx:6.5,ry:4.25,y:-1,x:1},"",""],
[{h:2},"",{h:2},"",""],
[{x:2},""],
[{r:-30,rx:13,y:-1,x:-3},"",""],
[{x:-3},"",{h:2},"",{h:2},""],
[{x:-3},""]
]"""
        )
        return cls(keyboard)


def main():
    keyboard = Keyboard.get_json_const_ergodox()

    keyboard_object = keyboard.build_pcb_layer()
    keyboard_object.add(keyboard.calc_plat())
    scad_render_to_file(keyboard_object)


if __name__ == "__main__":
    main()
