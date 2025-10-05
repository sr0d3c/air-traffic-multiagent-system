import mesa
from random_walk import RandomWalker


class Plane(RandomWalker):
    """
    Agente de avión que solicita permiso para despegar, entra en pista y vuela hasta que llega a destino y solicita el aterrizaje. 
    Tras entrar en pista y aterrizar, hace el viaje de vuelta.

    Args:
        - Unique_id: id único del avión.
        - pos_actual: posición en la que se encuentra el avión en el momento.
        - model: modelo de la simulación
        - moore: parámetro que indica siendo True si el avión se mueve en 8 direcciones, por el contrario lo hace en 4.
        - start: aeropuerto de partida.
        - finish: aeropuerto de destino.
        - countdown: tiempo de espera que toma el avión para poder despegar.
    """


    def __init__(self, unique_id, pos_actual, model, moore, start, finish, countdown):

        super().__init__(unique_id, pos_actual, model, moore=moore)

        self.pos_actual = pos_actual
        self.start = start
        self.finish = finish
        self.countdown = countdown
        self.estado = "aeropuerto"

    def step(self):

        if self.estado == "aeropuerto":

            if self.countdown <= 0:

                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                airport = [obj for obj in this_cell if isinstance(obj, Airport)]
                airport[0].entra_pista.append(self.unique_id)

            else:

                self.countdown -= 1

    def advance(self):

        if self.estado=="aeropuerto":

            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            airport = [obj for obj in this_cell if isinstance(obj, Airport)][0]

            if self.unique_id in airport.aviones_pista:

                self.estado = "volando"

                airport.aviones_pista.remove(self.unique_id)
                airport.entra_pista.remove(self.unique_id)

                self.random_move()

        elif self.estado == "volando":

            if self.pos == self.finish:

                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                airport = [obj for obj in this_cell if isinstance(obj, Airport)][0]

                if self.unique_id not in airport.entra_pista:

                    airport.entra_pista.append(self.unique_id)

                if self.unique_id in airport.aviones_pista:

                    self.estado = "aeropuerto"

                    airport.entra_pista.remove(self.unique_id)
                    airport.aviones_pista.remove(self.unique_id)

                    self.countdown = self.model.permission_time

                    self.finish = self.start
                    self.start = self.pos

            else:
                self.random_move()

class Airport(mesa.Agent):
    """
    Agente de aeropuerto que da permiso al avión para que pueda despegar/aterrizar.

    Args:
        - Unique_id: ID único del aeropuerto
        - pos: posición del aeropuerto
        - model: modelo de la simulación
        - n_pistas: Número de pistas de aterrizaje/despegue
    """

    def __init__(self, unique_id, pos, model, n_pistas):

        super().__init__(unique_id, model)
        self.pos = pos
        self.n_pistas = n_pistas
        self.entra_pista = []
        self.aviones_pista = []

    def step(self):

        print("Aviones pidiendo entrar en pista " + str(self.unique_id) + " = " + str(self.entra_pista))

        if len(self.entra_pista) > 0:
            for avion in self.entra_pista:
                if len(self.aviones_pista) < self.n_pistas:

                    self.aviones_pista.append(avion)

                else:
                    break

        print("Aviones en pista del aeropuerto " + str(self.unique_id) + " = " + str(self.aviones_pista) + " // N_pistas = " + str(self.n_pistas))
        self.entra_pista = []

    def advance(self):
        pass