"""
Main Module

Author: @SamuelDubos
Date: January 24, 2024
"""

import argparse

from src.pixel_tracking import PixelTracker
from src.zone_delimiting import ZoneDelimiter
from src.poi_identifying import PoiIdentifier
from src.poi_tracker import PoiTracker
from seq.matcher import Photographer, PhotographsMatcher


class Tracker:
    """
    The Tracker class handles command-line arguments and initiates the appropriate tracking mechanism.

    Attributes:
        args (Namespace): Parsed command-line arguments

    Methods:
        parse_args(): Parses command-line arguments using argparse.
        main(): Handles the parsed arguments and initiates the corresponding tracking mechanism.
    """

    def __init__(self):
        self.args = self.parse_args

    @property
    def parse_args(self):
        """
        Parse the command-line arguments.

        Returns:
            Namespace: Parsed command-line arguments
        """
        parser = argparse.ArgumentParser(add_help=True)

        # General arguments
        parser.add_argument('--camera', type=int, default=0,
                            help='Select the camera peripheral '
                                 '(0 for built-in webcam, 1 for external webcam)')
        parser.add_argument('--item', type=str, default='poi',
                            help='Select the type of time to track (pixel, zone, or poi)')

        # Specific arguments
        parser.add_argument('--mesh', action='store_true',
                            help='Add a mesh (only for item == zone)')
        parser.add_argument('--n_poi', type=int, default=10,
                            help='Add Points Of Interest (only for item == poi)')
        parser.add_argument('--track', action='store_false',
                            help='Track the Points Of Interest (only for item == poi)')
        parser.add_argument('--folder', type=str, default='',
                            help='Select the folder (only for item == limits)')
        parser.add_argument('--run', action='store_false',
                            help='Take new screenshots (only for item == limits)')
        return parser.parse_args()

    def main(self):
        """
        Handle the parsed command-line arguments and
        initiate the corresponding tracking mechanism.
        """
        if self.args.item == 'pixel':
            PixelTracker(self.args.camera).main()
        elif self.args.item == 'zone':
            ZoneDelimiter(self.args.camera,
                          self.args.mesh).main()
        elif self.args.item == 'poi':
            if self.args.track:
                PoiTracker(self.args.camera,
                           self.args.n_poi).main()
            else:
                PoiIdentifier(self.args.camera,
                              self.args.n_poi).main()
        elif self.args.item == 'limits':
            photographer = Photographer(camera=self.args.camera,
                                        folder=self.args.folder,
                                        run=self.args.run)
            PhotographsMatcher(camera=self.args.camera,
                               photographer=photographer).main()


if __name__ == '__main__':
    Tracker().main()
