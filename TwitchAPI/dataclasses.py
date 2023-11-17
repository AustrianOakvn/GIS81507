import dataclasses


@dataclasses
class Player:
    twitch_id: str
    username: str

    # it should be either "player_1" or "player_2"
    player_team: str


@dataclasses
class Character:
    hp: float
    energy: float


@dataclasses
class GameStatus:
    game_id: str
    game_status: str
    character_1: Character
    character_2: Character
