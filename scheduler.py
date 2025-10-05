import mesa


class SimultaneousActivationDay(mesa.time.SimultaneousActivation):
    """
    Un scheduler que sobreescribe el método step para que la iteración dure un día
    """

    def step(self) -> None:
        """Step all agents, then advance them."""
        #self.time = 0

        #while self.time < 60 * 24:
        print("Time: " + str(self.time))
        agent_keys = list(self._agents.keys())
        
        for agent_key in agent_keys:
            self._agents[agent_key].step()
        for agent_key in agent_keys:
            self._agents[agent_key].advance()
        
        self.time += 1
        self.steps += 1
