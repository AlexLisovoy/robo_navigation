import argparse
import sys
import logging
import typing
import csv
import math


logger = logging.getLogger(__name__)

_LANDMARK_TO_COORDINATE = {
    "Start": (0, 0),
    "Statue of Old Man": (40, 10)
}


class RoutePoint(typing.NamedTuple):
    position: int
    action: str
    direction: str
    capacity: int = None
    x: int = None
    y: int = None

    @staticmethod
    def from_csv_data(data):
        capacity = x = y = None
        if data['landmark']:
            if data['landmark'] not in _LANDMARK_TO_COORDINATE:
                raise ValueError('Unknown landmark: %s', data['landmark'])
            x, y = _LANDMARK_TO_COORDINATE[data['landmark']]
        else:
            if data['capacity']:
                try:
                    capacity = int(data['capacity'])
                except (TypeError, ValueError):
                    logger.error('Invalid value in capacity: %s', data)
                    raise

        return RoutePoint(
            int(data['position']),
            data['action'],
            data['direction'] if data['direction'] else None,
            capacity,
            x,
            y
        )


class Robot:
    _FACTORS = {
        'north': (0, 1),
        'east': (1, 0),
        'south': (0, -1),
        'west': (-1, 0),
    }

    def __init__(self, coord_x, coord_y, direction='north'):
        self.x = coord_x
        self.y = coord_y
        self.direction = direction

    def __str__(self):
        return '%s, %s -> %s' % (self.x, self.y, self.direction)

    def turn(self, direction):
        if self.direction == direction or not direction:
            logger.debug('Robot is in right direction')
            return 0

        compass = list(self._FACTORS.keys())
        logger.debug('Direction: %s -> %s', self.direction, direction)
        if direction in ('left', 'right'):
            factor = 1 if direction == 'right' else -1
            try:
                direction = compass[compass.index(self.direction) + factor]
            except IndexError:
                direction = 'north'
            logger.debug('Change direction to %s', direction)

        ind1 = compass.index(self.direction)
        ind2 = compass.index(direction)
        if ind1 > ind2:
            ind2 += len(compass)
        degrees = int(math.fabs(ind1 - ind2) * 90)
        logger.info('Turn on %s degrees', degrees)
        self.direction = direction
        return degrees

    def move(self, capacity=None, coord=None):
        factor = self._FACTORS[self.direction]
        if capacity:
            new_coord = (
                self.x + factor[0] * capacity,
                self.y + factor[1] * capacity
            )
        else:
            new_coord = coord

        logger.info('Go to coordinate: %s', new_coord)
        self.x = new_coord[0]
        self.y = new_coord[1]

    def navigate(self, route_points):
        logger.info('Start at: %s', self)
        for num, point in enumerate(route_points, start=1):
            logger.debug('Route point #%s: %s', num, point)

            if point.action == 'turn':
                self.turn(point.direction)
            else:
                self.turn(point.direction)
                self.move(point.capacity, (point.x, point.y))

        logger.info('End at: %s, %s', self.x, self.y)


def parse_file(the_file):
    logger.info('Parse CSV file with route points: %s', the_file.name)
    reader = csv.DictReader(the_file)
    try:
        instructions = [RoutePoint.from_csv_data(rec) for rec in reader]
    except (TypeError, ValueError) as error:
        raise RuntimeError(str(error))
    logger.info('Found route points: %s', len(instructions))
    return sorted(instructions, key=lambda v: v.position)


def main():
    parser = argparse.ArgumentParser(
        description="Script to interpret instructions for the robot"
    )
    parser.add_argument(
        "file",
        type=argparse.FileType('r'),
        help='csv file with instructions for the robot.'
    )
    parser.add_argument(
        '-s',
        "--start_at",
        metavar='start_at',
        nargs=2,
        type=int,
        default=[0, 0],
        help='start coordinates for the robot. (default: %(default)s)'
    )
    parser.add_argument(
        '-v', '--verbose', action='count', dest='level',
        default=2, help='verbose logging (repeat for more verbose)')
    parser.add_argument(
        '-q', '--quiet', action='store_const', const=0, dest='level',
        default=2, help='quiet logging (opposite of --verbose)')

    # parse arguments
    args = parser.parse_args()

    # setup logging
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    level = levels[min(args.level, len(levels) - 1)]
    logging.basicConfig(
        level=level,
        format=('%(asctime)s %(levelname)-8s %(lineno)-3d '
                '%(filename)-20s %(message)s')
    )
    logger.info(
        'Logging system successfully configured with level: %s',
        logging._levelToName[level]
    )

    robot = Robot(*args.start_at)
    try:
        robot.navigate(parse_file(args.file))
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('\nInterrupted\n')


if __name__ == '__main__':
    main()
