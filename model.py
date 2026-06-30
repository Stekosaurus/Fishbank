import mesa
from agents import *

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
        self.opponent = Opponent.create_agents (model = self, n =1)
        self.ships = Ship.create_agents(model=self, n=1)#Initialisiert ein Schiff.
        #Initialisieren bedeuted das quasi aus der Vorlage der Klasse einzelne Objekte, Objekte mit denen Gearbeitet werden kann erstellt werden.
        
        #self.player[0].fleet.append(list(self.ships)[0])#Fügt ein Schiff der Flotte(fleet) des Spielers hinzu.
        #self.opponent[0].fleet.append
    def step(self):
        self.ocean.do("reproduce")
        player = self.player[0]  
        opponent = self.opponent[0]
        self.opponent.do("execute")
        for ship in opponent.fleet:
            if ship.operating:
                ship.catch()
            else:
                ship.idle()
        for ship in player.fleet:
            if ship.operating:
                ship.catch()
            else:
                ship.idle()
        
        #self
        self.player.do("sell_fish")
        self.opponent.do("sell_fish")
            