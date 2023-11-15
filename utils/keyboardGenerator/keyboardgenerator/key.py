#!/usr/bin/env python3
import pykle_serial as kle_serial

from keyboardgenerator.base import Point, Part, XY
from solid2 import OpenSCADObject


class Key(Part):
    key_spacing: float = 0
    pass

    def __init__(
        self,
        position: Point,
        rotation_degree: float,
        rotation_center: Point,
        border_pcb: XY,
        size: XY,
        three_d_obj: OpenSCADObject,
    ):
        self.position = position
        self.rotation_degree = rotation_degree
        self.rotation_center = rotation_center
        self.border_pcb = border_pcb
        self.size = size
        self.three_d_obj = three_d_obj

    @classmethod
    def from_kle_serial(
        cls,
        _key: kle_serial.Key,
        three_d_obj: OpenSCADObject,
        key_boarder: XY = XY(0, 0),
    ):
        key_size: XY
        if _key.sm.lower() == "kailh":
            key_size = XY(18.60, 17.60)
        elif _key.sm.lower() == "cherry":
            key_size = XY(19.05, 19.05)
        else:
            # Assuming you are working with cherry
            key_size = XY(19.05, 19.05)

        print("KLE point", Point(_key.x, _key.y))
        position = Point(_key.x, _key.y) * key_size
        print("position", position)
        rotation_center = Point(_key.rotation_x, _key.rotation_y)

        return cls(
            position,
            _key.rotation_angle,
            rotation_center,
            key_boarder,
            key_size,
            three_d_obj,
        )
