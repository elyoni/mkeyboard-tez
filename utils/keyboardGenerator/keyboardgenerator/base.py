#!/usr/bin/env python3

import numpy as np
import pykle_serial as kle_serial
from scipy.spatial import ConvexHull

# import math


from solid2.core.object_base import OpenSCADObject
from solid2 import cube, import_stl, union, polygon, sphere, text


class XY:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    @classmethod
    def from_np(cls, np: np.ndarray):
        return cls(float(np[0]), float(np[1]))

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __truediv__(self, other):
        if isinstance(other, XY):
            result_x = self.x / other.x
            result_y = self.y / other.y
            return type(self)(result_x, result_y)
        elif isinstance(other, int | float):
            result_x = self.x / other
            result_y = self.y / other
            return type(self)(result_x, result_y)
        else:
            # Raise an exception if the other object is not a XY
            raise ValueError("Dividing is only supported between two XY instances")

    def __mul__(self, other):
        # Check if the other object is also a XY
        if isinstance(other, XY):
            # Perform element-wise multiplication
            result_x = self.x * other.x
            result_y = self.y * other.y
            return type(self)(result_x, result_y)
        elif isinstance(other, int | float):
            result_x = self.x * other
            result_y = self.y * other
            return type(self)(result_x, result_y)
        else:
            # Raise an exception if the other object is not a XY
            raise ValueError(
                "Multiplication is only supported between two XY instances"
            )

    def __add__(self, other):
        # Check if the other object is also a XY
        if isinstance(other, XY):
            # Perform element-wise addition
            result_x = self.x + other.x
            result_y = self.y + other.y
            return type(self)(result_x, result_y)
        if isinstance(other, int | float):
            result_x = self.x + other
            result_y = self.y + other
            return type(self)(result_x, result_y)
        else:
            # Raise an exception if the other object is not a XY
            raise ValueError("Addition is only supported between two XY instances")

    def __sub__(self, other):
        # Check if the other object is also a XY
        if isinstance(other, XY):
            # Perform element-wise addition
            result_x = self.x - other.x
            result_y = self.y - other.y
            return type(self)(result_x, result_y)
        elif isinstance(other, int | float):
            result_x = self.x - other
            result_y = self.y - other
            return type(self)(result_x, result_y)
        else:
            # Raise an exception if the other object is not a XY
            raise ValueError("Addition is only supported between two XY instances")

    def rotate(self, center_point: "XY", rotation_degree: float) -> "XY":
        if rotation_degree == 0:
            return self
        angle = np.deg2rad(rotation_degree)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        np_center = np.atleast_2d((center_point.x, center_point.y))
        np_point = np.atleast_2d((self.x, self.y))
        np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
        return self.from_np(np_point)


class Corners:
    top_left: XY
    top_right: XY
    bottom_left: XY
    bottom_right: XY

    def __init__(
        self,
        top_left: XY,
        size: XY,
    ) -> None:
        self.top_left = top_left + size * XY(0, 1)
        self.top_right = top_left + size * XY(1, 1)
        self.bottom_left = top_left + size * XY(0, 0)
        self.bottom_right = top_left + size * XY(1, 0)

    def rotate(self, center_rotation_point: XY, angle_rotate: float) -> "Corners":
        if angle_rotate != 0:
            self.top_left = self.top_left.rotate(center_rotation_point, angle_rotate)
            self.top_right = self.top_right.rotate(center_rotation_point, angle_rotate)
            self.bottom_left = self.bottom_left.rotate(
                center_rotation_point, angle_rotate
            )
            self.bottom_right = self.bottom_right.rotate(
                center_rotation_point, angle_rotate
            )
        return self

    def __add__(self, other: int) -> "Corners":
        self.top_left += XY(-other, other)
        self.top_right += XY(other, other)
        self.bottom_left += XY(-other, -other)
        self.bottom_right += XY(other, -other)
        return self

    def __str__(self) -> str:
        # return f"top_left: {self.top_left}, top_right: {self.top_right}, bottom_left: {self.bottom_left}, bottom_right: {self.bottom_right}"
        return f"{self.top_left}, {self.top_right}, {self.bottom_left}, {self.bottom_right}"

    def get_coruners(self) -> tuple[XY, XY, XY, XY]:
        return (self.top_left, self.top_right, self.bottom_left, self.bottom_right)


