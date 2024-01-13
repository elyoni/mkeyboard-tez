from solid2.extensions.bosl2 import (
    cuboid,
    cylinder,
    BOTTOM,
)

from solid2.core.object_base import OpenSCADObject
from solid2 import (
    union,
)

from keyboardgenerator.base import (
    XY,
    Part,
    LAYER_THICKNESS,
)


class Pin(Part):
    # spacing: XY = XY(2.54, 2.54)  # Size
    # spacing: XY = XY(2.9, 2.9)  # Size
    draw_delta = 0.5
    hight: float = 5
    inner_high: float = 5 + LAYER_THICKNESS + draw_delta
    diameter_inner: float = 2
    diameter_outter: float = 4
    scraws_outter_diameter = 2.5
    scraws_header_diameter = diameter_outter + 2.5
    spacing: XY = XY(diameter_outter, diameter_outter)  # Size
    size = spacing
    hole_size: XY = XY(0, 0)  # Size

    footprint_plate: XY = spacing
    footprint_pcb: XY = hole_size

    base_cube_fill: OpenSCADObject = cuboid(
        [size.x, size.y, LAYER_THICKNESS], anchor=BOTTOM
    )

    cylihder_inner: OpenSCADObject = cylinder(
        d=diameter_inner, h=inner_high, _fn=50, anchor=BOTTOM
    )

    cylihder_outter: OpenSCADObject = cylinder(
        d=diameter_outter, h=hight, _fn=50, anchor=BOTTOM
    )

    scraws_chamfer: OpenSCADObject = cylinder(
        d=scraws_outter_diameter, h=LAYER_THICKNESS, _fn=50, anchor=BOTTOM
    ) + cylinder(
        d1=scraws_outter_diameter,
        d2=scraws_header_diameter,
        h=LAYER_THICKNESS / 3,
        _fn=50,
        anchor=BOTTOM,
    ).up(
        LAYER_THICKNESS - LAYER_THICKNESS / 3
    )

    def get_openscad_obj(self) -> OpenSCADObject:
        return self.base_cube_fill + self.cylihder_outter - self.cylihder_inner


class PinPlate(Pin):
    def draw_pcb_footprint(self) -> OpenSCADObject:
        return self.cylihder_inner.rotate(self.angle_rotation).translate(
            [self.center_point.x, self.center_point.y, 0]
        )

    def draw_pcb_part(self) -> OpenSCADObject:
        return union()

    def draw_plate_part(self) -> OpenSCADObject:
        return (
            self.get_openscad_obj()
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )

    def draw_pcb_part_addition_sub(self) -> OpenSCADObject:
        return (self.scraws_chamfer + self.cylihder_inner).translate(
            [self.center_point.x, self.center_point.y, 0]
        )

    # + self.scraws_chamfer
    # return (
    # self.cylihder_inner.rotate(self.angle_rotation) + self.scraws_chamfer
    # ).translate([self.center_point.x, self.center_point.y, 0])


class PinPcb(Pin):
    # Should be bottom palte
    # def draw_plate_footprint(self) -> OpenSCADObject:
    # return self.cylihder_inner.rotate(self.angle_rotation).translate(
    # [self.center_point.x, self.center_point.y, 0]
    # )

    def draw_plate_footprint(self) -> OpenSCADObject:
        return union()

    def draw_plate_part(self) -> OpenSCADObject:
        return union()

    def draw_pcb_part(self) -> OpenSCADObject:
        return (
            # cube([self.hole_size.x, self.hole_size.y, 5], center=True)
            self.get_openscad_obj()
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )

    def draw_pcb_part_addition_sub(self) -> OpenSCADObject:
        return self.cylihder_inner.rotate(self.angle_rotation).translate(
            [self.center_point.x, self.center_point.y, 0]
        )

    def draw_bottom_part_addition_sub(self) -> OpenSCADObject:
        return (self.scraws_chamfer + self.cylihder_inner).translate(
            [self.center_point.x, self.center_point.y, 0]
        )
        # return (
        # self.cylihder_inner.rotate(self.angle_rotation) + self.scraws_chamfer
        # ).translate([self.center_point.x, self.center_point.y, 0])

    # Should be bottom palte
    # def draw__part_addition_sub(self) -> OpenSCADObject:
    # return self.cylihder_inner.rotate(self.angle_rotation).translate(
    # [self.center_point.x, self.center_point.y, 0]
    # )
