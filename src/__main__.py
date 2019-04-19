"""Zombie Survival game in Pygame"""
import sys
import os
import pathlib
src_path = pathlib.Path(os.path.realpath(__file__).replace("__main__.py", ""))
sys.path.insert(0, str(src_path))
os.chdir(src_path.parent)
if __name__ == '__main__':
    import main
    main.main()
