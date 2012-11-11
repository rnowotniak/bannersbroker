BannersBroker modelling and simulation software in Python
=========================================================

Author: Robert Nowotniak <rnowotniak@gmail.com>

In August 2012, I created a mathematical model (based on discrete dynamical system) and
the simulator software for account management in BannersBroker. --
Initially, there were plans of running a paid site, allowing for example to
perform calculations and simulations by BB users.

Currently, I came to the conclusion, that I can no longer invest my time and
work (which I put in, a lot already) in something I'm not going to be seriously
involved with (for various reasons) in the future.
Therefore, I decided to publish the results of all of my work in this area.

The simulator allows to create long-term forecasts, and to perform simulations and
optimization of a **single account management** in BannersBroker.
In this simulator,
all rules of single account management have been implemented:
monthly membership fees, traffic packs, limits (macro and color banks),
5+2:1 principle, panel types: purchased, repurchased, complimentary, and roll the
panels
The software allows to simulate Standard and Premium subscription types.
Reliability and accuracy of the simulations have been verified in practice,
i.e. on real accounts in BB from August 2012 to the present.

I decided to release this software on General Public License (GPL),
which allows each person to use it for free, for any purpose.

At the same time, I remain open to the potential for cooperation in the future,
for example, on the basis of the creation of paid forecasts, analysis or
optimization strategy.  If there is such a demand in the future, I'm available.

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

