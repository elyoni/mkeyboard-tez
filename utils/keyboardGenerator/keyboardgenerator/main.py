import pykle_serial as kle_serial  # serial
from solid2 import (
    import_stl,
    union,
    scad_render_to_file,
    polygon,
    color,
    cube,
)
import math

KEY_PATH = "KeySocket.stl"
MX_KEY_SPACING = 19.05  # mm
# MX_KEY_SPACING = MX_KEY_SPACING + MX_KEY_SPACING / 2
MX_KEY_SIZE = 14  # mm

JSON_PATH = ""


def rotate_shape(original_point, center_rotation_point, angle_degrees):
    # Step 1: Translate the shape
    translate_distance = (
        original_point[0] - center_rotation_point[0],
        original_point[1] - center_rotation_point[1],
    )

    # Step 2: Perform the rotation
    angle_radians = math.radians(angle_degrees)
    rotated_point = (
        translate_distance[0] * math.cos(angle_radians)
        - translate_distance[1] * math.sin(angle_radians),
        translate_distance[0] * math.sin(angle_radians)
        + translate_distance[1] * math.cos(angle_radians),
    )

    # Step 3: Translate the shape back
    final_point = (
        rotated_point[0] + center_rotation_point[0],
        rotated_point[1] + center_rotation_point[1],
    )

    return final_point

def build_pcb_layer(keyboard_layout):
    pcb_layer = []
    for key_pos in keyboard_layout.keys:
        new_pos = rotate_shape(
            (key_pos.x, key_pos.y),
            (key_pos.rotation_x, key_pos.rotation_y),
            key_pos.rotation_angle,
        )
        keyboard.append(
            key.rotate(-key_pos.rotation_angle)
            .right(new_pos[0] * MX_KEY_SPACING)
            .back(new_pos[1] * MX_KEY_SPACING)
        )


def main():
    keyboard_layout = read_keyboard_json(JSON_PATH)
    print(type(keyboard_layout))
    key = get_key_socket_stl()
    keyboard = []
    # keyboard.append(calc_plat(keyboard_layout))

    # TODO Need to understand how to work with pykle_serial.serial.Keyboard
    for key_pos in keyboard_layout.keys:
        new_pos = rotate_shape(
            (key_pos.x, key_pos.y),
            (key_pos.rotation_x, key_pos.rotation_y),
            key_pos.rotation_angle,
        )

        keyboard.append(
            key.rotate(-key_pos.rotation_angle)
            .right(new_pos[0] * MX_KEY_SPACING)
            .back(new_pos[1] * MX_KEY_SPACING)
        )
        # if key_pos.rotation_angle > 0:
        # print(key_pos)
        # # print(f"Will be moved in x:{key_pos.x} y: {key_pos.y}")
        # new_pos = rotate_shape(
        # (key_pos.x, key_pos.y),
        # (key_pos.rotation_x, key_pos.rotation_y),
        # key_pos.rotation_angle,
        # )
        # keyboard.append(
        # key.rotate(-key_pos.rotation_angle)
        # .right(new_pos[0] * MX_KEY_SPACING)
        # .back(new_pos[1] * MX_KEY_SPACING)
        # )

        # # keyboard.append(
        # # key.rotateX(
        # # -key_pos.rotation_angle, (0, key_pos.rotation_x, key_pos.rotation_y)
        # # )
        # # .right(key_pos.x * MX_KEY_SPACING)
        # # .back(key_pos.y * MX_KEY_SPACING)
        # # )
        # else:
        # keyboard.append(
        # key.translate((key_pos.rotation_x, key_pos.rotation_y))
        # .rotate(-key_pos.rotation_angle)
        # .right(key_pos.x * MX_KEY_SPACING)
        # .back(key_pos.y * MX_KEY_SPACING)
        # )
        print(f"Will be moved in key_pos {key_pos.rotation_x}, {key_pos.rotation_y}")
        # translate(center)
        # keyboard.append(
        # key.right(key_pos.rotation_x * MX_KEY_SPACING)
        # .back(key_pos.rotation_y * MX_KEY_SPACING)
        # .right(key_pos.x * MX_KEY_SPACING)
        # .back(key_pos.y * MX_KEY_SPACING)
        # .rotate(-key_pos.rotation_angle)
        # # .right(key_pos.x * MX_KEY_SPACING)
        # # .back(key_pos.y * MX_KEY_SPACING)
        # # .right(MX_KEY_SPACING / 2)
        # # .back(MX_KEY_SPACING / 2)
        # # .right(key_pos.x * MX_KEY_SPACING)
        # # .back(key_pos.y * MX_KEY_SPACING)
        # )
        # keyboard.append(
        # key.rotate(-key_pos.rotation_angle)
        # .right(key_pos.x * MX_KEY_SPACING)
        # .back(key_pos.y * MX_KEY_SPACING)
        # # .right(MX_KEY_SPACING / 2)
        # # .back(MX_KEY_SPACING / 2)
        # # .right(key_pos.rotation_x * MX_KEY_SPACING)
        # # .back(key_pos.rotation_y * MX_KEY_SPACING)
        # # .right(key_pos.x * MX_KEY_SPACING)
        # # .back(key_pos.y * MX_KEY_SPACING)
        # )

        # else:
        # keyboard.append(
        # key
        # # .right(key_pos.rotation_x * MX_KEY_SPACING)
        # # .back(key_pos.rotation_y * MX_KEY_SPACING)
        # .rotate(-key_pos.rotation_angle)
        # .right(key_pos.x * MX_KEY_SPACING)
        # .back(key_pos.y * MX_KEY_SPACING)
        # )
        # keyboard.append(
        # # text(text=f"{key_pos.x}:{key_pos.y}", size=3)
        # # .right(key_pos.x * MX_KEY_SPACING + 3)
        # # .back(key_pos.y * MX_KEY_SPACING + 3)
        # # .up(12)
        # )
        # keyboard.append(
        # color("blue", alpha=0.4)(
        # cube([14, 14, 6], center=True)
        # .right(MX_KEY_SPACING / 2)
        # .back(MX_KEY_SPACING / 2)
        # .rotate(-key_pos.rotation_angle)
        # .right(key_pos.x * MX_KEY_SPACING)
        # .back(key_pos.y * MX_KEY_SPACING)
        # .up(9)
        # )
        # )
        keyboard.append(
            color("blue", alpha=0.4)(
                cube([14, 14, 6], center=True)
                .right(MX_KEY_SPACING / 2)
                .back(MX_KEY_SPACING / 2)
                .translate((key_pos.rotation_x, key_pos.rotation_y))
                .rotate(-key_pos.rotation_angle)
                .right(key_pos.x * MX_KEY_SPACING)
                .back(key_pos.y * MX_KEY_SPACING)
                .up(9)
            )
        )

    print(f"x:{key_pos.x} y:{key_pos.y}")

    c = union()(keyboard)
    scad_render_to_file(c)
    # total_width = 0
    # for key in keyboard.keys:
    # total_width += key.width
    # print(key)
    # print(total_width)


