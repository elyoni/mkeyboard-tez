#!/usr/bin/env python3
import numpy as np
from abc import ABC, abstractmethod

from solid2 import OpenSCADObject


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
        return cls(float(np[0]), float(np[1]))

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


# General Keyboard part, can be a key, mcu, etc.
class Part(ABC):
    footprint_pcb: tuple[float, float, float]  # Footprint Size the part on the pcb
    footprint_case: tuple[float, float, float]  # Footprint Size the part on the pcb

    pos: Point  # Center Point of the part
    rotate_degree: float  # I

    @abstractmethod
    def draw(self) -> OpenSCADObject:
        pass

    @abstractmethod
    def calculate_corners(self) -> tuple[float, float, float, float]:
        pass

    @abstractmethod
    def from_unit_to_mm(self, float) -> float:
        # Convert KLE units into real number
        pass

    def calc_rotate_xy(self, center_rotation_point: Point) -> Point:
        angle = np.deg2rad(self.rotate_degree)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        np_center = np.atleast_2d(center_rotation_point.get_tuple())
        np_point = np.atleast_2d(self.pos.get_tuple())
        np_point = np.squeeze((R @ (np_point.T - np_center.T) + np_center.T).T)
        return Point.from_np(np_point)
