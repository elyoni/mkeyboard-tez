from solid import import_stl

KEY_PATH = "1_X_Kailh_Socket_Holder.stl"


def get_key_socket():
    key = import_stl(KEY_PATH, convexity=3)
    return key


# keyboard = []
# for i in range(10):
# keyboard.append(up(i * 10)(key))

# Deprecated, and will raise a warning. But that seems like correct behavior
# until OpenSCAD actually makes dxf_linear_extrude() illegal.
# a = dxf_linear_extrude(file=PATH, height=HEIGHT)
# c = union()(keyboard)
# scad_render_to_file(c)

# The future-proof way:
# a = import_(file=PATH)  # or: a = import_dxf(file=PATH)
# b = linear_extrude(height=HEIGHT)(a)