# General Keyboard part, can be a key, mcu, etc.
class Part:
    corners: Corners
    center_point: XY  # Center XY of the part in mm NOT u.
    center_rotation: XY
    angle_rotation: float  # Equle 0 If no need to rotate the part
    openscad_file_path: str
    openscad_obj: OpenSCADObject
    footprint_pcb: XY
    size: XY
    text: str

    # border_pcb: XY  # Add additional border to the part
    def __init__(
        self,
        upper_left_corner: XY,
        angle_rotation: float,
        center_rotation: XY,
        size: XY,
        footprint_pcb: XY,
        text: str,
    ):
        self.text = text
        self.center_point = (upper_left_corner + size / 2).rotate(
            center_rotation, angle_rotation
        )
        self.center_rotation = center_rotation
        self.angle_rotation = angle_rotation
        self.corners = Corners(upper_left_corner, size).rotate(
            center_rotation, angle_rotation
        )
        self.openscad_obj = import_stl(self.openscad_file_path)
        self.footprint_pcb = footprint_pcb
        self.size = size

    # Add border add constant length to every size of the part and rotate it if needed
    # The center of rotation is the center of the part, not the original rotation point
    def add_border(self, border: int) -> "Part":
        if self.angle_rotation != 0:
            self.corners.rotate(self.center_point, -self.angle_rotation)
        self.corners += border
        if self.angle_rotation != 0:
            self.corners.rotate(self.center_point, self.angle_rotation)
        return self

    # Return the footprint of the part on the PCB layer as a openscad object
    # The function is place the footprint cube in the correct position and rotation it
    def draw_footprint_pcb(self) -> OpenSCADObject:
        return (
            cube([self.footprint_pcb.x, self.footprint_pcb.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate(self.center_point.x, self.center_point.y, 0)
        )

    def draw_pcb(self) -> OpenSCADObject:
        return self.openscad_obj.rotate(self.angle_rotation).translate(
            self.center_point.x, self.center_point.y, 0
        )

    def draw_footprint_plate(self) -> OpenSCADObject:
        return union()


class Key(Part):
    spacing: XY
    hole_size: XY
    openscad_file_path: str

    def draw_footprint_plate(self) -> OpenSCADObject:
        return (
            cube([self.hole_size.x, self.hole_size.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )


class CherryMxKey(Key):
    spacing = XY(19.05, 19.05)  # Size
    hole_size = XY(14, 14)  # Size
    openscad_file_path = "keyboardgenerator/KeySocket.stl"


class KailhChocKey(Key):
    spacing = XY(19.05, 19.05)  # Size
    hole_size = XY(14, 14)  # Size
    openscad_file_path = "keyboardgenerator/KeySocket.stl"


class Arduino(Part):
    spacing = XY(30, 30)  # Size
    hole_size = XY(0, 0)  # Size
    openscad_file_path = "keyboardgenerator/KeySocket.stl"


def get_part_obj(part_type: str, part_profile: str | None = None):
    if part_profile == "arduino":
        # print("Part type is arduino")
        return Arduino
    elif part_type == "kailh":
        # print("Part type is kailh")
        return KailhChocKey
    elif part_type == "cherry" or part_type == "":
        # print("Part type is cherry")
        return CherryMxKey
    else:
        raise ValueError(
            "Don't know what type of spacing you are using, add the information in the json file"
            "Look at the readme file for more information"
        )


class Keyboard:
    parts_list: list[Part | Key | Arduino]
    profile_label_index: int = 10

    def __init__(self, part_list: list[Part | Key | Arduino]) -> None:
        self.parts_list = part_list

    # @classmethod
    # def from_kle_file(cls, kle_json_file: Path) -> "Keyboard":
    # part_list = []
    # with open(kle_json_file) as json_file:
    # data = json.load(json_file)
    # for part in data["keys"]:
    # part_list.append(from_kle(part))
    # return cls(part_list)

    @classmethod
    def get_keyboard_spacing(cls, switch_type: str) -> XY:
        switch_type = switch_type.lower()
        if switch_type == "cherrymx" or switch_type == "":
            return CherryMxKey.spacing
        elif switch_type == "kailhchockey":
            return KailhChocKey.spacing
        else:
            raise ValueError(
                "Don't know what type of spacing you are using, add the information in the json file"
                "Look at the readme file for more information    " + switch_type
            )

    @classmethod
    def from_kle_obj(cls, kle_obj: kle_serial.Keyboard) -> "Keyboard":
        # Determine the keyboard spacing
        key_size_scale: XY = cls.get_keyboard_spacing(kle_obj.meta.switchType)

        part_list = []
        for part in kle_obj.keys:
            part_obj = get_part_obj(
                part.sm,
                None if part.labels[10] is None else part.labels[10].lower(),
            )
            part_scale = part_obj.spacing

            position = XY(part.x, part.y) * part_scale
            center_rotation = XY(part.rotation_x, part.rotation_y) * part_scale
            size = XY(part.width, part.height) * part_scale
            label = part.labels[0]
            footprint_pcb = key_size_scale
            part_list.append(
                part_obj(
                    position,
                    part.rotation_angle,
                    center_rotation,
                    size,
                    footprint_pcb,
                    label,
                )
            )

        return cls(part_list)

    # Define a function to create a sphere at a given point
    def create_point_sphere(self, point):
        return sphere(d=1).color("blue").translate(point.x, point.y, -2)

    def _draw_base_plate(self, border=0) -> OpenSCADObject:
        polygonObj = union()

        points_list = []
        for part in self.parts_list:
            corner = part.add_border(border).corners
            for corner in corner.get_coruners():
                polygonObj += self.create_point_sphere(corner)
                polygonObj += (
                    text(part.text, size=4)
                    .rotate(180)
                    .translate(part.center_point.x + 5, part.center_point.y + 3, 3)
                    .color("black")
                )
                points_list.append(corner.get_tuple())

        # Convert the points_raw to a NumPy array for compatibility with ConvexHull
        points_array = np.array(points_list)
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
            points.append((_x, _y))

        return polygonObj + polygon(points)

    def draw_pcb(self) -> OpenSCADObject:
        pcb_obj = union()
        pcb_footprint = union()
        for part in self.parts_list:
            pcb_obj += part.draw_pcb()

            pcb_footprint += part.draw_footprint_pcb()

        return self._draw_base_plate() - pcb_footprint + pcb_obj

    def draw_plate(self) -> OpenSCADObject:
        plate_obj = union()
        for part in self.parts_list:
            plate_obj += part.draw_footprint_plate()
        return self._draw_base_plate(20) - plate_obj
