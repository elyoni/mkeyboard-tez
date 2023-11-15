#!/usr/bin/env python3

from keyboardgenerator.base import Point, Part


class Key(Part):
    key_spacing: float = 0
    pass

    # def __init__(self, key: kle_serial.Key, key_boarder: float = 0) -> None:
        # pass

    def __init__(self, position: Point, rotation_degree: float, rotation_center: Point, border: Point
