#!/usr/bin/python
# coding=utf-8
#
# Copyright (C) 2012   Robert Nowotniak, Nowotniak Technologies (C)
#

import sys

PANELS_ATTRIBUTES = (
    # name    price  traffic time(weeks)
    ('Yellow',   10,    5000,  4),
    ('Purple',   30,   15000,  6),
    ('Blue',     90,   45000,  7),
    ('Green',   270,  135000,  8),
    ('Red',     810,  405000, 12),
    ('Black',  2430, 1215000, 34),
)

class PanelType:
    COMPLIMENTARY = 0
    PURCHASED     = 1
    REPURCHASED   = 2
    ROLLUP        = 3

class PanelSettings:
    REPURCHASE_50  = 0
    REPURCHASE_100 = 1

class PanelStatus:
    NOT_QUALIFIED = 0
    ACTIVE = 1
    # FINISHED = 2   # -- no actions can be performed on such panels anyway

class Panel:
    YELLOW = 0
    PURPLE = 1
    BLUE   = 2
    GREEN  = 3
    RED    = 4
    BLACK  = 5

    COLORS = [YELLOW, PURPLE, BLUE, GREEN, RED, BLACK]

    next_id = 0

    def __init__(self, color, type = PanelType.PURCHASED):
        self.id = Panel.next_id
        Panel.next_id += 1
        self.color = color
        self.name, self.price, self.traffic, self.time = PANELS_ATTRIBUTES[color]
        self.type = type
        self.cycle = 0
        self.status = PanelStatus.NOT_QUALIFIED
        self.progress = 0 # for how many days this panel has been working already
        self.settings = PanelSettings.REPURCHASE_100
        self.locked = False

    def regenerate(self):
        if self.type == PanelType.COMPLIMENTARY and self.cycle == 0:
            panel = Panel(self.color, PanelType.COMPLIMENTARY)
        else:
            panel = Panel(self.color, PanelType.REPURCHASED)
        panel.cycle = self.cycle + 1
        print 'Panel %s regenerated' % panel
        return panel

    def qualify(self):
        print "Qualifying the panel %s" % self
        self.status = PanelStatus.ACTIVE
        self.progress = 0


    def symbol(self):
        result = 'YPBGRX'[self.color] + '(%s,%s,%d%%)' % ('CPRU'[self.type], 'NA'[self.status], round(100.*self.progress/(self.time*7)))
        return result

    def __str__(self):
        return self.symbol()

class PanelManager:

    def __init__(self):
        self.__panels = {}
        for color in xrange(len(PANELS_ATTRIBUTES)):
            self.__panels[color] = []

    def add(self, panel):
        self.__panels[panel.color].append(panel)

    def __len__(self):
        return sum([len(p) for p in self.__panels.values()])

    def __iter__(self):
        for color in sorted(self.__panels, reverse=True):
            ind = 0
            while ind < len(self.__panels[color]):
                panel = self.__panels[color][ind]
                yield panel
                ind += 1

    def __getitem__(self, item):
        return self.__panels[item]

    def __str__(self):
        result = ''
        for color in xrange(len(PANELS_ATTRIBUTES)):
            result += '  %6s: %d\n' % (PANELS_ATTRIBUTES[color][0], len(self.__panels[color]))
        return result


class Account:
    STANDARD = 0
    PREMIUM  = 1

    def __init__(self, wallet):
        self.wallet = wallet
        self.traffic = 0
        self.type = Account.STANDARD
        self.panels = PanelManager()
        self.macro = {}
        for color in xrange(len(Panel.COLORS)):
            # free macro for 5 qualifications in each color
            self.macro[color] = PANELS_ATTRIBUTES[color][2] * 5
        self.referrals = []
        self.inviter = None
        print "Created %s" % str(self)

    def printMacro(self):
        result = 'Macro:'
        for color in Panel.COLORS:
            result += ' %d' % self.macro[color]
        return result

    def __str__(self):
        return 'Account: $%.2f   (traffic: %d)' % (self.wallet, self.traffic)


