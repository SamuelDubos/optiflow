from src.pixel_tracking import PixelTracker
from src.zone_tracking import ZoneTracker
import sys


if __name__ == '__main__':
    ITEM = sys.argv[1]
    CAMERA = int(sys.argv[2])
    MESH = True if ITEM == 'zone' and len(sys.argv) >= 4 and sys.argv[3] == 'mesh' else False
    if ITEM == 'pixel':
        PixelTracker(CAMERA).main()
    elif ITEM == 'zone':
        ZoneTracker(CAMERA).main(MESH)