def calc_plat(keyboard_layout):
    from scipy.spatial import ConvexHull
    import numpy as np

    points_raw = []
    for key_pos in keyboard_layout.keys:
        points_raw.append((key_pos.x, key_pos.y))

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
        points.append((_x * MX_KEY_SIZE * 2, _y * MX_KEY_SIZE * 2))
    plate = polygon(points)

    # center_x = sum(p[0] for p in points) / len(points)
    # center_y = sum(p[1] for p in points) / len(points)

    # my_centered_polygon = translate([center_x, center_y, 0])(plate)
    return color("red")(plate)


def get_key_socket_stl():
    key = import_stl(KEY_PATH, convexity=3)

    key = key.translate((MX_KEY_SPACING / 2, -MX_KEY_SPACING / 2))
    # key = key.right(MX_KEY_SPACING / 2).back(MX_KEY_SPACING / 2)

    return key
    # return key.root()

    # key = key.rotateX(90).right(MX_KEY_SPACING / 2).forward(MX_KEY_SPACING / 2)

    key = cube([MX_KEY_SPACING, MX_KEY_SPACING, 2])

    return key


def read_keyboard_json(json_path: str) -> dict:
    # NOTE To the output of the json we need to add [] around the all information
    keyboard = kle_serial.parse(
        """[
[{y:0.375,a:7,w:1.5},""],
[{w:1.5},""],
[{w:1.5},""],
[{w:1.5},""],
[{y:0.005,x:0.25},""]
        ]"""
    )
    # keyboard = serial.parse(
    # # """[
    # # {
    # # "a": 1
    # # },
    # # [
    # # {
    # # "a": 5
    # # },
    # # "a",
    # # "b",
    # # "c"
    # # ],
    # # [
    # # "d",
    # # "e",
    # # "f"
    # # ],
    # # [
    # # "1",
    # # "2",
    # # "3"
    # # ]
    # # ]"""
    # )
    return keyboard


if __name__ == "__main__":
    main()
