import pykle_serial as kle_serial
import os

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
    keyboard_plate = Keyboard.from_kle_obj(get_json_const_ergodox_arduino_pin01())
    keyboard_pcb = Keyboard.from_kle_obj(get_json_const_ergodox_arduino_pin01())
    keyboard_bottom = Keyboard.from_kle_obj(get_json_const_ergodox_arduino_pin01())

    pcb = keyboard_pcb.draw_pcb_add()
    plate = keyboard_plate.draw_plate()
    bottom = keyboard_bottom.draw_bottom()

    pcb.save_as_scad("pcb.scad")
    plate.save_as_scad("plate.scad")
    bottom.save_as_scad("bottom.scad")

    # .save_as_scad("pcb.scad")
    # keyboard_bottom.draw_bottom().save_as_scad("bottom.scad")

    (pcb.color("gray") + plate.up(40) + bottom.down(40).color("blue")).save_as_scad(
        "keyboard.scad"
    )
    # (
    # keyboard_pcb.draw_pcb().color("gray")
    # + keyboard_plate.draw_plate().up(40)
    # + keyboard_bottom.draw_bottom().down(40)
    # ).save_as_scad("all.scad")
    print("Created new scad files")

    print("\tpcb scad file", os.path.abspath("pcb.scad"))
    print("\tplate scad file", os.path.abspath("plate.scad"))

    print("done")


