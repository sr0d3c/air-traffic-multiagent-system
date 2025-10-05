# Airport Traffic Multi-Agent System

A multi-agent simulation system modeling air traffic coordination between airports and airplanes using Mesa (Python).

## 📋 Overview

This project implements a multi-agent system that simulates airplane traffic between multiple airports. The system models realistic airport operations including runway management, takeoff permissions, flight coordination, and collision avoidance.

## 🎯 Features

- **Multi-airport environment**: Multiple airports distributed across a grid world
- **Dynamic runway management**: Airports with varying numbers of runways assigned randomly
- **Flight coordination**: Airplanes request takeoff permissions and coordinate landings
- **Collision avoidance**: Prevention of airplane collisions during flight
- **Time-based simulation**: Each simulation step represents one day (1440 minutes)
- **Simultaneous activation**: All agents act concurrently within each time step

## 🏗️ Architecture

### Space Model
- **Grid Type**: MultiGrid (allows multiple agents per cell)
- **Grid Size**: Configurable (default 10x10)
- **Cell Capacity**: Multiple agents can occupy the same position

### Scheduler
- **Type**: SimultaneousActivation
- **Time Scale**: 
  - 1 iteration = 1 minute
  - 1 step = 60 × 24 iterations = 1 day

### Agent Types

#### 1. Airplane Agent (`Plane`)
**Base Class**: RandomWalker

**Attributes**:
- Current position
- Origin airport
- Destination airport
- Model reference
- Wait time
- State (in airport / flying)

**Behavior**:
- **Step method**: 
  - Countdown timer for takeoff permission request
  - Requests runway access from current airport
  - Adds airplane ID to airport's request queue
  
- **Advance method**:
  - Checks if cleared for takeoff (ID in runway list)
  - Changes state to "flying" and begins movement
  - Navigates toward destination airport
  - Requests landing when reaching destination
  - Changes state back to "in airport" after landing
  - Resets countdown timer

#### 2. Airport Agent (`Airport`)
**Base Class**: mesa.Agent

**Attributes**:
- Position on grid
- Model reference
- Number of available runways
- List of airplanes on runway

**Behavior**:
- **Step method**:
  - Checks runway availability (list size < number of runways)
  - Processes airplane takeoff/landing requests
  - Adds approved airplanes to runway list
  
- **Advance method**:
  - Continues execution (no specific actions)

### Collision Avoidance

The RandomWalker class has been modified to include collision detection:
- Before moving, checks if the next cell is occupied
- If occupied, selects an alternative available position
- Ensures no two airplanes occupy the same cell while flying

## 🚀 Getting Started

### Prerequisites

- Python 3.9
- Mesa 1.2.1

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sr0d3c/air-traffic-multiagent-system.git
cd air-traffic-multiagent-system
```

2. Create a conda environment:
```bash
conda create -n mesa_env python=3.9 -y
conda activate mesa_env
```

3. Install dependencies:
```bash
pip install mesa==1.2.1
```

### Running the Simulation

```bash
python run.py
```

Then open your browser and navigate to:
```
http://localhost:8521
```

## 🎮 Parameters

You can adjust the following simulation parameters:

- **Permission Time**: Time required for airplanes to request takeoff (5-30 minutes)
- **Initial Planes**: Number of airplanes at simulation start (1-10)
- **Initial Airports**: Number of airports in the system (2-10)

## 📊 Simulation Flow

1. **Initialization**:
   - Airports are randomly distributed across the grid
   - Each airport is assigned a random number of runways
   - Airplanes are distributed among airports with assigned destinations

2. **Airplane Lifecycle**:
   - Airplane waits at origin airport
   - Requests takeoff permission after countdown
   - Receives runway clearance
   - Takes off and navigates to destination
   - Requests landing at destination airport
   - Lands and resets for next flight

3. **Airport Operations**:
   - Manages runway allocation
   - Processes takeoff and landing requests
   - Ensures runway capacity is not exceeded

## 🛠️ Technology Stack

- **Framework**: Mesa (Python Agent-Based Modeling Framework)
- **Language**: Python 3.9
- **Visualization**: Mesa ModularServer with CanvasGrid

## 📁 Project Structure

```
airport-traffic-simulator/
├── agents.py          # Agent definitions (Plane, Airport)
├── model.py           # Model definition (PlaneAirport)
├── server.py          # Visualization server
├── random_walk.py     # Random Walker methods
├── scheduler.py       # Custom scheduler (1 step = 1 day = 1440)
├── resources/         # Images and assets
│   ├── airplane.png
│   └── airport.png
└── README.md
```

## 🎓 Academic Context

This project was developed as part of the Multi-Agent Systems course of MSc in Software Engineering and Artificial Intelligence at the University of Málaga.

## 📝 License

This project is available under the MIT License.

## 👤 Author

Sergio Rodero Casado