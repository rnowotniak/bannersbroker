BannersBroker modelling and simulation software in Python
=========================================================

Author: Robert Nowotniak <rnowotniak@gmail.com>

Theoretical model for BannersBroker
-----------------------------------

![model](https://raw.github.com/rnowotniak/bannersbroker/master/docs/bannersbroker-0.jpg)

![algorithm](https://raw.github.com/rnowotniak/bannersbroker/master/docs/bannersbroker-1.jpg)

Usage
-----

Typical usage of the provided Python classes:

	from bannersbroker import *

	account = Account(325)
	manager = AccountManager(account)

	strategy = RobertStrategy()

	sim = BBSimulation(manager, strategy)
	sim.run(months = 13)

Simulation details will be printed to the standard output
for further analysis. [draw.py](https://github.com/rnowotniak/bannersbroker/blob/master/draw.py) creates a plot
for the simulation. For example, by default,

	$ python bannersbroker.py > data.txt
	$ python draw.py   

creates the following plot:

![plots](https://raw.github.com/rnowotniak/bannersbroker/master/docs/plots.jpg)

Examples: Selected simulations
------------------------------
### 11 yellow + 3 purple panels  ###
![plots](https://raw.github.com/rnowotniak/bannersbroker/master/docs/bb-11y-3p.jpg)

### 5 blue + 15 purple + 35 yellow panels ###
![plots](https://raw.github.com/rnowotniak/bannersbroker/master/docs/bb-5b-15p-35y.jpg)

