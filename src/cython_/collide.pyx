cpdef bint collide(int x1, int y1, int w1, int h1, int x2, int y2, int w2, int h2):
    """Return True if self and other overlap else False
       Returns False if self and other are side by side

       Examples:
       True if self and other partially covers eachother
       >>> a = BaseClass(x=0, y=0, width=10, height=10)
       >>> b = BaseClass(x=9, y=9, width=10, height=10)
       >>> a.collide(b)
       True
       >>> b.collide(a)
       True

       True if self and other are identical
       >>> a = BaseClass(x=0, y=0, width=None, height=None)
       >>> a.collide(a)
       True

       True if self or other entirely incaptures the other
       >>> a = BaseClass(x=0, y=0, width=3, height=3)
       >>> b = BaseClass(x=1, y=1, width=1, height=1)
       >>> a.collide(b)
       True
       >>> b.collide(a)
       True

       False if self and other are side by side
       >>> a = BaseClass(x=0, y=0, width=10, height=10)
       >>> b = BaseClass(x=10, y=0, width=10, height=10)
       >>> a.collide(b)
       False
       >>> b.collide(a)
       False"""
    return ((x1 + w1 > x2) and (y1 < y2 + h2) and
            (y1 + h1 > y2) and (x1 < x2 + w2))
