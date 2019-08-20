# robo_navigation

## Assumptions

 1. Each unit/block has the same size.
 2. The robot moves uniformly at the same speed
 3. The robot can move only by edge of unit/block. Diagonal movement is prohibited.
 4. In initial/start point the robot is always facing to north.
 5. The route is always correct and it's not possible to go out of the Northern or Eastern edges.

## Route Specification

A route is an ordered list of steps.
Each step can be described by 4 main criterias:

 1. Action - describes the action that the robot must perform. Possible values: go, turn.
 2. Direction - describes in which way the robot must perform action. Empty Direction means that the robot is already in right direction. Possible values: left, right, north, east, south and west.
 3. Capacity - describes how many units/blocks a robot must perform to be consider action as completed. Also can contains coordinate in landmark case.
 3. Landmark - local names of specific coordinates. For example: Statue of Old Man.

 Example of route(the route is stored in CSV format):

route,position,action,direction,capacity,landmark
route 1,10,go,north,10,
route 1,20,turn,left,,
route 1,30,go,,5,
route 1,40,turn,right,,
route 1,50,go,,10,
route 1,60,go,east,,Statue of Old Man

You can found more routes under data folder.

## Database schema

![Infrastructure of the service](https://github.com/AlexLisovoy/robo_navigation/blob/master/db.svg)

You can found raw sql definition under db folder.

## Instalation

To install project just execute command:

```
$ pip install -e .
```

## Run the implementation

To run interpretator you should provide the route in CSV file. For example:

```
$ robo-navigation data/route_1.csv
```

The script also support to change start point. To do this provide optional argmunent start_at:

```
$ robo-navigation data/route_1.csv --start_at 40 10
```

## Preconditions for running tests

We expect you to use a python virtual environment to run our tests.

There are several ways to make a virtual environment.

If you like to use virtualenv please run:

```
$ virtualenv --python=`which python3` venv
```

For standard python venv (my choice):

```
$ python3 -m venv venv
```

There are other tools like pyvenv but you know the rule of thumb now: create a python3 virtual environment and activate it.

After that please install libraries required for development:

```
$ pip install -r requirements-dev.txt
```

Congratulations, you are ready to run tests.


## Run tests

After all the preconditions are met you can run tests typing the next command:

```
$ make test
```

The command at first will run the flake8 tool.

On flake8 success the tests will be run.

Please take a look on the produced output.

**Note:** if you need more verbose output or you plan to use ipdb within the tests, use:

```
$ make vtest
```

to run the tests.


## Tests coverage

Use:

```
$ make cov
```

to run test suite and collect coverage information. Once the command has finished check your coverage at the file that appears in the last line of the output:
`open file:///.../../coverage/index.html`