class LimitException(Exception):
    pass

class MakroException(LimitException):
    pass

class TrafficException(LimitException):
    pass

class RollupException(Exception):
    pass

class AccountManager:

    def __init__(self, account):
        self.account = account

    def buyPackage(self, color):
        print "buying a package"
        self.buyMembershipFee()
        for c in xrange(color + 1):
            self.buyPanel(c, type = PanelType.COMPLIMENTARY)

    def buyMembershipFee(self):
        print 'buying a monthly membership'
        self.account.wallet -= 15 if self.account.type == Account.STANDARD else 100

    def buyPanel(self, color, qty = 1, type = PanelType.PURCHASED):
        for i in xrange(qty):
            panel = Panel(color, type = type)
            print 'buying a panel %s' % panel.symbol()
            self.account.wallet -= panel.price
            self.account.panels.add(panel)

    def buyTraffic(self, packs = 1):
        print 'buying %d traffic pack' % packs
        self.account.wallet -= 50
        self.account.traffic += 100000

    def canQualify(self, panel):
        if panel.status == PanelStatus.ACTIVE:
            # already qualified
            return False

        # Firstly, check if it is a complimentary panel (always allowed to be qualified)
        if panel.type == PanelType.COMPLIMENTARY:
            return True

        # Check if there is enough traffic
        if self.account.traffic < panel.traffic: # TODO: ... and self.account.color_banks[panel.color] < panel.traffic
            raise TrafficException('Not enough traffic')

        # Secondly, check if it is a black panel (unlimited qualifications?)
        if panel.color == Panel.BLACK:
            return True

        # Thirdly, check if there is enough macro for this color
        if self.account.macro[panel.color] < panel.traffic:
            raise MakroException("Not enough macro")

        return True


    def qualifyPanel(self, panel):
        if not self.canQualify(panel):
            return

        # TODO: signal panel qualification

        if panel.type != PanelType.COMPLIMENTARY:
            self.account.traffic -= panel.traffic
            self.account.macro[panel.color] -= panel.traffic

            # Qualification of a complimentary panel does not increase macro for the panel owner
            if panel.color > Panel.YELLOW:
                # allow to qualify 2 additional panels of lower color
                self.account.macro[panel.color - 1] += PANELS_ATTRIBUTES[panel.color - 1][2] * 2

        # TODO: notify the sponsor about macro and traffic donation (IF it is a PURCHASE panel)

        panel.qualify()


    def rollup(self, color):
        assert(color < Panel.BLACK)
        to_rollup = filter(lambda p: p.status == PanelStatus.NOT_QUALIFIED, self.account.panels[color])[:3]
        if len(to_rollup) >= 3:
            # remove 3 not qualified panels
            for y in to_rollup:
                self.account.panels[color].remove(y)
                # add 1 new higher panel
            newpanel = Panel(color + 1, PanelType.ROLLUP)
            # TODO: set roll-up type (information of how many purchased packages was in to_rollup)
            self.account.panels.add(newpanel)
            return newpanel
        else:
            raise RollupException("There are only %d %s panels" % (len(to_rollup), PANELS_ATTRIBUTES[color][0]))





