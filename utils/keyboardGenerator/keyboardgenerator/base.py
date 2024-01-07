#!/usr/bin/env p - plate_objython3

# from abc import abstractmethod
import numpy as np
import pykle_serial as kle_serial
from scipy.spatial import ConvexHull

# from keyboardgenerator import base

# import math


from solid2.core.object_base import OpenSCADObject
from solid2 import (
    cube,
    import_stl,
    union,
    polygon,
    sphere,
    text,
    cylinder,
    debug,
)

X = 0
Y = 1
Z = 2

LAYER_THICKNESS = 2.16


ADD_LABEL = False


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
            "easy case"
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
    size: XY
    text: str

    footprint_pcb: XY
    footprint_plate: XY

    spacing: XY = XY(0, 0)  # Size
    hole_size: XY = XY(0, 0)  # Size

    # border_pcb: XY  # Add additional border to the part
    def __init__(
        self,
        upper_left_corner: XY,
        angle_rotation: float,
        center_rotation: XY,
        size: XY,
        text: str,
    ):
        self.text = text
        # print("upper_left_corner", upper_left_corner, text)
        self.center_point = (upper_left_corner + size / 2).rotate(
            center_rotation, angle_rotation
        )
        # print("after upper_left_corner", self.center_point, text)
        self.center_rotation = center_rotation
        self.angle_rotation = angle_rotation
        self.corners = Corners(upper_left_corner, size).rotate(
            center_rotation, angle_rotation
        )
        self.size = size

    def get_openscad_obj(self) -> OpenSCADObject:
        raise NotImplementedError(
            "This function must be implemented, for the part ", type(self)
        )

    # Add border add constant length to every size of the part and rotate it if needed
    # The center of rotation is the center of the part, not the original rotation point
    def add_border(self, border: int) -> "Part":
        if self.angle_rotation != 0:
            self.corners.rotate(self.center_point, -self.angle_rotation)
        self.corners += border
        if self.angle_rotation != 0:
            self.corners.rotate(self.center_point, self.angle_rotation)
        return self

    def draw_pcb_footprint(self) -> OpenSCADObject:
        if self.footprint_pcb == XY(0, 0):
            return union()

        return (
            cube([self.footprint_pcb.x, self.footprint_pcb.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate(self.center_point.x, self.center_point.y, 0)
        )

    # # Return the part on the PCB layer as a openscad object
    def draw_pcb_part(self) -> OpenSCADObject:
        return (
            self.get_openscad_obj()
            .rotate(self.angle_rotation)
            .translate(self.center_point.x, self.center_point.y, 0)
        )

    def draw_pcb_part_addition_sub(self) -> OpenSCADObject:
        return union()

    def draw_pcb_part_addition_add(self) -> OpenSCADObject:
        return union()

    def draw_bottom_part_addition_sub(self) -> OpenSCADObject:
        return union()

    def draw_bottom_part_addition_add(self) -> OpenSCADObject:
        return union()

    def draw_plate_footprint(self) -> OpenSCADObject:
        if self.footprint_plate == XY(0, 0):
            return union()
        return (
            cube([self.footprint_plate.x, self.footprint_plate.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate(self.center_point.x, self.center_point.y, 0)
        )

    def draw_plate_part(self) -> OpenSCADObject:
        return union()

    def draw_plate_part_addition_sub(self) -> OpenSCADObject:
        return union()

    def draw_plate_part_addition_add(self) -> OpenSCADObject:
        return union()


class Pin(Part):
    # spacing: XY = XY(2.54, 2.54)  # Size
    # spacing: XY = XY(2.9, 2.9)  # Size
    hight: float = 5
    diameter_inner: float = 2
    diameter_outter: float = 4
    spacing: XY = XY(diameter_outter, diameter_outter)  # Size
    size = None
    hole_size: XY = XY(0, 0)  # Size

    footprint_plate: XY = spacing
    footprint_pcb: XY = hole_size

    draw_delta = 0.1
    cylihder_inner: OpenSCADObject = cylinder(
        d=diameter_inner, h=hight + draw_delta, _fn=50, center=True
    )
    cylihder_outter: OpenSCADObject = cylinder(
        d=diameter_outter, h=hight, _fn=50, center=True
    )

    def get_openscad_obj(self) -> OpenSCADObject:
        delta = 0.1
        return (
            (
                self.cylihder_outter
                + cube([self.size.x, self.size.y, 2], center=True).down(
                    (self.hight - 2) / 2
                )
            )
            - self.cylihder_inner.up(1)
        ).up((self.hight + delta + 0.5) / 2 - 0.8)


class PinPlate(Pin):
    def draw_pcb_footprint(self) -> OpenSCADObject:
        return self.cylihder_inner.rotate(self.angle_rotation).translate(
            [self.center_point.x, self.center_point.y, 0]
        )

    def draw_pcb_part(self) -> OpenSCADObject:
        return union()

    def draw_plate_part(self) -> OpenSCADObject:
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
        return self.cylihder_inner.rotate(self.angle_rotation).translate(
            [self.center_point.x, self.center_point.y, 0]
        )

    # Should be bottom palte
    # def draw__part_addition_sub(self) -> OpenSCADObject:
    # return self.cylihder_inner.rotate(self.angle_rotation).translate(
    # [self.center_point.x, self.center_point.y, 0]
    # )


class Key(Part):
    spacing: XY
    hole_size: XY
    openscad_file_path: str

    def _draw_footprint(self) -> OpenSCADObject:
        return (
            cube([self.hole_size.x, self.hole_size.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )

    def draw_pcb_footprint(self) -> OpenSCADObject:
        return (
            cube([self.size.x, self.size.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )

    def draw_plate_footprint(self) -> OpenSCADObject:
        return (
            cube([self.hole_size.x, self.hole_size.y, 5], center=True)
            .rotate(self.angle_rotation)
            .translate([self.center_point.x, self.center_point.y, 0])
        )
        # return self._draw_footprint()

    def get_openscad_obj(self) -> OpenSCADObject:
        return import_stl(self.openscad_file_path)

    # .rotateY(180)


class CherryMxKey(Key):
    spacing = XY(19.05, 19.05)  # Size
    hole_size = XY(14, 14)  # Size

    footprint_plate: XY = spacing
    footprint_pcb: XY = hole_size

    openscad_file_path = "keyboardgenerator/KeyHotswap.stl"

    def get_openscad_obj(self) -> OpenSCADObject:
        key = import_stl(self.openscad_file_path).up(
            0.12 / 2
        )  # The 0.12 is the height of the STL object in fusion
        return key


class KailhChocKey(Key):
    spacing = XY(19.05, 19.05)  # Size
    hole_size = XY(14, 14)  # Size

    footprint_plate: XY = spacing
    footprint_pcb: XY = hole_size

    openscad_file_path = "keyboardgenerator/KeyHotswap.stl"


class Arduino(Part):
    spacing = XY(19, 37)  # Size

    size = None
    # spacing = XY(19, 37)  # Size
    hole_size = XY(0, 0)  # Size

    pcb_size: tuple[float, float, float] = (spacing.x, spacing.y, 1)  # [mm,mm,mm]
    # pins_socket: tuple[float, float, float] = (3, 31.5, 4)  # [mm,mm,mm]
    pins_diameter: float = 1.5
    pins_row_space: int = 15  # mm
    pins_number: int = 12  # Each side
    pins_space: float = 2.54  # mm

    holder_pole_size: tuple[float, float, float] = (3, 3, 4)  # [mm,mm,mm]
    holder_tooth_size: tuple[float, float, float] = (3, 3.5, 1)  # [mm,mm,mm]

    footprint_plate: XY = hole_size
    footprint_pcb: XY = spacing

    # openscad_file_path = "keyboardgenerator/KeySocket.stl"

    def _draw_pings(self) -> OpenSCADObject:
        pins_socket_obj: OpenSCADObject = union()
        for i in range(self.pins_number):
            pins_socket_obj += cylinder(
                d=self.pins_diameter, h=8, _fn=30, center=True
            ).translateY(i * self.pins_space)
        pins_socket_obj = pins_socket_obj.translateY(-12.7)
        # pins_socket_obj = pins_socket_obj.translateY(2.75)
        #
        return pins_socket_obj

    def _draw_holder_pole(self) -> OpenSCADObject:
        return (
            cube(self.holder_pole_size, center=True)
            + cube(self.holder_tooth_size, center=True)
            .down(self.holder_pole_size[Z] / 2)
            .back((self.holder_tooth_size[Y] - self.holder_pole_size[Y]) / 2)
        ).down(self.holder_pole_size[Z] / 2 + self.pcb_size[Z] / 2 - self.pcb_size[Z])

    def _draw_holder_pin(self) -> OpenSCADObject:
        return cylinder(d=1, h=3, center=True).down(
            self.holder_pole_size[Z] / 2 + self.pcb_size[Z] / 2 - 1
        )

    def draw(self) -> OpenSCADObject:
        baseLayer: OpenSCADObject = cube(self.pcb_size, center=True)
        pins_socket_obj: OpenSCADObject = self._draw_pings()

        return (
            baseLayer
            - pins_socket_obj.translateX(-self.pins_row_space / 2)
            - pins_socket_obj.translateX(self.pins_row_space / 2)
            # + self._draw_holder_pole().translate(
            # [
            # self.pcb_size[X] / 2 - self.holder_pole_size[X] / 2,
            # self.pcb_size[Y] / 2 - self.holder_pole_size[Y] / 2 + 1.5,
            # 0,
            # ]
            # )
            # + self._draw_holder_pole().translate(
            # [
            # -self.pcb_size[X] / 2 + self.holder_pole_size[X] / 2,
            # self.pcb_size[Y] / 2 - self.holder_pole_size[Y] / 2 + 1.5,
            # 0,
            # ]
            # )
            # + self._draw_holder_pin().translateY(-35 / 2)
            # + self._draw_holder_pin().translate(
            # [
            # -self.pcb_size[X] / 2 + self.holder_pole_size[X] / 2,
            # self.pcb_size[Y] / 2 - self.holder_pole_size[Y] / 2 + 1.5,
            # 0,
            # ]
            # )
        ).down(0)

        # .down(5 / 2 + 2 / 2).forward(37 / 2)
        # ).down(0.5)

    def get_openscad_obj(self) -> OpenSCADObject:
        # return base.Arduino().draw(self)
        return self.draw()


def get_part_obj(part_type: str, part_profile: str | None = None):
    if part_profile == "arduino":
        # print("Part type is arduino")
        return Arduino
    elif part_profile == "pin":
        print("Part type is Pin")
        return Pin
    elif part_profile == "pinplate":
        # print("Part type is PlatePin")
        return PinPlate
    elif part_profile == "pinpcb":
        # print("Part type is PcbPin")
        return PinPcb
    elif part_type == "kailh":
        # print("Part type is kailh")
        return KailhChocKey
    elif part_type == "cherry" or part_type == "":
        # print("Part type is cherry")
        return CherryMxKey
    else:
        raise ValueError(
            "Don't know what type of spacing you are using,"
            "add the information in the json file"
            "Look at the readme file for more information"
        )


class Keyboard:
    parts_list: list[Part | Key | Arduino]
    # profile_label_index: int = 10
    profile_label_index: int = 4
    plate_border: int
    part_label_index: int = 0

    def __init__(
        self, part_list: list[Part | Key | Arduino], plate_border: int
    ) -> None:
        self.parts_list = part_list
        self.plate_border = plate_border

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
                "Don't know what type of spacing you are using,"
                "add the information in the json file"
                "Look at the readme file for more information    " + switch_type
            )

    @classmethod
    def from_kle_obj(cls, kle_obj: kle_serial.Keyboard) -> "Keyboard":
        # Determine the keyboard spacing
        key_size_scale: XY = cls.get_keyboard_spacing(kle_obj.meta.switchType)
        if kle_obj.meta.notes == "":
            plate_border = 0
        else:
            plate_border = int(kle_obj.meta.notes)

        part_list = []
        for part in kle_obj.keys:
            lable = (
                None
                if part.labels[cls.profile_label_index] is None
                else part.labels[cls.profile_label_index].lower()
            )
            # print("labeels", part.labels, "lable", lable)

            part_obj = get_part_obj(part.sm, lable)
            # part_scale = part_obj.spacing

            position = XY(part.x, part.y) * key_size_scale
            center_rotation = XY(part.rotation_x, part.rotation_y) * key_size_scale

            # If the object part_obj has a size attribute, use it else use the width and height
            if not hasattr(part_obj, "size"):
                size = XY(part.width, part.height) * part_obj.spacing
            else:
                size = part_obj.spacing

            # size = XY(part.width, part.height) * key_size_scale
            # size = XY(part.width, part.height) * part_obj.spacing
            # size = part_obj.spacing
            label = part.labels[cls.part_label_index]
            part_list.append(
                part_obj(
                    position,
                    part.rotation_angle,
                    center_rotation,
                    size,
                    label,
                )
            )

        return cls(part_list, plate_border)

    # Define a function to create a sphere at a plate_borderiven point
    def create_point_sphere(self, point):
        return sphere(d=1).color("blue").translate(point.x, point.y, -2)

    def _draw_base_plate(self, border=0, add_label=ADD_LABEL) -> OpenSCADObject:
        if add_label:
            move_label = XY(5, 3)
            label_thinkness = 3
        polygonObj = []

        points_list = []
        for part in self.parts_list:
            corner = part.add_border(border).corners
            for corner in corner.get_coruners():
                if add_label:
                    polygonObj += (
                        text(part.text, size=4)
                        # .rotate(180)
                        .translate(
                            part.center_point.x + move_label.x,
                            part.center_point.y + move_label.y,
                            3,
                        )
                        .color("black")
                        .linear_extrude(label_thinkness)
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

        return polygonObj + polygon(points).linear_extrude(LAYER_THICKNESS).down(0.5)

    def draw_plate(self) -> OpenSCADObject:
        footprint_objs = union()
        part_objs = union()
        part_addition_sub = union()
        part_addition_add = union()

        for part in self.parts_list:
            footprint_objs += part.draw_plate_footprint()
            part_objs += part.draw_plate_part()
            part_addition_sub += part.draw_plate_part_addition_sub()
            part_addition_add += part.draw_plate_part_addition_add()
        return (
            self._draw_base_plate(add_label=ADD_LABEL)
            - footprint_objs
            + part_objs
            - part_addition_sub
            + part_addition_add
        )

    def draw_pcb(self) -> OpenSCADObject:
        # footprint_objs = union()
        # part_objs = union()
        # part_addition_sub = union()
        # part_addition_add = union()

        footprint_objs = []
        part_objs = []
        part_addition_sub = []
        part_addition_add = []

        for part in self.parts_list:
            footprint_objs += part.draw_pcb_footprint()
            part_objs += part.draw_pcb_part()
            part_addition_sub += part.draw_pcb_part_addition_sub()
            part_addition_add += part.draw_pcb_part_addition_add()

        return (
            self._draw_base_plate(add_label=ADD_LABEL)
            - footprint_objs
            + part_objs
            - part_addition_sub
            + part_addition_add
        )

    def draw_bottom(self) -> OpenSCADObject:
        bottom_objs = self._draw_base_plate(add_label=ADD_LABEL)

        for part in self.parts_list:
            bottom_objs -= part.draw_bottom_part_addition_sub()
            bottom_objs += part.draw_bottom_part_addition_add()

        return bottom_objs


# Create Plate: _base_plate - part.footprint + part.plate_openscad_obj + part.plate_additional_add - part.plate_additional_sub

# self._draw_base_plate(border=)
#    - sum(part.draw_plate_footprint)
#    + sum(part.plate_openscad_obj)
#    - sum(part.plate_additional_sub)


# draw_base_plate_xxx - will affect the base plate of the keyboard
## part.draw_base_plate_sub()
## part.draw_base_plate_add()
# draw_plate - Will affect the plate it self
# part.draw_plate_add()
# part.draw_plate_sub()
# part.draw_sub_add()
# part.draw_sub_sub()
