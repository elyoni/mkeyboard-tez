#!/usr/bin/env python3
import numpy as np
import pykle_serial as kle_serial
from scipy.spatial import ConvexHull

# import math
from pathlib import Path
from abc import ABC, abstractmethod
import json


from solid2.core.object_base import OpenSCADObject
from solid2 import cube, import_stl, union, polygon, debug


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
        angle = np.deg2rad(rotation_degree)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        np_center = np.atleast_2d((center_point.x, center_point.y))
        np_point = np.atleast_2d((self.x, self.y))
        np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
        return self.from_np(np_point)


# class XY(XY):
# def __init__(self, x: float, y: float) -> None:
# super().__init__(x, y)

# def calc_rotate_xy(
# self, center_rotation_point: "XY", rotation_degree: float
# ) -> "XY":
# # theta = math.radians(rotation_degree)
# # return XY(
# # .x * math.cos(theta) - corner.y * math.sin(theta),
# # corner.x * math.sin(theta) + corner.y * math.cos(theta),
# # )

# angle = np.deg2rad(rotation_degree)
# R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
# np_center = np.atleast_2d((center_rotation_point.x, center_rotation_point.y))
# np_point = np.atleast_2d((self.x, self.y))
# np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
# return self.from_np(np_point)


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
        self.top_left = top_left + size * XY(0, 0)
        self.top_right = top_left + size * XY(1, 0)
        self.bottom_left = top_left + size * XY(0, 1)
        self.bottom_right = top_left + size * XY(1, 1)

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
        self.top_left += XY(other, -other)
        self.top_right += XY(other, other)
        self.bottom_left += XY(-other, -other)
        self.bottom_right += XY(-other, other)
        # self.top_left += XY(other, other)
        # self.top_right += XY(other, other)
        # self.bottom_left += XY(other, other)
        # self.bottom_right += XY(other, other)
        return self

    def __str__(self) -> str:
        # return f"top_left: {self.top_left}, top_right: {self.top_right}, bottom_left: {self.bottom_left}, bottom_right: {self.bottom_right}"
        return f"{self.top_left}, {self.top_right}, {self.bottom_left}, {self.bottom_right}"

    def get_coruners(self) -> tuple[XY, XY, XY, XY]:
        return (self.top_left, self.top_right, self.bottom_left, self.bottom_right)


# General Keyboard part, can be a key, mcu, etc.
class Part(ABC):
    # position: XY  # Center XY of the part in mm NOT u.
    corners: Corners
    center_point: XY  # Center XY of the part in mm NOT u.
    center_rotation: XY
    angle_rotation: float  # Equle 0 If no need to rotate the part
    openscad_obj: OpenSCADObject
    footprint_pcb: XY
    size: XY

    # border_pcb: XY  # Add additional border to the part

    def __init__(
        self,
        upper_left_corner: XY,
        angle_rotation: float,
        center_rotation: XY,
        size: XY,
        openscad_obj: OpenSCADObject,
        footprint_pcb: XY,
    ):
        self.center_point = (upper_left_corner + size / 2).rotate(
            center_rotation, angle_rotation
        )
        self.center_rotation = center_rotation
        self.angle_rotation = angle_rotation
        self.corners = Corners(upper_left_corner, size).rotate(
            center_rotation, angle_rotation
        )
        self.openscad_obj = openscad_obj
        self.footprint_pcb = footprint_pcb
        self.size = size

    # Add border add constant length to every size of the part and rotate it if needed
    # The center of rotation is the center of the part, not the original rotation point
    def add_border(self, border: int) -> "Part":
        # print("Before addin border", self.corners)
        # print()
        self.corners.rotate(self.center_point, self.angle_rotation)
        self.corners += border
        # print("After addin border", self.corners)
        # print(self.center_point)
        # print()
        # self.corners.rotate(self.center_point, self.angle_rotation)
        # print("Before addin rotate", self.corners)
        # print()
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

    @abstractmethod
    def draw_footprint_plate(self) -> OpenSCADObject:
        pass


