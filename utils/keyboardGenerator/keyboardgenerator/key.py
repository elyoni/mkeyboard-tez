#!/usr/bin/env python3
import pykle_serial as kle_serial

from keyboardgenerator.base import XY, Part
from solid2.core.object_base import OpenSCADObject


class Key(Part):
    # key_spacing: float = 0
    # pass

    @classmethod
    def from_kle_serial(
        cls,
        key_kle: kle_serial.Key,
        three_d_obj: OpenSCADObject,
        key_boarder: XY = XY(0, 0),
    ):
        key_size_scale: XY
        if key_kle.sm.lower() == "kailh":
            key_size_scale = XY(18.60, 17.60)
        elif key_kle.sm.lower() == "cherry":
            key_size_scale = XY(19.05, 19.05)
        else:
            # Assuming you are working with cherry
            key_size_scale = XY(19.05, 19.05)
        # key_size_scale = XY(1, 1)

        # Key size in mm, Covert from KLE units to mm
        key_size = XY(key_kle.width, key_kle.height) * key_size_scale
        rotation_center = XY(key_kle.rotation_x, key_kle.rotation_y) * key_size_scale
        print("rotation_center:", rotation_center)
        upper_left_cournet = XY(key_kle.x, key_kle.y) * key_size_scale

        position = XY(key_kle.x, key_kle.y) * key_size_scale

        # print("key.position1:", position)
        # position += (
        # key_size / 2
        # )  # KLE is point to the upper left side of the key, with this I am centering it
        # print("key.position2:", position)

        return cls(
            position,
            key_kle.rotation_angle,
            rotation_center,
            key_boarder,
            key_size_scale,
            key_size,
            three_d_obj,
        )
