# Lifeguard Pool Simulation

This project is a simple Pygame-based simulation of the classic lifeguard optimization problem.

## What it demonstrates

- A drowning person appears at a random location inside a rectangular water pool.
- A lifeguard starts from a fixed land location below the pool.
- The lifeguard can run quickly on land and swims more slowly in water.
- The user selects a shoreline entry point where the lifeguard enters the water.
- The simulation shows both the chosen path and the computed optimal path.

The goal is to illustrate how the fastest rescue route may not be a straight line to the victim.

## How to use

1. Install Python and Pygame.
   - Example: `pip install pygame`
2. Run the simulation:
   - `python lifeguard_sim.py`
3. When the window opens:
   - Click on the shoreline (the boundary line between land and water) to choose where the lifeguard enters the water.
   - The black dot represents the lifeguard following your chosen path.
   - The green dot follows the computed optimal entry path.
   - The red dot is the drowning person.
4. Press `Space` or click the green reset button to spawn a new random target and try again.

## Controls

- Left click on the shoreline: choose a custom entry point.
- `Space`: reset the target and start over.

## Notes

- The blue area is water.
- The sandy area is land.
- The green line/dot indicates the most optimal entry point found by the simulation.
- The yellow marker shows your selected entry point.