class BBSimulation:
    """
    MAIN BannersBroker Simulation algorithm
    """

    def __init__(self, manager, strategy = None):
        self.manager = manager
        self.day = 0
        self.strategy = strategy

    def step(self):
        print '- day %d; %s -' % (self.day, self.manager.account)
        print self.manager.account.printMacro()
        # handle the "special" day (pay a membership fee and buy a traffic pack)
        if self.day % 30 == 0:
            if self.day > 0:
                self.manager.buyMembershipFee()
                self.manager.buyTraffic()
        # present all panels in the inventory
        for panel in self.manager.account.panels:
            print panel.symbol()

        # apply the Strategy callback (qualify panels, buy panels, lock panels etc.)
        if self.strategy:
            self.strategy.callback(self)

        # advance all the panels by one day
        for c in xrange(Panel.BLACK + 1):
            ind = 0
            while ind < len(self.manager.account.panels[c]):
                panel = self.manager.account.panels[c][ind]
                if panel.type == PanelType.COMPLIMENTARY and panel.status != PanelStatus.ACTIVE:
                    # qualify the complimentary panel automatically
                    self.manager.qualifyPanel(panel)
                if panel.status == PanelStatus.ACTIVE:
                    panel.progress += 1
                    if panel.progress == panel.time * 7:
                        # the panel has gained its final revenue
                        # TODO: donate macro and traffic to owner (according to purchase/re-purchase)
                        # TODO: signal panel finish
                        if panel.settings == PanelSettings.REPURCHASE_50:
                            # 1) earn revenue
                            print 'Panel %s earned $ %.2f' % (panel, panel.price)
                            self.manager.account.wallet += panel.price
                            # 2) replace the panel with its new copy
                            newpanel = panel.regenerate()
                            self.manager.account.panels[c][ind] = newpanel
                        elif panel.settings == PanelSettings.REPURCHASE_100:
                            # 1) replace the panel with its new copy
                            newpanel = panel.regenerate()
                            self.manager.account.panels[c][ind] = newpanel
                            # 2) buy a new panel of the same color
                            newpanel = panel.regenerate()
                            self.manager.account.panels[c].insert(0, newpanel)
                            ind += 1
                ind += 1


    def run(self, months = 3):
        self.strategy.start(self)
        for self.day in xrange(months * 31):
            if self.day % 7 == 0:
                print '--- week %d %s---' % (self.day / 7, ('', '(%d months)'%(self.day/7/4))[self.day/7 % 4 == 0])
            self.step()


class AbstractStrategy:

    def start(self, simulation):
        pass

    def callback(self, simulation):
        pass


class Strategy1(AbstractStrategy):

    def callback(self, simulation):
        # odpalac, co sie da
        for panel in simulation.manager.account.panels:
            panel.settings = PanelSettings.REPURCHASE_50
            if panel.status == PanelStatus.NOT_QUALIFIED and simulation.manager.account.traffic >= panel.traffic: # strategy's heuristic rule
                try:
                    simulation.manager.qualifyPanel(panel)
                except LimitException:
                    print "Can't qualify the panel %s" % panel


class ArekStrategy(AbstractStrategy):

    def callback(self, simulation):
        # po ostatnim cyklu fioletowego, rollowac do niebieskiego
        for color in reversed(Panel.COLORS): # reverse is important due to 2:1 rule
            repeat = True
            while repeat:
                repeat = False
                for panel in simulation.manager.account.panels[color]:
                    panel.settings = PanelSettings.REPURCHASE_50
                    if panel.type == PanelType.COMPLIMENTARY and panel.cycle == 0:
                        panel.settings = PanelSettings.REPURCHASE_100
                    try:
                        simulation.manager.qualifyPanel(panel)
                    except MakroException:
                        print "Can't qualify the panel %s" % panel
                        if panel.color == Panel.PURPLE: # and len(simulation.manager.account.panels[Panel.BLUE]) == 0:
                            try:
                                newpanel = simulation.manager.rollup(Panel.PURPLE)
                                print 'Rolled'
                                simulation.manager.qualifyPanel(newpanel)
                                simulation.manager.buyPanel(Panel.PURPLE, 2)
                                repeat = True
                                break
                            except RollupException:
                                pass


class RobertStrategy(AbstractStrategy):

    def start(self, simulation):
        simulation.manager.buyPackage(Panel.BLUE)
        simulation.manager.buyTraffic()
        print 'Buying additional panels'
        simulation.manager.buyPanel(Panel.PURPLE, 2)
        simulation.manager.buyPanel(Panel.YELLOW, 6)

    def callback(self, simulation):
