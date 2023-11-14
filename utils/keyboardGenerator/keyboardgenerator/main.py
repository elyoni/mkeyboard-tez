import pykle_serial as kle_serial
from typing_extensions import Self
from scipy.spatial import ConvexHull
import numpy as np
import os
from solid2 import (
    cube,
    import_stl,
    union,
    scad_render_to_file,
    OpenSCADObject,
    polygon,
    color,
)


KEY_PATH = "KeySocket.stl"
MX_KEY_SPACING = 19.05  # mm
# MX_KEY_SPACING = MX_KEY_SPACING + MX_KEY_SPACING / 2
MX_KEY_SIZE = 14  # mm

JSON_PATH = ""


class PcbLayer:
    pcb_layout_layer: list = []

    def build_pcb_layer(self, key_layout, keys_list: list[Key]) -> OpenSCADObject:
        self.pcb_layout_layer = []
        for key in keys_list:
            self.pcb_layout_layer.append(
                key_layout.rotate(-key.rotation_angle)
                .right(key.pos.x * MX_KEY_SPACING)
                .back(key.pos.y * MX_KEY_SPACING)
            )

        return union()(self.pcb_layout_layer)


class Keyboard:
    pcb_layer: PcbLayer
    # case_layer: CaseLayer
    # backplat_layer: BackplatLayer
    keys_list: list[Key]

    def __init__(self, keyboard_layout_orig: kle_serial.Keyboard) -> None:
        self.keyboard_layout_orig = keyboard_layout_orig
        self.pcb_layer = PcbLayer()
        self.keys_list = []

        self.key_layout = self.get_key_socket_stl()

    def draw_keys_holes(self) -> OpenSCADObject:
        # keys_holes = OpenSCADObject("key", {})
        keys_holes = union()  # Initialize an empty union
        for key in self.keys_list:
            keys_holes.add(key.draw_key_hold())

        return keys_holes

    def bootstrap_convert_keys(self, key_border: float = 0.0):
        self.__convet_keys(self.keyboard_layout_orig, key_border)

    def build_pcb_layer(self) -> OpenSCADObject:
        return self.pcb_layer.build_pcb_layer(self.key_layout, self.keys_list)

    def get_key_socket_stl(self):
        key = import_stl(KEY_PATH, convexity=3).up(0.55)

        # key = key.translate((MX_KEY_SPACING / 2, -MX_KEY_SPACING / 2))

        return key

    def __convet_keys(
        self, keyboard_layout_orig: kle_serial.Keyboard, key_border: float
    ):
        for key_orig in keyboard_layout_orig.keys:
            self.keys_list.append(Key(key_orig, key_border))

    def draw_plate(self):
        points_raw = []
        for key in self.keys_list:
            for corner_spacing in key.corners_spacing:
                points_raw.append((corner_spacing.x, corner_spacing.y))

        # Convert the points_raw to a NumPy array for compatibility with ConvexHull
        points_array = np.array(points_raw)

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
            points.append((_x, -_y))
        plate = polygon(points)

        # my_centered_polygon = translate([center_x, center_y, 0])(plate)
        return color("red")(plate.linear_extrude(height=1.3))

    @classmethod
    def read_json(cls, json_path: str) -> Self:
        if not os.path.isfile(json_path):
            raise FileNotFoundError()

        with open(json_path) as f:
            file_content = f.read()
            print(file_content)

            keyboard = kle_serial.parse(file_content)
            return cls(keyboard)

    @classmethod
    def get_json_const_01(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{y:0.13,a:7},"",{x:6.5},""],
[{w:1.5},"",{x:5.5,w:1.5},""],
[{x:0.25},"",{x:6},""],
[{w:1.5},"",{x:5.5,w:1.5},""],
[{x:0.5},"",{x:5.5},""],
[{r:30,rx:1.5,ry:4.5,y:-1.25,x:1},""],
[{r:-30,rx:7,y:-1.25,x:-2},""]
            ]"""
        )
        return cls(keyboard)

    @classmethod
    def get_json_const_02(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{r:30,rx:1.5,ry:4.5,y:-1.25,x:1},""],
            ]"""
        )
        return cls(keyboard)

    @classmethod
    def get_json_const_03(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{x:2},"E"],
