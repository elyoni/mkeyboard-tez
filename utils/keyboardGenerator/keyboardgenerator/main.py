import pykle_serial as kle_serial
from key import Key
from solid2 import OpenSCADObject, cube, union, import_stl


def main():
    KEY_PATH = "keyboardgenerator/KeySocket.stl"
    keyboard_kle = get_json_const_02()
    key_stl = import_stl(KEY_PATH, convexity=3).up(0.55)
    keys_list = []
    for key_orig in keyboard_kle.keys:
        keys_list.append(Key.from_kle_serial(key_orig, key_stl))
    pcb_obj = union()
    for key_obj in keys_list:
        pcb_obj += key_obj.draw_pcb()
    pcb_obj.save_as_scad("nettt.scad")


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


def get_json_const_02():
    keyboard = kle_serial.parse(
        """[
[{a:7},"Tab"],
[{r:30,y:-1,x:2},"A"]
]"""
    )
    return keyboard


if __name__ == "__main__":
    main()