#        if simulation.manager.account.wallet >= 360:
#            simulation.manager.buyPanel(Panel.GREEN)
#            simulation.manager.buyPanel(Panel.BLUE)
        for color in reversed(Panel.COLORS): # reverse is important due to 2:1 rule
            repeat = True
            while repeat:
                repeat = False
                for panel in simulation.manager.account.panels[color]:
                    panel.settings = PanelSettings.REPURCHASE_50
                    if panel.type == PanelType.COMPLIMENTARY and panel.cycle == 0:
                        panel.settings = PanelSettings.REPURCHASE_100
                    try:
                        simulation.manager.qualifyPanel(panel)
                    except LimitException:
                        print "Can't qualify the panel %s" % panel
                        continue
                        if panel.color == Panel.PURPLE: # and len(simulation.manager.account.panels[Panel.BLUE]) == 0:
                            try:
                                newpanel = simulation.manager.rollup(Panel.PURPLE)
                                print 'Rolled'
                                simulation.manager.qualifyPanel(newpanel)
                                simulation.manager.buyPanel(Panel.PURPLE, 2)
                                repeat = True
                                break
                            except RollupException:
                                pass

class PPStrategy1(AbstractStrategy):
    def start(self, simulation):
        simulation.manager.buyPackage(Panel.PURPLE)
        simulation.manager.buyTraffic()
        print 'Buying additional panels'
        simulation.manager.buyPanel(Panel.PURPLE, 2)
        simulation.manager.buyPanel(Panel.YELLOW, 10)

    def callback(self, simulation):
        for color in reversed(Panel.COLORS): # reverse is important due to 2:1 rule
            repeat = True
            while repeat:
                repeat = False
                for panel in simulation.manager.account.panels[color]:
                    panel.settings = PanelSettings.REPURCHASE_50
                    if panel.type == PanelType.COMPLIMENTARY and panel.cycle == 0:
                        panel.settings = PanelSettings.REPURCHASE_100
                    try:
                        simulation.manager.qualifyPanel(panel)
                    except LimitException:
                        print "Can't qualify the panel %s" % panel
                        continue


if __name__ == '__main__':

    account = Account(265)
    manager = AccountManager(account)

    # strategy = Strategy1()
    strategy = PPStrategy1()

#    print account
#    print account.panels

    sim = BBSimulation(manager, strategy)
    sim.run(months = 6)
    print account.wallet





# watpliwosci:
# domyslnie jest repurchase 50 czy 100  (dla kazdego przypadku?)  (100)
# po dwoch cyklach Complimentary znikaja totalnie i w ogole? (tak)
# complimentary nie wchodza do liczby 5, ktore mozna odpalic bez limitow z danego koloru? (tak)
# czy sam 1 complimentary danego koloru pozwala na to, aby odpalic dwa nizszego koloru? (NIE)
# w zasadzie 2 1, ten "1" może byc niekwalifikowany? (musi być kwalifikowany)
#
# czy mozna rollowac panele, ktore moga byc odpalane?  tak
# jak jest z odpalaniem czarnych? podobno można dowolnie dużo
#
# panel rollup daje traffic na koncie sponsora juz na poczatku czy dopiero za zakonczeniu swojej pracy?
#
# do optymalizacji:
#   * kwota wejscia
#   * panel wejscia
#   * reinwestycje (repurchase, zakup dodatkowych paneli za kase z ewalletu)
#   * przekazywanie paneli między kontami
#
# Chromosomy:
#    Y-225-...
#    P-225-...
#
# TODO:
#
#   Zbadac strategie zaproponowana przez Tomasza Plicha
#       (co miesiac wykupywanie o 1 traffic pack wiecej)
#
#   donate makro and traffic to sponsor (re-purchase - na koncu; purchase - na poczatku)
#   wykres calkowitego stanu konta (z panelami)
#   lockowanie
#   konto premium
#   traffic booster
#
#   wykresy makro DONE
#
#
# TODO auto roll-up (przy 6 niekwalifikowanych)
#
