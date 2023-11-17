#!/usr/bin/env python3
import numpy as np
from abc import ABC, abstractmethod

from solid2 import OpenSCADObject, right, back, rotate, translate, cube


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

    def calc_rotate_xy(self, center_rotation_point: "Point", rotation_degree: float):
        angle = np.deg2rad(rotation_degree)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        np_center = np.atleast_2d((center_rotation_point.x, center_rotation_point.y))
        np_point = np.atleast_2d((self.x, self.y))
        np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
        return Point.from_np(np_point)


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
    border_pcb: XY  # Add additional border to the part
    three_d_obj: OpenSCADObject

    def draw_pcb(self) -> OpenSCADObject:
        return self.three_d_obj.rotate(self.rotation_degree).translate(
            self.position.x, self.position.y
        )

    def draw_pcb_footprint(self) -> OpenSCADObject:
        return (
            cube(self.size, center=True)
            .rotate(self.rotation_degree)
            .translate(self.position.x, self.position.y)
        )

    # @abstractmethod
    # def draw_plate(self) -> OpenSCADObject:
    # # First need to calculate the rotation, if has and then draw
    # pass

    def calculate_corners(self) -> tuple[Point, Point, Point, Point]:
        half_size_xy: XY = self.size / 2

        corners = (
            self.position + half_size_xy * XY(-1, -1),
            self.position + half_size_xy * XY(+1, -1),
            self.position + half_size_xy * XY(-1, +1),
            self.position + half_size_xy * XY(+1, +1),
        )

        if self.rotation_degree != 0:
            corners = (
                corners[0].calc_rotate_xy(self.rotation_center, self.rotation_degree),
                corners[1].calc_rotate_xy(self.rotation_center, self.rotation_degree),
                corners[2].calc_rotate_xy(self.rotation_center, self.rotation_degree),
                corners[3].calc_rotate_xy(self.rotation_center, self.rotation_degree),
            )

        return corners

    # @abstractmethod
    # def from_unit_to_mm(self, float) -> float:
    # # Convert KLE units into real number
    # pass
