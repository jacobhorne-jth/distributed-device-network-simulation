# distributed-device-network-simulation
A Python simulation of alert propagation and cancellation across a distributed network of devices with configurable delays.

**Overview**

This project is a simulation of how information spreads across a network of interconnected devices, built in Python with clean separation of simulation logic, event scheduling, and device state management.

It models a simplified distributed system where devices send alerts and cancellations to each other according to configurable rules and delays—illustrating key concepts of network propagation and event-driven systems.

The project implements:

- A time-stepped event scheduler to process message events in order.

- Object-oriented modeling of devices, events, and simulation orchestration.

- Deterministic, reproducible outputs for the same inputs.

- Unit tests covering core logic of device state and event queueing.

**Features**

- Event-Driven Simulation

  Devices send and receive alerts and cancellations based on input specifications.

- Configurable Network Topology

  Devices, connections, and delays are defined in an input file.

- Deterministic Outputs

  Running the same simulation always yields the same event log.

- Automatic Time Advancement

  Simulation jumps forward to the next scheduled event for efficiency.

- Custom Exception Handling

  Gracefully handles invalid input files (e.g., missing files).

- Unit Testing

  Includes automated tests for devices, events, and simulation flow.

**How to Run**

_Prerequisites_

- Python 3.6+
- Unittest frameworks

_Running the Simulation_

Execute the main script:

python3 devicesimulationmain.py

You will be prompted to enter the path to an input file describing the simulation.

_Example input file:_

insert ouytput

The program prints event logs to the console.

_Example output file:_

insert output

_Controls_

- Enter file path when prompted.

- Watch simulation output in the terminal.

- Ctrl+C or close terminal to stop.

_Project Structure_

device.py # Device class and propagation logic

event.py # Event scheduling and processing

devicesimulationmain.py # Main simulation entry point

test_device.py # Unit tests for devices

test_event.py # Unit tests for events

test_devicesimulationmain.py # Integration tests

_Example Run Through_


When you start the simulation:

- Devices and their connections are created.

- Events are scheduled (alerts and cancellations).

- The simulation processes events chronologically.

- Devices propagate messages as per configuration.

Simulation ends at the specified time.

_Notes_

- Simulation Mechanics: The program models devices that automatically propagate alerts and cancellations with delays. No real networking occurs—it's purely simulated.

- File Organization: Core logic, event management, and main script are modularized for clarity.

_Future Steps_

- Visualizing the propagation timeline with a graphical interface.

- Supporting dynamic network changes during simulation.

- Adding configuration validation and richer error reporting.

- Exporting simulation logs to a file.

_Attribution_

Python Standard Library: Used for all functionality (no third-party packages).

<br>
_License_

This project is intended for educational use.
