import numpy as np
import pandas as pd
import seaborn as sns
import mesa 
import matplotlib.pyplot as plt


class Ocean(mesa.Agent):
    """
    Erstellt die Vorlage Ozean mit seinen Parametern
    """
    def __init__(self, model):
        super().__init__(model)
        self.num_of_fish = 10000 #Anzahl der Fische zu beginn des Modells
        self.capacity = 15000 #Natürliche Kapzität des Ozeans
        self.r_rate = 0.1 #Reproduktionsrate der Fische
        self.history = [self.num_of_fish] #Liste mit dem Verlauf der der Anzahl der Fische. Wichtig für das Zeichnen des Graphen
        

    def reproduce(self):
        """
        Funktion zum vermehren der Fische, wird in jedem Schritt aufgerufen
        """
        self.num_of_fish = self.num_of_fish + self.r_rate * self.num_of_fish * (1 - self.num_of_fish / self.capacity) #Gleichung für Logistische Wachstum
        self.num_of_fish = round(self.num_of_fish)#"round" rundet das Ergebnis damit wir immer mit ganzen Zahlen arbeiten können.

        self.history.append(self.num_of_fish)#Hängt der aktualisierte Zahl der Fische an die "history" Liste an.

class Ship(mesa.Agent):
    base_price = 1000
    def __init__(self, model, owner: "Player" = None):
        super().__init__(model)
        self.owner = owner
        self.operating = True
       
        self.sell_price = 750
        self.idle_cost = 10
        self.operating_cost = 30
        self.catch_rate = 0.01
        self.max_cargo = 150
        self.caught_fish_last = 0
        self.caught_fish_total = 0
        self.history_total = [self.caught_fish_total]
        self.history_last = [self.caught_fish_last]

    def catch(self):
        ocean = self.model.agents.select(agent_type=Ocean)[0]
        player = self.model.agents.select(agent_type=Player)[0]
        
        raw_catch = ocean.num_of_fish * self.catch_rate * len(player.fleet)
        
        # max_cargo gilt pro Schiff → Gesamtkapazität = max_cargo * Anzahl Schiffe
        total_cargo = self.max_cargo * len(player.fleet)
        self.caught_fish_last = round(min(raw_catch, total_cargo))
        self.caught_fish_total += self.caught_fish_last
        
        ocean.num_of_fish -= self.caught_fish_last
        ocean.num_of_fish = round(ocean.num_of_fish)
        #player.money = round(player.money - self.operating_cost * len(player.fleet))
        
        self.history_total.append(self.caught_fish_total)
        self.history_last.append(self.caught_fish_last)
    def idle(self) :
        player = self.model.agents.select(agent_type=Player)[0]
        player.money = round(player.money - self.idle_cost)
    


class Player(mesa.Agent):
    def __init__(self, model, fleet: list[Ship] = None):
        super().__init__(model)
        self.money = 10000
        self.fleet = fleet if fleet is not None else []
        self.num_of_ships = len(self.fleet)
        self.price_per_fish = 1
        self.capital = self.money + sum(ship.buy_price for ship in self.fleet)
        self.history = [self.money]
        #self.operating_cost = ship.operating_cost

    @property
    def dynamic_buy_price(self):
        return Ship.base_price + len(self.fleet) * 100
    
    @property
    def dynamic_sell_price(self ):
        return Ship.base_price - len(self.fleet) * 100
        
    def buy_ship(self):
        new_ship = Ship.create_agents(model=self.model, n=1)  
        if self.money < self.dynamic_buy_price:
            print("Not enough money")
        else:
            self.fleet.append(new_ship[0])
            self.money -= self.dynamic_buy_price
    
    def sell_ship(self):
        ship = self.model.agents.select(agent_type = Ship)[0]
        
        if len(self.fleet) == 0 :
           return False
        else:
            self.fleet.pop()
            self.money = self.money + ship.sell_price
            return True
    
    def sell_fish(self):
        # Fang aller Schiffe in der Flotte summieren
        total_catch = sum(s.caught_fish_last for s in self.fleet)
        total_operating_cost = sum(s.operating_cost for s in self.fleet)
        self.money += round(self.price_per_fish * total_catch - total_operating_cost)
        self.history.append(self.money)


    
print("agent run succesfull")