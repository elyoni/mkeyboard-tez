from keyboardgenerator.base import Point, Part


class Key(Part):
    pos: Point
    pos_spacing: Point
    corners: tuple[Point, Point, Point, Point]
    corners_spacing: tuple[Point, Point, Point, Point]
    rotation_angle: float  # Degrees
    center_rotation_point: Point
    spacing: Point
    height: float
    width: float
    key_boarder: float  # in key units

    def __init__(self, key: kle_serial.Key, key_boarder: float = 0) -> None:
        self.spacing = Point(
            MX_KEY_SPACING,  # In the future need to collect this data from the Json file
            MX_KEY_SPACING,
        )
        self.key_boarder = key_boarder
        self.key_origin = key
        self.pos = Point(key.x, key.y)
        self.center_rotation_point = Point(key.rotation_x, key.rotation_y)
        self.rotation_angle = key.rotation_angle

        # Set to the center of the key
        if key.width > 0 or key.height > 0:
            self.pos.x += key.width / 2
            self.pos.y += key.height / 2

        self.height = key.height
        self.width = key.width

        self.calcuate_corners(key_boarder)

        # Calculate the center
        if key.rotation_angle != 0:
            self.pos = self.calc_rotate_xy(self.pos, self.center_rotation_point)
        self.pos_spacing = self.pos * self.spacing

    def draw_key_hold(self) -> OpenSCADObject:
        try:
            return (
                cube(self.spacing.x, self.spacing.y, 8, center=True)
                .rotate(-self.rotation_angle)
                .translate(self.pos_spacing.x, -self.pos_spacing.y)
                .down(1)
            )
        except Exception:
            print(type(self.pos_spacing.x), type(self.pos_spacing.y))
            raise

    def calcuate_corners(self, key_boarder):
        self.corners = (
            Point(
                self.pos.x - (self.width / 2 + key_boarder),
                self.pos.y + (self.height / 2 + key_boarder),
            ),
            Point(
                self.pos.x - (self.width / 2 + key_boarder),
                self.pos.y - (self.height / 2 + key_boarder),
            ),
            Point(
                self.pos.x + (self.width / 2 + key_boarder),
                self.pos.y + (self.height / 2 + key_boarder),
            ),
            Point(
                self.pos.x + (self.width / 2 + key_boarder),
                self.pos.y - (self.height / 2 + key_boarder),
            ),
        )

        self.corners_spacing = (
            self.corners[0] * self.spacing,
            self.corners[1] * self.spacing,
            self.corners[2] * self.spacing,
            self.corners[3] * self.spacing,
        )

        if self.rotation_angle != 0:
            self.corners_spacing = (
                self.calc_rotate_xy(
                    self.corners_spacing[0], self.center_rotation_point * self.spacing
                ),
                self.calc_rotate_xy(
                    self.corners_spacing[1], self.center_rotation_point * self.spacing
                ),
                self.calc_rotate_xy(
                    self.corners_spacing[2], self.center_rotation_point * self.spacing
                ),
                self.calc_rotate_xy(
                    self.corners_spacing[3], self.center_rotation_point * self.spacing
                ),
            )
