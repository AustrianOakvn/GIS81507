# GIS81507 - Artificial Intelligence in Games

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