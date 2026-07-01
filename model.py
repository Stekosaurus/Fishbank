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
        self.opponent = Opponent.create_agents (model = self, n =1)
        self.ships = Ship.create_agents(model=self, n=1)#Initialisiert ein Schiff.
        #Initialisieren bedeuted das quasi aus der Vorlage der Klasse einzelne Objekte, Objekte mit denen Gearbeitet werden kann erstellt werden.
        
        #self.player[0].fleet.append(list(self.ships)[0])#Fügt ein Schiff der Flotte(fleet) des Spielers hinzu.
        #self.opponent[0].fleet.append
    def catch_together(self, player, opponent):
        ocean = self.ocean[0]
        player_count = len(player.fleet)
        opponent_count = len(opponent.fleet)

        ocean.fleet.extend(opponent.fleet)
        ocean.fleet.extend(player.fleet)
        player.fleet = []
        opponent.fleet = []

        rd.shuffle(ocean.fleet)
        for ship in ocean.fleet:
            ship.catch()

        receivers = [(player, player_count), (opponent, opponent_count)]
        rd.shuffle(receivers)
        for agent, count in receivers:
            for i in range(count):
                a = ocean.fleet.pop()
                agent.fleet.append(a)
        
    def step(self):
        self.ocean.do("reproduce")
        player = self.player[0]  
        opponent = self.opponent[0]
        self.opponent.do("execute")
        self.catch_together(player,opponent)
    
        self.player.do("sell_fish")
        self.opponent.do("sell_fish")
            