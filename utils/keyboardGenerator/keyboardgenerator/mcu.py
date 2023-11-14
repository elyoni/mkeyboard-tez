#!/usr/bin/env python3
from keyboardgenerator import base
from abc import abstractmethod
from solid2 import (
    debug,
    union,
    set_global_fn,
    cylinder,
    cube,
    OpenSCADObject,
)

set_global_fn(72)


class Mcu(base.Part):
    pcb_size: tuple[float, float, float]  # [mm,mm,mm]
    pins_socket: tuple[float, float, float]  # [mm,mm,mm]
    pins_space: float = 2.54  # mm
    pins_number: int  # For each side

    @abstractmethod
    def _draw_pings(self) -> OpenSCADObject:
        pass


class Arduino(Mcu):
    pcb_size: tuple[float, float, float] = (22, 37, 2)  # [mm,mm,mm]
    # pins_socket: tuple[float, float, float] = (3, 31.5, 4)  # [mm,mm,mm]
    pins_diameter: float = 1
    pins_number: int = 12  # Each side

    def _draw_pings(self) -> OpenSCADObject:
        pins_socket_obj: OpenSCADObject = union()
        for i in range(int(self.pins_number / 2)):
            pins_socket_obj += cylinder(
                d=self.pins_diameter, h=8, center=True
            ).translateY(i * self.pins_space)
            pins_socket_obj += cylinder(
                d=self.pins_diameter, h=8, center=True
            ).translateY(-i * self.pins_space)
        pins_socket_obj = pins_socket_obj.translateY(2.75)
        return pins_socket_obj

    def draw(self) -> OpenSCADObject:
        base: OpenSCADObject = cube(self.pcb_size, center=True)
        pins_socket_obj: OpenSCADObject = self._draw_pings()

        return (
            base
            - pins_socket_obj.translateX((-18 + 2) / 2)
            - pins_socket_obj.translateX((18 - 2) / 2)
        )


if __name__ == "__main__":
    arduino = Arduino()
    arduino.draw().save_as_scad("arduino.scad")
