from src.pixel_tracking import PixelTracker
from src.zone_tracking import ZoneTracker
import sys


if __name__ == '__main__':
    ITEM = sys.argv[1]
    MESH = True if ITEM == 'zone' and len(sys.argv) >= 3 and sys.argv[2] == 'mesh' else False
    if ITEM == 'pixel':
        PixelTracker().main()
    elif ITEM == 'zone':
        ZoneTracker().main(MESH)
