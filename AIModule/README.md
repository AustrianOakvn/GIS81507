# This represent the module for AI interact with the DareFightingICE game

## Resources

DareFightingICE provide an library for python to interact with the game called: `pyftg`
Link to the library: [Github repo](https://github.com/TeamFightingICE/pyftg)

Sample code was taken from: [Github repo](https://github.com/TeamFightingICE/PythonAISamples)
Reinforcement learning using only sounds: https://github.com/TeamFightingICE/BlindAI

- Action corresponds to the CommandCenter: https://www.ice.ci.ritsumei.ac.jp/~ftgaic/ZEN_action_animations.htm

## Requirement

Please install DareFightingICE version 6.1 because it need to be compatiable with pyftg

- `python==3.10`
- `pyftg==1.1`

## Structure and available data of `pyftg`

├── ai_controller.py
├── aiinterface (Command with all the available keys)
│   ├── ai_interface.py
│   ├── command_center.py
│   └── **init**py
├── enum
│   ├── action.py
│   ├── data_flag.py
│   ├── flag.py
│   ├── **init**.py
│   └── state.py
├── gateway.py
├── observer_gateway.py
├── observer_handler.py
├── protoc (define message to interact with the games, at the moment, dont have to care about)
│   ├── enum_pb2_grpc.py
│   ├── enum_pb2.py
│   ├── message_pb2_grpc.py
│   ├── message_pb2.py
│   ├── service_pb2_grpc.py
│   └── service_pb2.py
├── struct (Data that we can use)
│   ├── attack_data.py
│   ├── audio_data.py
│   ├── character_data.py
│   ├── fft_data.py
│   ├── frame_data.py (character_data and attack_data of both characters)
│   ├── game_data.py (max_hps, max_energies, character_names, ai_names)
│   ├── hit_area.py
│   ├── key.py (Available keys: A, B, C, U, R, D, L)
│  ├── round_result.py
│   └── screen_data.py
└── util.py

Character Data:

- player_number
- hp
- energy
- x, y (position)
- left, right, top, bottom (?)
- speed_x, speed_y
- state (class)
- action
- front (?)
- control
- attack_data (class)
- hit_count
- last_hit_frame

Attack Data:

- hi_area
- setting_speed_x, setting_speed_y
- current_hit_area (class)
- current_frame
- player_number
- speed_x, speed_y
- start_up (?)
- active (?)
- hit_damge, guard_damge
- start_add_energy, hit_add_energy, guard_add_energy, give_energy
- impact_x, impact_y
- attack_type
- is_projectile

## Idea

- Input 1: User input keys (how many is needed for one attack?)
- Input 2: Hp, energy, distance between 2 characters
- Movement logic: extract the movement input keys --> select random?(sort keys based on if that key would make the character move closer) or any rules?
- Attack logic: extract combo (search combination?, random?) Simple first: if-else (if the combo exist inside the sequence and enery full and near enemy --> launch combo else chose random attack?)
- Advanced: insert keys into the mctsai? (2 mcts played against, modify the mctsai)
- Let's the game run and there will be an AI that trains against another AI (random action, MCTS)
- If both are random?

## How to use

- First run the game with option grpc

```bash
./run-linux-amd64.sh --grpc-auto

```

- Then run the python file Main_PyAIvsPyAI or your own file.
