# A* Search Optimisation System

This project implements a configurable A* search-based optimisation system for solving constrained resource allocation and movement problems.

The system models states, actions, and transition costs explicitly and uses an admissible heuristic to minimise total operational cost.

## Problem Overview
The optimisation problem involves transferring resources between constrained locations while minimising cost under capacity and movement constraints.  
Although the example domain uses livestock pens, the underlying model generalises to logistics and routing problems.

## Features
- A* search using an informed best-first strategy
- Explicit state, action, and cost modelling
- Configurable capacities and movement costs
- Multiple test scenarios and edge cases
- Defensive validation of states and inputs

## Technologies
- Python 3
- A* Search (Informed Search)
- Object-Oriented Design

## How to Run
```bash
python src/shepherd_problem.py
