from src.pixel_tracking import PixelTracker
from src.zone_tracking import ZoneTracker
import argparse


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--camera', type=int, default=0,
                        help='Select the camera peripheral (0 for built-in webcam, 1 for external webcam)')
    parser.add_argument('--item', type=str, required=True,
                        help='Select the type of time to track (pixel or zone)')
    parser.add_argument('--mesh', action='store_true',
                        help='Add a mesh (only for item == zone)')
    return parser.parse_args()


def track(args):
    if args.item == 'pixel':
        PixelTracker(args.camera).main()
    elif args.item == 'zone':
        ZoneTracker(args.camera).main(args.mesh)


if __name__ == '__main__':
    track(args=parse_args())
