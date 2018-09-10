from PIL import Image
import os
from random import randint
import argparse

parser = argparse.ArgumentParser("map_from_bitmap")
parser.add_argument(
    "filename", help="the name of the input image excluding .bmp")
parser.add_argument("-s", "--spawns", nargs="+", type=int,
                    default=[0], help="Create random spawns. default is 0")
args = parser.parse_args()
filename = args.filename
spawns = tuple(args.spawns) if len(
    args.spawns) == 2 else tuple(args.spawns * 2)
assert len(spawns) == 2, spawns


class MapFromBitmap:
    """Create a .txt map file from a .bmp bitmap file
    The .bmp must be in the /assets/Tools/bitmaps/ folder
    Run the file from /assets/Tools/
    The .txt is called output.txt and is placed in /assets/Tools/

    Params:
    str filename_: the name of the .bmp excluding .bmp
    tuple[int] num_spawns: a tuple where the first is the number of
        zombie spawns and the second is pickup spawns

    Raises:
    RuntimeError if .create() is run more than once

    """
    blacks = {0, (0, 0, 0), (0, 0, 0, 0)}  # Some files hsave different values
    # for black. This is monochrome, RGB, and RGBA respectivly
    cwd = os.getcwd()  # current working directory

    def __init__(self, filename_, num_spawns=(5, 5)):
        img_path = MapFromBitmap.cwd + "/bitmaps/{}.bmp".format(filename_)
        self.img = Image.open(img_path)
        self.output_path = MapFromBitmap.cwd + "/output.txt"
        self.new_file = open(self.output_path, mode="w")
        self.width, self.height = self.img.size
        self.num_spawns = num_spawns
        assert sum(num_spawns) <= self.width * self.height
        self.z_spawns, self.p_spawns = self.get_spawns()
        self.as_str = ""

    @classmethod
    def test(cls, num_spawns=(2, 3)):
        return cls("Test", num_spawns)

    def get_spawns(self):
        taken_spawns = []
        for num_spawn in self.num_spawns:
            current_spawns = []
            while len(current_spawns) < num_spawn:
                rnd_num = randint(0, self.width * self.height - 1)
                coordinate = divmod(rnd_num, self.height)
                if (not is_black(self.img.getpixel(coordinate)) and
                        coordinate not in taken_spawns):
                    current_spawns.append(coordinate)
                    taken_spawns.append(coordinate)
            yield current_spawns

    def create_file(self):
        if self.as_str:
            raise RuntimeError("Already created file")
        for i in range(self.height * self.width):
            y, x = coordinate = divmod(i, self.width)
            pixel = self.img.getpixel(coordinate)
            tile = "#" if is_black(pixel) else "."
            if coordinate in self.z_spawns:
                tile = "Z"
            elif coordinate in self.p_spawns:
                tile = "P"
            self.new_file.write(tile)
            if (i + 1) % self.width == 0:
                self.new_file.write("\n")

        self.new_file.close()
        self.img.close()
        with open(self.output_path, mode="r") as file:
            self.as_str = file.read()
        if self.num_spawns == (0, 0):
            print("don't forget to add zombie and pickup spawn points!")

    def display(self):
        print(self.as_str)


def is_black(pixel) -> bool:
    return pixel in MapFromBitmap.blacks


if __name__ == "__main__":
    a = MapFromBitmap(filename, spawns)
    a.create_file()
    a.display()