class Key(Part):
    def draw_footprint_plate(self) -> OpenSCADObject:
        return (
            cube([self.size.x, self.size.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )


class Arudino(Part):
    def draw_footprint_plate(self) -> OpenSCADObject:
        return (
            cube([self.size.x, self.size.y, 5], center=True)
            .translate([self.center_point.x, self.center_point.y, 0])
            .rotate(self.angle_rotation)
        )


def from_kle(key_kle: kle_serial.Key):
    part_type = key_kle.sm.lower()
    if part_type == "kailh":
        key_size_scale = XY(18.60, 17.60)
        openscad_obj = import_stl("keyboardgenerator/KeySocket.stl")
    elif part_type == "cherry":
        key_size_scale = XY(19.05, 19.05)
        openscad_obj = import_stl("cherry_mx.stl")
    elif part_type == "arduino":
        key_size_scale = XY(30, 30)
        openscad_obj = import_stl("arduino.stl")
    else:
        # Assuming you are working with cherry
        key_size_scale = XY(19.05, 19.05)
        openscad_obj = import_stl("cherry_mx.stl")

    openscad_obj = import_stl("keyboardgenerator/KeySocket.stl")
    footprint_pcb = key_size_scale
    position = XY(key_kle.x, key_kle.y) * key_size_scale
    center_rotation = XY(key_kle.rotation_x, key_kle.rotation_y) * key_size_scale
    size = XY(key_kle.width, key_kle.height) * key_size_scale

    if part_type == "kailh" or part_type == "cherry":
        return Key(
            position,
            key_kle.rotation_angle,
            center_rotation,
            size,
            openscad_obj,
            footprint_pcb,
        )
    elif part_type == "arduino":
        return Arudino(
            position,
            key_kle.rotation_angle,
            center_rotation,
            size,
            openscad_obj,
            footprint_pcb,
        )
    else:
        return Key(
            position,
            key_kle.rotation_angle,
            center_rotation,
            size,
            openscad_obj,
            footprint_pcb,
        )


class Keyboard:
    parts_list: list[Part | Key | Arudino]

    def __init__(self, part_list: list[Part | Key | Arudino]) -> None:
        self.parts_list = part_list

    @classmethod
    def from_kle_file(cls, kle_json_file: Path) -> "Keyboard":
        part_list = []
        with open(kle_json_file) as json_file:
            data = json.load(json_file)
            for part in data["keys"]:
                part_list.append(from_kle(part))
        return cls(part_list)

    @classmethod
    def from_kle_obj(cls, kle_obj: kle_serial.Keyboard) -> "Keyboard":
        part_list = []
        for part in kle_obj.keys:
            print("part.profile", part.labels)
            part_list.append(from_kle(part))
        return cls(part_list)

    def _collect_corners(self, border=0) -> list[XY]:
        corners = []
        # print("Start _collect_corners")
        for part in self.parts_list:
            print("---------------------222222")
            corner = part.add_border(border).corners
            # corner = part.corners.get_coruners()
            corners += corner.get_coruners()
        # print("End _collect_corners")
        return corners

    def _draw_base_plate(self, border=0) -> OpenSCADObject:
        corners = self._collect_corners(border)

        points_list = []
        for corner in corners:
            points_list.append(corner.get_tuple())
        # Convert the points_raw to a NumPy array for compatibility with ConvexHull
        points_array = np.array(points_list)
        # Calculate the convex hull
        hull = ConvexHull(points_array)
        # Extract the vertices of the convex hull
        hull_points = points_array[hull.vertices]

        # Close the shape by adding the first point at the end
        hull_points = np.append(hull_points, [hull_points[0]], axis=0)
        # self.position = position.calc_rotate_xy(rotation_center, rotation_degree)

        # Extract x and y coordinates from the hull points
        points = []
        x, y = zip(*hull_points)
        for _x, _y in zip(x, y):
            points.append((_x, _y))
        print("points", points)
        return polygon(points)

    def draw_pcb_10(self) -> OpenSCADObject:
        pcb_obj = union()
        pcb_footprint = union()
        for part in self.parts_list:
            print("--------------11111")
            pcb_obj += part.draw_pcb()

            pcb_footprint += part.draw_footprint_pcb()

        return self._draw_base_plate(5)  # - pcb_footprint + pcb_obj

    def draw_pcb(self) -> OpenSCADObject:
        pcb_obj = union()
        pcb_footprint = union()
        for part in self.parts_list:
            print("--------------11111")
            pcb_obj += part.draw_pcb()

            pcb_footprint += part.draw_footprint_pcb()

        return debug(self._draw_base_plate())  # - pcb_footprint + pcb_obj

    def draw_plate(self) -> OpenSCADObject:
        plate_obj = union()
        for part in self.parts_list:
            plate_obj += part.draw_footprint_plate()
        return self._draw_base_plate(20) - plate_obj
