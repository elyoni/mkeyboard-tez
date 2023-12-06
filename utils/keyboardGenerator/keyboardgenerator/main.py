import pykle_serial as kle_serial

# from pykle_serial.serial import Keyboard as KleKeyboard

# from key import Key
# from solid2.core.object_base import OpenSCADObject

# from scipy.spatial import ConvexHull
# import numpy as np
# from solid2 import (
# import_stl,
# union,
# polygon,
# color,
# )

from keyboardgenerator.base import Keyboard

KEY_PATH = "keyboardgenerator/KeySocket.stl"


def main():
    keyboard = Keyboard.from_kle_obj(get_json_const_03())
    keyboard10 = Keyboard.from_kle_obj(get_json_const_03())
    # keyboard = Keyboard.from_kle_obj(get_json_const_ergodox())
    (keyboard.draw_pcb() + keyboard10.draw_pcb_10()).save_as_scad("pcb.scad")
    # keyboard.draw_plate().save_as_scad("plate.scad")
    # keyboard_kle = get_json_const_03()
    # key_stl = import_stl(KEY_PATH, convexity=3).translate(
    # 19.05 / 2, 19.05 / 2, 0.55
    # )  # will move into key.py
    # keys_list: list[
    # Part
    # ] = []  # Should be replace by parts, because this list will also contain Arduino
    # for key_orig in keyboard_kle.keys:
    # keys_list.append(Key.from_kle_serial(key_orig, key_stl))
    # pcb_obj = union()
    # pcb_obj_footprint = union()
    # corents_list = []
    # for key_obj in keys_list:
    # pcb_obj += key_obj.draw_pcb()
    # # for cor in key_obj.calculate_corners():
    # # corents_list.append(cor.get_tuple())
    # pcb_obj_footprint += key_obj.draw_pcb_footprint()
    # print(corents_list)
    # plate = draw_plate(corents_list)
    # # print(plate.hull)
    # # plate_pcb = plate - pcb_obj_footprint
    # # plate_pcb_final = plate_pcb + pcb_obj
    # plate_pcb_final = pcb_obj + plate

    # plate_pcb_final.save_as_scad("nettt.scad")

    # print(corents_list)
    # pcb_obj.save_as_scad("nettt.scad")


# def draw_plate(points_raw) -> OpenSCADObject:
# # Convert the points_raw to a NumPy array for compatibility with ConvexHull
# points_array = np.array(points_raw)
# # Calculate the convex hull
# hull = ConvexHull(points_array)
# # Extract the vertices of the convex hull
# hull_points = points_array[hull.vertices]

# # Close the shape by adding the first point at the end
# hull_points = np.append(hull_points, [hull_points[0]], axis=0)
# # self.position = position.calc_rotate_xy(rotation_center, rotation_degree)

# # Extract x and y coordinates from the hull points
# points = []
# x, y = zip(*hull_points)
# for _x, _y in zip(x, y):
# points.append((_x, _y))
# plate = polygon(points)

# # my_centered_polygon = translate([center_x, center_y, 0])(plate)
# return color("red")(plate.linear_extrude(height=1.3))


def get_json_const_ergodox() -> kle_serial.Keyboard:
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
    return keyboard


def get_json_const_02() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
["Num Lock","/"],
["7\\nHome"],
[{r:45,rx:1,ry:1,y:-0.5},"8\\n↑"]
]"""
    )
    return keyboard


def get_json_const_03() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
    [{r:45,rx:1,ry:1,y:-0.5},"8\\n↑"]
    ]"""
    )

    return keyboard


if __name__ == "__main__":
    main()
