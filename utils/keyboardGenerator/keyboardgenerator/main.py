import pykle_serial as serial
from solid2 import import_stl, union, scad_render_to_file, polygon, color, cube, text

KEY_PATH = "KeySocket.stl"
MX_KEY_SPACING = 19.05  # mm
MX_KEY_SIZE = 14  # mm

JSON_PATH = ""


def main():
    keyboard_layout = read_keyboard_json(JSON_PATH)
    print(type(keyboard_layout))
    key = get_key_socket()
    keyboard = []
    # keyboard.append(calc_plat(keyboard_layout))

    # TODO Need to understand how to work with pykle_serial.serial.Keyboard
    for key_pos in keyboard_layout.keys:
        keyboard.append(
            key.right(key_pos.x * MX_KEY_SPACING).back(key_pos.y * MX_KEY_SPACING)
        )
        # keyboard.append(
        # # text(text=f"{key_pos.x}:{key_pos.y}", size=3)
        # # .right(key_pos.x * MX_KEY_SPACING + 3)
        # # .back(key_pos.y * MX_KEY_SPACING + 3)
        # # .up(12)
        # )
        keyboard.append(
            color("blue", alpha=0.4)(
                cube([14, 14, 6], center=True)
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


def get_key_socket():
    key = import_stl(KEY_PATH, convexity=3)
    return key
    # return key.root()

    # key = key.rotateX(90).right(MX_KEY_SPACING / 2).forward(MX_KEY_SPACING / 2)

    key = cube([MX_KEY_SPACING, MX_KEY_SPACING, 2])

    return key


def read_keyboard_json(json_path: str) -> dict:
    # NOTE To the output of the json we need to add [] around the all information
    keyboard = serial.parse(
        """[
            [{a:7},"00","01","02"],
["10","11"],
[{r:30,y:-1.5,x:3.25},"02"]
]
            """
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
