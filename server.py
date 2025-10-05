import mesa

from agents import Plane, Airport
from model import PlaneAirport


def port_airport_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Plane:
        portrayal["Shape"] = "./resources/airplane.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Airport:
        portrayal["Shape"] = "./resources/airport.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(port_airport_portrayal, 10, 10, 500, 500)
# chart_element = mesa.visualization.ChartModule(
#     [
#         {"Label": "Plane", "Color": "#AA0000"},
#         {"Label": "Airport", "Color": "#666666"},
#     ]
# )

model_params = {
    "title": mesa.visualization.StaticText("Parameters:"),
    "permission_time": mesa.visualization.Slider("Permission Time", value=10, min_value=5, max_value=30, step=1, description="Tiempo que toma el avión para solicitar despegue"),
    "initial_planes": mesa.visualization.Slider(
        "Number of Initial Planes",value=1, min_value=1, max_value=10, step=1,
        description="Número de aviones iniciales"
    ),
    "initial_airports": mesa.visualization.Slider("Number of airports",value=2, min_value=2, max_value=10, step=1, description="Número de aeropuertos iniciales"),
}

server = mesa.visualization.ModularServer(
    PlaneAirport, [canvas_element], "Plane Airport Traffic", model_params)

server.port = 8521