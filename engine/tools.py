from engine.triangle import Triangle


def intersect_plane(plane_p, plane_n, l_start, l_end):
    plane_n = plane_n.normalise()
    plane_d = plane_n.dot(plane_p)
    ad = l_start.dot(plane_n)
    bd = l_end.dot(plane_n)
    t = (plane_d - ad) / (bd - ad)
    l_full = l_end - l_start
    l_intersect = l_full * t
    return l_start + l_intersect

def dist(p, plane_p, plane_n):
    return (plane_n.x * p.x + plane_n.y * p.y + plane_n.z * p.z - plane_n.dot(plane_p))

def clip_tri_by_plane(plane_p, plane_n, in_tri, debug=True):
    plane_n = plane_n.normalise()

    inside_points = []
    outside_points = []

    d = [dist(in_tri.vertices[i], plane_p, plane_n) for i in range(3)]

    for i in range(3):
        if d[i] > 0:
            inside_points.append(in_tri.vertices[i])
        else:
            outside_points.append(in_tri.vertices[i])


    if len(inside_points) == 0:
        return []

    if len(inside_points) == 3:
        return [in_tri]

    if len(inside_points) == 1 and len(outside_points) == 2:
        out = []

        out.append(Triangle(
            inside_points[0],
            intersect_plane(plane_p, plane_n, inside_points[0], outside_points[0]),
            intersect_plane(plane_p, plane_n, inside_points[0], outside_points[1]),
            col=in_tri.col
        ))

        if debug: out[0].col = (255,0,0)

        return out

    if len(inside_points) == 2 and len(outside_points) == 1:
        out = []

        out.append(Triangle(
            inside_points[0],
            inside_points[1],
            intersect_plane(plane_p, plane_n, inside_points[0], outside_points[0]),
            col=in_tri.col
        ))

        out.append(Triangle(
            inside_points[1],
            out[0].vertices[2],
            intersect_plane(plane_p, plane_n, inside_points[1], outside_points[0]),
            col=in_tri.col
        ))

        if debug: out[0].col = (0, 255, 0)
        if debug: out[1].col = (0, 0, 255)

        return out