import mesa
from agents import *
import random as rd
import solara
import plotly.express as px
import plotly.graph_objects as go

class Fishbank(mesa.Model):

    def __init__(self, seed=None):
        """
        Erstellt das Grundmodell in dem sich alle weiteren "Agenten" befinden und agieren.
        """
        super().__init__(seed=seed)
        self.ocean = Ocean.create_agents(model=self, n=1) #Initialisiert einen Ozean mit Fischen
        self.player = Player.create_agents (model=self, n=1) # Initialisiert die gewünschte anzahl Spieler(Aktuell nur 1).
        self.opponent = Opponent.create_agents (model = self, n =3)
        self.ships = Ship.create_agents(model=self, n=1)#Initialisiert ein Schiff.
        #Initialisieren bedeuted das quasi aus der Vorlage der Klasse einzelne Objekte, Objekte mit denen Gearbeitet werden kann erstellt werden.
        
        #self.player[0].fleet.append(list(self.ships)[0])#Fügt ein Schiff der Flotte(fleet) des Spielers hinzu.
        #self.opponent[0].fleet.append
    def catch_together(self, player, *opponents):
        ocean = self.ocean[0]

        agents = [player, *opponents]   # bei keinem Gegner: agents = [player]
        counts = [len(a.fleet) for a in agents]

        for agent in agents:
            ocean.fleet.extend(agent.fleet)
            agent.fleet = []

        rd.shuffle(ocean.fleet)
        for ship in ocean.fleet:
            ship.catch()

        receivers = list(zip(agents, counts))
        rd.shuffle(receivers)
        for agent, count in receivers:
            for i in range(count):
                a = ocean.fleet.pop()
                agent.fleet.append(a)
        
    def step(self):
        self.ocean.do("reproduce")
        player = self.player[0]
        opponents = list(self.opponent)

        if len(opponents) >= 1:
            opponents[0].money_oriented_one()     # direkter Methodenaufruf statt .do()
        if len(opponents) >= 2:
            opponents[1].money_oriented_two()
        if len(opponents) >= 3:
            opponents[2].money_oriented_three()

        self.catch_together(player, *opponents)

        self.player.do("sell_fish")
        self.opponent.do("sell_fish")
            