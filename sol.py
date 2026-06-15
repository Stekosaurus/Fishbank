import solara
import plotly.graph_objects as go
from model import *

# Global erstellen
fishbank = Fishbank(1)
ocean  = next(a for a in fishbank.agents if isinstance(a, Ocean))
player = next(a for a in fishbank.agents if isinstance(a, Player))
ship   = next(a for a in fishbank.agents if isinstance(a, Ship))
clicks = solara.reactive(0)
active_ships = solara.reactive(0)

def make_line_plot(history, title, y_label, color="red", name=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(history))),
        y=history,
        mode='lines',
        name=name or title,
        line=dict(color=color, width=2),
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Schritt",
        yaxis_title=y_label,
        template="plotly_white"
    )
    return fig


@solara.component
def Page():
    show_warning, set_show_warning = solara.use_state(False)


    def reset():
        global fishbank, ocean, player, ship
        fishbank = Fishbank(1)
        ocean  = next(a for a in fishbank.agents if isinstance(a, Ocean))
        player = next(a for a in fishbank.agents if isinstance(a, Player))
        ship   = next(a for a in fishbank.agents if isinstance(a, Ship))
        clicks.value = 0
        
    def one_step():
        fishbank.n_active = active_ships.value
        fishbank.step()
        clicks.value += 1

    def ten_steps():
        for _ in range(10):
            one_step()

    def on_sell_click():
        success = player.sell_ship()
        if not success:
            set_show_warning(True)
        else:
            set_show_warning(False)
    
    def set_active_ships(val):
        active_ships.set(val)
        player.make_active(val)
        
    plots = [
    #(ocean.history, "Populations-Verlauf", "Anzahl Fische", "blue",   "Fish"),
    (player.history, "Kapital",        "Geld",    "orange", "Geld"),
    (ship.history_last, "Gefangene Fische im Letzten Jahr", "Fische", "green", "Fish")
    # weitere Plots einfach hier anhängen...
    ]
    solara.Style(".title { text-align: center; font-size: 3rem; font-weight: bold; }")
    solara.Markdown("<h1 class='title'>Catch The Fish!</h1>")
    
    with solara.Row():
        
        with solara.Column(style={"align-items": "start"}):
            solara.Button(label=f"Jahr {clicks.value}", on_click=one_step)
            solara.Button(label=f"10 Schritte", on_click=ten_steps)
            solara.Button(label="Boot Kaufen", on_click=player.buy_ship)
            solara.Button(label="Boot Verkaufen", on_click=on_sell_click)
            if show_warning:
                solara.Warning("Du hast keine Schiffe!")
                solara.Button("Schließen", on_click=lambda: set_show_warning(False))
            solara.Button(label=f"Reset", on_click=reset)
            

        with solara.Card("Monitor"):
            #solara.Markdown(f"Fische im Ozean:{ocean.num_of_fish}")
            solara.Markdown(f"Geld:{player.money}")
            solara.Markdown(f"Kapital:{player.capital}")
            solara.Markdown(f"Anzahl Schiffe: {len(player.fleet)}")
            solara.Markdown(f"Boots-Kaufpreis:{player.dynamic_buy_price}")
            solara.Markdown(f"Boots-Verkaufspreis: {player.dynamic_sell_price}")
            solara.Markdown(f"Gefange Fische: {ship.caught_fish_last}")

    
        with solara.Columns([1] * len(plots)):
            for history, title, ylabel, color, legend in plots:
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=history, line=dict(color=color), name=legend))
                fig.update_layout(
                    title=title,
                    yaxis_title=ylabel,
                    width=500,
                    height=400
                )
                solara.FigurePlotly(fig)

    # with solara.Column(style={"width": "400px"}):
    #     solara.SliderInt(
    #         label="Aktive Schiffe",
    #         value=active_ships.value,
    #         on_value=set_active_ships,
    #         min=0,
    #         max=len(player.fleet),
    #         step=1,
    #         )

    
print(fishbank.agents)
print(len(fishbank.agents))