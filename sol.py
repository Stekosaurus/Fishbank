import solara
import plotly.graph_objects as go
from model import *

# Global erstellen
fishbank = Fishbank(1)
ocean  = next(a for a in fishbank.agents if isinstance(a, Ocean))
player = next(a for a in fishbank.agents if isinstance(a, Player))
ship   = next(a for a in fishbank.agents if isinstance(a, Ship))
opponent = next(a for a in fishbank.agents if isinstance(a, Opponent))
clicks = solara.reactive(0)
active_ships = solara.reactive(0)

def make_line_plot(history, title, y_label, color="red", name=None, extra=None):
    """
    extra: optionales (history2, name2, color2)-Tupel für eine zweite Linie
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(history))),
        y=history,
        mode='lines',
        name=name or title,
        line=dict(color=color, width=2),
    ))
    if extra:
        history2, name2, color2 = extra
        fig.add_trace(go.Scatter(
            x=list(range(len(history2))),
            y=history2,
            mode='lines',
            name=name2,
            line=dict(color=color2, width=2),
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
        opponent = next(a for a in fishbank.agents if isinstance(a, Opponent))
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
    (ocean.history, "Ozean", "Population", "blue", "Fische", None),
    (player.capital_history, "Kapital", "Geld", "orange", "Geld",
        (opponent.capital_history, "Opponent", "red")),
    (player.total_catch_history, "Gefangene Fische im Letzten Jahr", "Fische", "green", "Spieler",
        (opponent.total_catch_history, "Opponent", "red")),
]
    
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
            solara.Markdown(f"Spieler Geld:{player.money}")
            solara.Markdown(f"Gegner Geld:{opponent.money}")
            solara.Markdown(f"Spieler Kapital:{player.capital}")
            solara.Markdown(f"Gegner Kapital:{opponent.capital}")
            solara.Markdown(f"Spieler  Schiffe: {len(player.fleet)}")
            solara.Markdown(f"Gegner Schiffe: {len(opponent.fleet)}")
            solara.Markdown(f"Boots-Kaufpreis:{player.dynamic_buy_price}")
            solara.Markdown(f"Boots-Verkaufspreis: {player.dynamic_sell_price}")
            solara.Markdown(f"Spieler Gefangene Fische: {player.total_catch}")
            solara.Markdown(f"Gegner Gefangene Fische: {opponent.total_catch}")

    
        with solara.Columns([1] * len(plots)):
            for history, title, ylabel, color, legend, extra in plots:
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=history, line=dict(color=color), name=legend))
                if extra:
                    history2, name2, color2 = extra
                    fig.add_trace(go.Scatter(y=history2, line=dict(color=color2), name=name2))
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

    
#print(fishbank.agents)
print(f"agenten:{len(fishbank.agents)}")
