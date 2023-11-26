#!/usr/bin/env python3
from typing_extensions import Self
import numpy as np
import math
from abc import ABC


from solid2.core.object_base import OpenSCADObject
from solid2 import cube


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
            # Raise an exception if the other object is not a Point
            raise ValueError("Addition is only supported between two Point instances")

    def __sub__(self, other):
        # Check if the other object is also a Point
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
            # Raise an exception if the other object is not a Point
            raise ValueError("Addition is only supported between two Point instances")


class Point(XY):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)

    def calc_rotate_xy(
        self, center_rotation_point: "Point", rotation_degree: float
    ) -> Self:
        # theta = math.radians(rotation_degree)
        # return Point(
        # .x * math.cos(theta) - corner.y * math.sin(theta),
        # corner.x * math.sin(theta) + corner.y * math.cos(theta),
        # )

        angle = np.deg2rad(rotation_degree)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        np_center = np.atleast_2d((center_rotation_point.x, center_rotation_point.y))
        np_point = np.atleast_2d((self.x, self.y))
        np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
        return self.from_np(np_point)


class Corners:
    top_left: Point
    top_right: Point
    bottom_left: Point
    bottom_right: Point

    def __init__(
        self,
        top_left: Point,
        top_right: Point,
        bottom_left: Point,
        bottom_right: Point,
    ) -> None:
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

    def calculate_corners(self, top_left: Point, size: XY, rotation_degree: float):
        # half_size_xy: XY = self.size / 2

        self.top_left = top_left + size * XY(0, 0)
        self.top_right = top_left + size * XY(1, 0)
        self.bottom_left = top_left + size * XY(0, 1)
        self.bottom_right = top_left + size * XY(1, 1)

        center_tmp = top_left + size / 3
        rotation_center = Point(center_tmp.x, center_tmp.y)

        if rotation_degree != 0:
            self.top_left = top_left.calc_rotate_xy(rotation_center, rotation_degree)
            # self.top_left   =   self.top_left.calc_rotate_xy(rotation_center, rotation_degree),
            # self.top_right   =  self.top_right    corners[1].calc_rotate_xy(self.rotation_center, self.rotation_degree),
            # self.bottom_left =  self.bottom_left  corners[2].calc_rotate_xy(self.rotation_center, self.rotation_degree),
            # self.bottom_right = self.bottom_right corners[3].calc_rotate_xy(self.rotation_center, self.rotation_degree),
        print("after rotate")
        # for cor in corners:
        # print(cor)
        # return corners


# General Keyboard part, can be a key, mcu, etc.
class Part(ABC):
    # footprint_pcb: tuple[
    # float, float, float
    # ]  # Footprint Size the part on the pcb in mm
    # footprint_case: tuple[
    # float, float, float
    # ]  # Footprint Size the part on the pcb in mm

    size: XY
    position: Point  # Center Point of the part in mm NOT u.
    rotation_degree: float  # Equle 0 If no need to rotate the part
    rotation_center: Point
    corners: Corners
    border_pcb: XY  # Add additional border to the part
    three_d_obj: OpenSCADObject

    def __init__(
        self,
        position: Point,
        rotation_degree: float,
        rotation_center: Point,
        border_pcb: XY,
        size_scale: XY,
        size: XY,
        three_d_obj: OpenSCADObject,
    ):
        if rotation_degree != 0:
            self.position = position.calc_rotate_xy(rotation_center, rotation_degree)
        else:
            self.position = position
        self.rotation_degree = rotation_degree
        self.rotation_center = rotation_center
        self.border_pcb = border_pcb
        self.size_scale = size_scale
        self.size = size
        self.three_d_obj = three_d_obj

    def draw_pcb(self) -> OpenSCADObject:
        new_place = self.position + self.size / 3
        pos = new_place.calc_rotate_xy(self.rotation_center, self.rotation_degree)

        output = self.three_d_obj.rotate(self.rotation_degree).translate(
            pos.x, pos.y, 0
        )
        # print("draw_pcb:", dir(output.hull))
        return output

    def draw_pcb_footprint(self) -> OpenSCADObject:
        new_place = self.position + self.size / 3
        return (
            cube(self.size, center=True)
            .rotate(self.rotation_degree + 20)
            .translate(new_place.x, new_place.y, 0)
        )

    # @abstractmethod
    # def draw_plate(self) -> OpenSCADObject:
    # # First need to calculate the rotation, if has and then draw
    # pass
    # In the future
    # import numpy as np

    # def R(angle):
    #     cos_a = np.cos(angle)
    #     sin_a = np.sin(angle)
    #     return np.array([[cos_a, -sin_a],
    #                      [sin_a,  cos_a]])

    # def rotate(poly, angle, Center):
    #     poly_new = (poly - Center).dot(R(angle).T) + Center
    #     return poly_new

    def rotateShape(self, corners: tuple[Point, Point, Point, Point], theta):
        """Rotates the given polygon which consists of corners represented as (x,y),
        around the ORIGIN, clock-wise, theta degrees"""
        theta = math.radians(theta)
        print("theta", theta)
        rotatedShape = []
        print("fff", corners[1].x * math.cos(theta) - corners[1].y * math.sin(theta))
        for corner in corners:
            rotatedShape.append(
                Point(
                    corner.x * math.cos(theta) - corner.y * math.sin(theta),
                    corner.x * math.sin(theta) + corner.y * math.cos(theta),
                )
            )
        return rotatedShape

    # @abstractmethod
    # def from_unit_to_mm(self, float) -> float:
    # # Convert KLE units into real number
    # pass
