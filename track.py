from src.pixel_tracking import PixelTracker
from src.zone_delimiting import ZoneDelimiter
from src.poi_identifying import PoiIdentifier
from src.poi_tracker import PoiTracker
import argparse


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)

    # General arguments
    parser.add_argument('--camera', type=int, default=0,
                        help='Select the camera peripheral (0 for built-in webcam, 1 for external webcam)')
    parser.add_argument('--item', type=str, required=True,
                        help='Select the type of time to track (pixel, zone or poi)')

    # Specific arguments
    parser.add_argument('--mesh', action='store_true',
                        help='Add a mesh (only for item == zone)')
    parser.add_argument('--n_poi', type=int, default=10,
                        help='Add Points Of Interest (only for item == poi)')
    parser.add_argument('--track', action='store_true',
                        help='Track the Points Of Interest (only for item == poi)')
    return parser.parse_args()


def track(args):
    if args.item == 'pixel':
        PixelTracker(args.camera).main()
    elif args.item == 'zone':
        ZoneDelimiter(args.camera, args.mesh).main()
    elif args.item == 'poi':
        if args.track:
            PoiTracker(args.camera, args.n_poi).main()
        else:
            PoiIdentifier(args.camera, args.n_poi).main()


if __name__ == '__main__':
    track(args=parse_args())
