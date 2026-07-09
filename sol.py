import solara
import plotly.graph_objects as go
from model import *

# Global erstellen
fishbank = Fishbank(1)
ocean  = next(a for a in fishbank.agents if isinstance(a, Ocean))
player = next(a for a in fishbank.agents if isinstance(a, Player))
ship   = next(a for a in fishbank.agents if isinstance(a, Ship))
opponents = [a for a in fishbank.agents if isinstance(a, Opponent)]
clicks = solara.reactive(0)
active_ships = solara.reactive(0)

COLORS = ["red", "purple", "brown", "gray", "cyan"]


def opponent_tuples(attr_name):
    """Baut (history, name, color)-Tupel für alle aktuellen Gegner."""
    return [
        (getattr(opp, attr_name), f"Opponent {i+1}", COLORS[i % len(COLORS)])
        for i, opp in enumerate(opponents)
    ]


@solara.component
def Page():
    show_warning, set_show_warning = solara.use_state(False)

    def reset():
        global fishbank, ocean, player, ship, opponents
        fishbank = Fishbank(1)
        ocean  = next(a for a in fishbank.agents if isinstance(a, Ocean))
        player = next(a for a in fishbank.agents if isinstance(a, Player))
        ship   = next(a for a in fishbank.agents if isinstance(a, Ship))
        opponents = [a for a in fishbank.agents if isinstance(a, Opponent)]
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
        (ocean.history, "Ozean", "Population", "blue", "Fische", []),
        (player.capital_history, "Kapital", "Geld", "orange", "Geld",
            opponent_tuples("capital_history")),
        (player.total_catch_history, "Gefangene Fische im Letzten Jahr", "Fische", "green", "Spieler",
            opponent_tuples("total_catch_history")),
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
            solara.Markdown(f"Spieler Geld:{player.money}")
            solara.Markdown(f"Spieler Kapital:{player.capital}")
            solara.Markdown(f"Spieler  Schiffe: {len(player.fleet)}")
            solara.Markdown(f"Boots-Kaufpreis:{player.dynamic_buy_price}")
            solara.Markdown(f"Boots-Verkaufspreis: {player.dynamic_sell_price}")
            solara.Markdown(f"Spieler Gefangene Fische: {player.total_catch}")

            for i, opp in enumerate(opponents):
                solara.Markdown(f"Gegner {i+1} Geld:{opp.money}")
                solara.Markdown(f"Gegner {i+1} Kapital:{opp.capital}")
                solara.Markdown(f"Gegner {i+1} Schiffe: {len(opp.fleet)}")
                solara.Markdown(f"Gegner {i+1} Gefangene Fische: {opp.total_catch}")

        with solara.Columns([1] * len(plots)):
            for history, title, ylabel, color, legend, extras in plots:
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=history, line=dict(color=color), name=legend))
                for history2, name2, color2 in extras:
                    fig.add_trace(go.Scatter(y=history2, line=dict(color=color2), name=name2))
                fig.update_layout(
                    title=title,
                    yaxis_title=ylabel,
                    width=500,
                    height=400
                )
                solara.FigurePlotly(fig)


print(f"agenten:{len(fishbank.agents)}")