BannersBroker modelling and simulation software in Python
=========================================================

Author: rnowotniak@gmail.com

Usage
-----

Typical usage of the provided Python classes:

	account = Account(325)
	manager = AccountManager(account)

	strategy = RobertStrategy()

	sim = BBSimulation(manager, strategy)
	sim.run(months = 13)

Simulation details will be printed to the standard output
for further analysis. [draw.py](draw.py) creates a plot
for the simulation. For example, by default,

	$ python bannersbroker.py > data.txt
	$ python draw.py   

creates the following plot:

![plots](https://raw.github.com/rnowotniak/bannersbroker/master/docs/plots.jpg)

Theoretical model for BannersBroker
-----------------------------------

![model](https://raw.github.com/rnowotniak/bannersbroker/master/docs/bannersbroker-0.jpg)

![algorithm](https://raw.github.com/rnowotniak/bannersbroker/master/docs/bannersbroker-1.jpg)

