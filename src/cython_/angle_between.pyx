"""Cython code for functions that are important to run fast
Pure python version is run if import fail"""


cdef extern from "<math.h>" nogil:
    double pi "M_PI"
    double atan2(double y, double x)
    double sqrt(double x)


cpdef double angle_between(int x1, int y1, int x2, int y2):
    """Get angle of the hypotenuse to the adjecent side of v1 in a
    rigth triangle where v1 and v2 are the non-right angled corners

          v2
         / |
        /  |
       /   |
      /θ   |
    v1------

    >>> v1, v2 = Vector(1, 5), Vector(8, 0)
    >>> angle_between(v1, v2)
    0.6202494859828215

    NB: Takes in mind pygame's flipped y-axis
    angles appears anti-clockwise on normal coordinate systems
    Examples:
    >>> angle_between(Vector(1, 0), Vector(1, 1))
    4.71238898038469
    >>> angle_between(Vector(1, 1), (2, 0))
    0.7853981633974483

    :return the angle in radians. No negative angles"""
    return atan2(y1 - y2, x2 - x1) % (2 * pi)