def get_json_const_ergodox() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
[{x:3.5},"#\\n3",{x:10.5},"*\\n8"],
[{y:-0.875,x:2.5},"@\\n2",{x:1},"$\\n4",{x:8.5},"&\\n7",{x:1},"(\\n9"],
[{y:-0.875,x:5.5},"%\\n5","LS0",{x:4.5},"RS0","^\\n6"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"!\\n1",{x:14.5},")\\n0",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"E",{x:10.5},"I"],
[{y:-0.875,x:2.5},"W",{x:1},"R",{x:8.5},"U",{x:1},"O"],
[{y:-0.875,x:5.5},"T",{h:1.5},"LS1",{x:4.5,h:1.5},"RS1","Y"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q",{x:14.5},"P",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"D",{x:10.5},"K"],
[{y:-0.875,x:2.5},"S",{x:1},"F",{x:8.5},"J",{x:1},"L"],
[{y:-0.875,x:5.5},"G",{x:6.5},"H"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A",{x:14.5},":\\n;",{a:7,w:1.5},""],
[{y:-0.625,x:6.5,a:4,h:1.5},"LS2",{x:4.5,h:1.5},"RS2"],
[{y:-0.75,x:3.5},"C",{x:10.5},"<\\n,"],
[{y:-0.875,x:2.5},"X",{x:1},"V",{x:8.5},"M",{x:1},">\\n."],
[{y:-0.875,x:5.5},"B",{x:6.5},"N"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z",{x:14.5},"?\\n/",{a:7,w:1.5},""],
[{y:-0.375,x:3.5},"",{x:10.5},""],
[{y:-0.875,x:2.5},"",{x:1},"",{x:8.5},"",{x:1},""],
[{y:-0.75,x:0.5},"","",{x:14.5},"",""],
[{r:30,rx:6.5,ry:4.25,y:-1,x:1,a:4},"LU0","LU1"],
[{h:2},"LB0",{h:2},"LB1","LB2"],
[{x:2},"LB3"],
[{r:-30,rx:13,y:-1,x:-3},"RU1","RU0"],
[{x:-3},"RB2",{h:2},"RB1",{h:2},"RB0"],
[{x:-3},"RB3"]
]"""
    )
    return keyboard


def get_json_const_ergodox_arduino() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
[{x:3.5},"#\\n3",{x:10.5},"*\\n8"],
[{y:-0.875,x:2.5},"@\\n2",{x:1},"$\\n4",{x:8.5},"&\\n7",{x:1},"(\\n9"],
[{y:-0.875,x:5.5},"%\\n5","LS0",{x:0.25,a:7,w:1.5,h:2.75},"\\n\\n\\n\\nArduino",{x:2.75,a:4},"RS0","^\\n6"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"!\\n1",{x:14.5},")\\n0",{a:7,w:1.5},""],
[{y:-0.495,x:10.25,w:1.5,h:2.75},"\\n\\n\\n\\nArduino"],
[{y:-0.88,x:3.5,a:4},"E",{x:10.5},"I"],
[{y:-0.875,x:2.5},"W",{x:1},"R",{x:8.5},"U",{x:1},"O"],
[{y:-0.875,x:5.5},"T",{h:1.5},"LS1",{x:4.5,h:1.5},"RS1","Y"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q",{x:14.5},"P",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"D",{x:10.5},"K"],
[{y:-0.875,x:2.5},"S",{x:1},"F",{x:8.5},"J",{x:1},"L"],
[{y:-0.875,x:5.5},"G",{x:6.5},"H"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A",{x:14.5},":\\n;",{a:7,w:1.5},""],
[{y:-0.625,x:6.5,a:4,h:1.5},"LS2",{x:4.5,h:1.5},"RS2"],
[{y:-0.75,x:3.5},"C",{x:10.5},"<\\n,"],
[{y:-0.875,x:2.5},"X",{x:1},"V",{x:8.5},"M",{x:1},">\\n."],
[{y:-0.875,x:5.5},"B",{x:6.5},"N"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z",{x:14.5},"?\\n/",{a:7,w:1.5},""],
[{y:-0.375,x:3.5},"",{x:10.5},""],
[{y:-0.875,x:2.5},"",{x:1},"",{x:8.5},"",{x:1},""],
[{y:-0.75,x:0.5},"","",{x:14.5},"",""],
[{r:30,rx:6.5,ry:4.25,y:-1,x:1,a:4},"LU0","LU1"],
[{h:2},"LB0",{h:2},"LB1","LB2"],
[{x:2},"LB3"],
[{r:-30,rx:13,y:-1,x:-3},"RU1","RU0"],
[{x:-3},"RB2",{h:2},"RB1",{h:2},"RB0"],
[{x:-3},"RB3"]

]"""
    )
    return keyboard


def get_json_const_ergodox_arduino02() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
{ name: "tez", switchType:"CherryMx", notes: 10},
[{x:3.5},"#\\n3",{x:10.5},"*\\n8"],
[{y:-0.875,x:2.5},"@\\n2",{x:1},"$\\n4",{x:8.5},"&\\n7",{x:1},"(\\n9"],
[{y:-0.875,x:5.5},"%\\n5","LS0",{x:0.25,a:7,w:1.5,h:2.75},"\\n\\n\\n\\nArduino",{x:2.75,a:4},"RS0","^\\n6"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"!\\n1",{x:14.5},")\\n0",{a:7,w:1.5},""],
[{y:-0.495,x:10.25,w:1.5,h:2.75},"\\n\\n\\n\\nArduino"],
[{y:-0.88,x:3.5,a:4},"E",{x:10.5},"I"],
[{y:-0.875,x:2.5},"W",{x:1},"R",{x:8.5},"U",{x:1},"O"],
[{y:-0.875,x:5.5},"T",{h:1.5},"LS1",{x:4.5,h:1.5},"RS1","Y"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q",{x:14.5},"P",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"D",{x:10.5},"K"],
[{y:-0.875,x:2.5},"S",{x:1},"F",{x:8.5},"J",{x:1},"L"],
[{y:-0.875,x:5.5},"G",{x:6.5},"H"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A",{x:14.5},":\\n;",{a:7,w:1.5},""],
[{y:-0.625,x:6.5,a:4,h:1.5},"LS2",{x:4.5,h:1.5},"RS2"],
[{y:-0.75,x:3.5},"C",{x:10.5},"<\\n,"],
[{y:-0.875,x:2.5},"X",{x:1},"V",{x:8.5},"M",{x:1},">\\n."],
[{y:-0.875,x:5.5},"B",{x:6.5},"N"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z",{x:14.5},"?\\n/",{a:7,w:1.5},""],
[{y:-0.375,x:3.5},"",{x:10.5},""],
[{y:-0.875,x:2.5},"",{x:1},"",{x:8.5},"",{x:1},""],
[{y:-0.75,x:0.5},"","",{x:14.5},"",""],
[{r:30,rx:6.5,ry:4.25,y:-1,x:1,a:4},"LU0","LU1"],
[{h:2},"LB0",{h:2},"LB1","LB2"],
[{x:2},"LB3"],
[{r:-30,rx:13,y:-1,x:-3},"RU1","RU0"],
[{x:-3},"RB2",{h:2},"RB1",{h:2},"RB0"],
[{x:-3},"RB3"]
]"""
    )
    return keyboard


def get_json_const_ergodox_arduino_pin01() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
[{x:3.5},"#/3",{x:10.5},"*/8"],
[{y:-0.875,x:2.5},"@/2",{x:1},"$/4",{x:8.5},"&/7",{x:1},"(/9"],
[{y:-0.875,x:5.5},"%/5","LS0",{x:0.25,a:7,w:1.5,h:2.75},"\\n\\n\\n\\nArduino",{x:2.75,a:4},"RS0","^/6"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"!/1",{x:14.5},")/0",{a:7,w:1.5},""],
[{y:-0.495,x:5.25,a:4,w:0.5,h:0.5},"pin\\n\\n\\n\\nPinPlate",{x:4.5,a:7,w:1.5,h:2.75},"\\n\\n\\n\\nArduino",{x:4,a:4,w:0.5,h:0.5},"pin\\n\\n\\n\\nPinPlate"],
[{y:-0.88,x:3.5},"E",{x:10.5},"I"],
[{y:-0.875,x:2.5},"W",{x:1},"R",{x:8.5},"U",{x:1},"O"],
[{y:-0.995,x:2.25,w:0.5,h:0.5},"pin\\n\\n\\n\\nPinPlate",{x:10,w:0.5,h:0.5},"pin\\n\\n\\n\\nPinPlate"],
[{y:-0.88,x:5.5},"T",{h:1.5},"LS1",{x:4.5,h:1.5},"RS1","Y"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q",{x:14.5},"P",{a:7,w:1.5},""],
[{y:-0.375,x:3.5,a:4},"D",{x:10.5},"K"],
[{y:-0.875,x:2.5},"S",{x:1},"F",{x:8.5},"J",{x:1},"L"],
[{y:-0.875,x:5.5},"G",{x:6.5},"H"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A",{x:14.5},":\\\\n;",{a:7,w:1.5},""],
[{y:-0.625,x:5.25,a:4,w:0.5,h:0.5},"\\n\\n\\n\\nPinPlate",{x:0.75,h:1.5},"LS2",{x:4.5,h:1.5},"RS2",{x:2.75,w:0.5,h:0.5},"\\n\\n\\n\\nPinPlate"],
[{y:-0.75,x:2.25,w:0.5,h:0.5},"\\n\\n\\n\\nPinPlate",{x:0.75},"C",{x:8.25,w:0.5,h:0.5},"\\n\\n\\n\\nPinPlate",{x:1.75},"<\\\\n,"],
[{y:-0.875,x:2.5},"X",{x:1},"V",{x:8.5},"M",{x:1},">/."],
[{y:-0.875,x:5.5},"B",{x:6.5},"N"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z",{x:14.5},"?//",{a:7,w:1.5},""],
[{y:-0.375,x:3.5},"",{x:10.5},""],
[{y:-0.875,x:2.5},"",{x:1},"",{x:8.5},"",{x:1},""],
[{y:-0.75,x:0.5},"","",{x:14.5},"",""],
[{r:30,rx:6.5,ry:4.25,y:-1,x:1,a:4},"LU0","LU1"],
[{h:2},"LB0",{h:2},"LB1","LB2"],
[{x:2},"LB3"],
[{r:-30,rx:13,y:-1,x:-3},"RU1","RU0"],
[{x:-3},"RB2",{h:2},"RB1",{h:2},"RB0"],
[{x:-3},"RB3"]
]"""
    )
    return keyboard


def get_json_const_ergodox_arduino_pin02() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
        [{x:3.5},"#/3"],
[{y:-0.875,x:2.5},"@/2",{x:1},"$/4"],
[{y:-0.875,x:5.5},"%/5","LS0",{x:0.25,a:7,w:1.5,h:2.75},"\\n\\n\\n\\nArduino"],
[{y:-0.875,w:1.5},"",{a:4},"!/1"],
[{y:-0.495,x:5.25,w:0.5,h:0.5},"pin\\n\\n\\n\\nplatepin"],
[{y:-0.88,x:3.5},"E"],
[{y:-0.875,x:2.5},"W",{x:1},"R"],
[{y:-0.995,x:2.25,w:0.5,h:0.5},"Pin\\n\\n\\n\\nplatepin"],
[{y:-0.88,x:5.5},"T",{h:1.5},"LS1"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Q"],
[{y:-0.375,x:3.5},"D"],
[{y:-0.875,x:2.5},"S",{x:1},"F"],
[{y:-0.875,x:5.5},"G"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"A"],
[{y:-0.625,x:5.25,w:0.5,h:0.5},"pin\\n\\n\\n\\nplatepin",{x:0.75,h:1.5},"LS2"],
[{y:-0.75,x:2.25,w:0.5,h:0.5},"pin\\n\\n\\n\\nplatepin",{x:0.75},"C"],
[{y:-0.875,x:2.5},"X",{x:1},"V"],
[{y:-0.875,x:5.5},"B"],
[{y:-0.875,a:7,w:1.5},"",{a:4},"Z"],
[{y:-0.375,x:3.5,a:7},""],
[{y:-0.875,x:2.5},"",{x:1},""],
[{y:-0.75,x:0.5},"",""]
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


def get_json_const_04() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
["Num Lock"],
[{r:45,rx:1,ry:1,y:-0.5},"8\\n↑"]
    ]"""
    )
    return keyboard


def get_json_const_05() -> kle_serial.Keyboard:
    keyboard = kle_serial.parse(
        """[
["Num Lock"],
    ]"""
    )
    return keyboard


if __name__ == "__main__":
    main()
