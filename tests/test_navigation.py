import pytest

from robo_navigation import Robot
from robo_navigation import RoutePoint


@pytest.fixture()
def robot():
    return Robot(0, 0)


@pytest.mark.parametrize(
    ("direction1,direction2,degrees"),
    [
        pytest.param('north', 'left', 270, id='north_left'),
        pytest.param('north', 'right', 90, id='north_right'),
        pytest.param('west', 'right', 90, id='west_right'),
        pytest.param('west', 'left', 270, id='west_left'),

        pytest.param('north', 'east', 90, id='north_east'),
        pytest.param('north', 'south', 180, id='north_south'),
        pytest.param('north', 'west', 270, id='north_west'),
        pytest.param('north', 'north', 0, id='north_north'),

        pytest.param('east', 'south', 90, id='east_south'),
        pytest.param('east', 'west', 180, id='east_west'),
        pytest.param('east', 'north', 270, id='east_north'),
        pytest.param('east', 'east', 0, id='east_east'),

        pytest.param('south', 'west', 90, id='south_west'),
        pytest.param('south', 'north', 180, id='south_north'),
        pytest.param('south', 'east', 270, id='south_east'),
        pytest.param('south', 'south', 0, id='south_south'),

        pytest.param('west', 'north', 90, id='west_north'),
        pytest.param('west', 'east', 180, id='west_east'),
        pytest.param('west', 'south', 270, id='west_south'),
        pytest.param('west', 'west', 0, id='west_west'),
    ]
)
def test_turn_robot(direction1, direction2, degrees, robot):
    robot.direction = direction1
    assert robot.turn(direction2) == degrees


@pytest.mark.parametrize(
    ("capacity,coord,expected_coord"),
    [
        pytest.param(None, (10, 10), (10, 10), id='move_to_specific_coord'),
        pytest.param(40, None, (0, 40), id='move_using_capacity'),
    ]
)
def test_move_robot(capacity, coord, expected_coord, robot):
    robot.move(capacity, coord)

    assert str(robot) == "%s, %s -> north" % expected_coord


def test_navigate(robot):
    # This route describe moving by square with end point in the same place.
    route_points = [
        RoutePoint.from_csv_data({
            'position': '10',
            'action': 'go',
            'direction': '',
            'capacity': '20',
            'landmark': ''
        }),
        RoutePoint.from_csv_data({
            'position': '20',
            'action': 'go',
            'direction': 'east',
            'capacity': '20',
            'landmark': ''
        }),
        RoutePoint.from_csv_data({
            'position': '30',
            'action': 'go',
            'direction': 'south',
            'capacity': '20',
            'landmark': ''
        }),
        RoutePoint.from_csv_data({
            'position': '40',
            'action': 'turn',
            'direction': 'right',
            'capacity': '',
            'landmark': ''
        }),
        RoutePoint.from_csv_data({
            'position': '50',
            'action': 'go',
            'direction': None,
            'capacity': '',
            'landmark': 'Start'
        }),
    ]
    robot.navigate(route_points)

    assert str(robot) == "0, 0 -> west"
