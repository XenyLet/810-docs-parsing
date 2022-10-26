def minmax_coords_to_xywh(x_min, y_min, x_max, y_max):
    return x_min, y_min, x_max-x_min, y_max-y_min

def get_absolute_coords(
        absolute_root_coords,
        relative_from_root_coords
):
    """
    absolute_root_coords - coordinates of root on image (from upper-left corner)
        example:[xmin, y_min, w, h]
    relative_from_root_coords - coordinates relative to root
        example:[xmin, y_min, w, h]
    """
    x_min_abs, y_min_abs = absolute_root_coords[:2]
    x_min_rel, y_min_rel, w, h = relative_from_root_coords
    return x_min_abs+x_min_rel, y_min_abs+y_min_rel, w, h