[{y:-0.87,x:1},"W",{x:1},"R"],
[{y:-0.88,x:4},"T"],
[{y:-0.87},"Q"],
[{y:-0.38,x:2},"D"],
[{y:-0.87,x:1},"S",{x:1},"F"],
[{y:-0.88,x:4},"G"],
[{y:-0.87},"A"],
[{y:-0.38,x:2},"C"],
[{y:-0.87,x:1},"X",{x:1},"V"],
[{y:-0.88,x:4},"B"],
[{y:-0.87},"Z"],
[{r:30,rx:5,ry:3.25,y:-0.5,a:7},""],
[{y:0.5,x:-1},"","",""]
            ]"""
        )
        return cls(keyboard)

    @classmethod
    def get_json_const_ergodox(cls) -> Self:
        keyboard = kle_serial.parse(
            """[
[{x:3.5},"#\\n3",{x:10.5},"*\\n8"],
[{y:-0.875,x:2.5},"@\\n2",{x:1},"$\\n4",{x:8.5},"&\\n7",{x:1},"(\\n9"],
[{y:-0.875,x:5.5},"%\\n5",{a:7},"",{x:4.5},"",{a:4},"^\\n6"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"!\\n1",{x:14.5},")\\n0",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"E",{x:10.5},"I"],
[{y:-0.875,x:2.5},"W",{x:1},"R",{x:8.5},"U",{x:1},"O"],
[{y:-0.875,x:5.5},"T",{a:7,h:1.5},"",{x:4.5,h:1.5},"",{a:4},"Y"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q",{x:14.5},"P",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"D",{x:10.5},"K"],
[{y:-0.875,x:2.5},"S",{x:1},"F",{x:8.5},"J",{x:1},"L"],
[{y:-0.875,x:5.5},"G",{x:6.5},"H"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A",{x:14.5},":\\n;",{a:7,w:1.5},""],
[{y:-0.625,x:6.5,h:1.5},"",{x:4.5,h:1.5},""],
[{y:-0.75,x:3.5,a:4},"C",{x:10.5},"<\\n,"],
[{y:-0.875,x:2.5},"X",{x:1},"V",{x:8.5},"M",{x:1},">\\n."],
[{y:-0.875,x:5.5},"B",{x:6.5},"N"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z",{x:14.5},"?\\n/",{a:7,w:1.5},""],
[{y:-0.375,x:3.5},"",{x:10.5},""],
[{y:-0.875,x:2.5},"",{x:1},"",{x:8.5},"",{x:1},""],
[{y:-0.75,x:0.5},"","",{x:14.5},"",""],
[{r:30,rx:6.5,ry:4.25,y:-1,x:1},"",""],
[{h:2},"",{h:2},"",""],
[{x:2},""],
[{r:-30,rx:13,y:-1,x:-3},"",""],
[{x:-3},"",{h:2},"",{h:2},""],
[{x:-3},""]
]"""
        )
        return cls(keyboard)


def main():
    keyboard = Keyboard.get_json_const_03()
    keyboard.bootstrap_convert_keys(0.2)
    keyboard_object = union()

    keyboard_object = keyboard.build_pcb_layer()
    # eyboard_object = keyboard.draw_plate() - keyboard.draw_keys_holes()
    # keyboard_object.add(keyboard.draw_keys_holes())
    keyboard_object.add(keyboard.draw_plate() - keyboard.draw_keys_holes())
    # keyboard_object = keyboard.draw_keys_holes()
    # keyboard_object = keyboard.draw_plate() - keyboard.draw_keys_holes()
    # keyboard_object.add(keyboard.draw_keys_holes())
    scad_render_to_file(keyboard_object)


if __name__ == "__main__":
    main()
