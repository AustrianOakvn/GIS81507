# GIS81507 - Artificial Intelligence in Games

## Requirements

Game: v6.1

Python 3.11 and the following dependencies:
```
# AI Module
uvicorn
fastapi
pyftg
pydantic
# Twitch Module
twitchio==2.8.2
python-dotenv==1.0.0
httpx==0.25.1
requests
python-dotenv
```

## Install instructions

1. Create a new Python environment with requirements
2. Run the game
3. Open new terminal and open game server
```
cd AIModule
python game_server.py
```
In the game, Player should show DemoAI_2 (Visual AI)
4. Open command server
```
cd AIModule
python command_server.py
```
5. Open new terminal and GUI. Specify a new path so that the GUI will read from this file. It does not have to be exist for now.
```
cd AIModule
python view.py --json_path <path_to_game_stat_file>
```
6. In `TwitchAPI` folder, configure the bot by copying `.env.example` to `.env`. Then, modify the `.env` file using your credentials.
7. In `TwitchAPI/config.py`, set `STATUS_JSON_ADDRESS` to the path specified in step 5.
8. Open new terminal and run the bot
```
cd TwitchAPI
python main.py
```
9. In the game, make sure that both are GRPC and characters are Zen.
10. Start the match

## API design


### Side choosing

### Player API

- Start game

```
{
    game_id: string,
    start: bool,
}
```

- Command handler

```
{
  player_1:
  {
    actions: [action_1, ..., action_n]
  },
  player_2:
  {
    actions: [action_1, ..., action_n]
  }
}
```

- Game status

```
{
    game_status: string,
    character_1:
    {
        hp: float,
        energy: float
    },
    character_2:
    {
        hp:float,
        energy: float
    }
}
```

### Better API

Twitch server received Game status message and perform betting logic.