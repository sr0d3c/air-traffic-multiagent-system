
import mesa
from scheduler import SimultaneousActivationDay
from agents import Plane, Airport
import random


class PlaneAirport(mesa.Model):
    """
    Plane-Airport Model
    """
    # Tamaño de cuadrícula
    height = 10
    width = 10
    # Días de simulación
    days = 2
    # Velocidad media de los aviones en km/min
    speed = 100
    # Distancia en km de cada cuadrícula
    distance = 100

    description = (
        "Modelo para la simulación del tráfico aéreo"
    )

    def __init__(
        self,
        width=width,
        height=height,
        days=days,
        initial_planes=10,
        initial_airports=5,
        permission_time=10,
        speed=speed,
        distance=distance,
    ):
        """
        Crea un modelo PlaneAirport para la simulación del tráfico aéreo.

        Args:
            - width: Ancho de la cuadrícula
            - height: Alto de la cuadrícula
            - days: número de días de la simulación
            - initial_planes: número de aviones iniciales
            - initial_airports: número de aeropuertos iniciales
            - permission_time: tiempo que requiere el avión para poder despegar
            - speed: velocidad media de los aviones
            - distance: distancia en km de la cuadrícula.
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.days = days
        self.initial_planes = initial_planes
        self.initial_airports = initial_airports
        self.pos_airports = []
        self.permission_time = permission_time
        self.speed = speed
        self.distance = distance
        self.day = 0
        self.min_pistas = 1
        self.max_pistas = 4

        self.schedule = SimultaneousActivationDay(self)
        self.schedule.time = 0
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.datacollector = mesa.DataCollector(
            {
               "agent_count": lambda m: m.schedule.get_agent_count() 
            }
        )

        # Crea los aeropuertos
        for i in range(self.initial_airports):

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            pos = (x, y)

            while pos in self.pos_airports:
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                pos = (x, y)

            self.pos_airports.append(pos)
            n_pistas = random.randint(self.min_pistas, self.max_pistas)

            airport = Airport(self.next_id(), pos, self, n_pistas)

            self.grid.place_agent(airport, (x, y))
            self.schedule.add(airport)

        # Crea los aviones:
        for i in range(self.initial_planes):
            
            start = self.random.choice(self.pos_airports)
            finish = self.random.choice([j for j in self.pos_airports if j != start])
            plane = Plane(self.next_id(), start, self, False, start, finish, self.permission_time)
            self.grid.place_agent(plane, start)
            self.schedule.add(plane)

        self.running = True
        self.datacollector.collect(self)

    def step(self):

        self.schedule.step()

        if self.schedule.time == 60*24:

            self.day += 1
            self.schedule.time = 0

        if self.day == self.days:

            self.running = False

        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        
        self.step()
        
        
