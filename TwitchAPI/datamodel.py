import dataclasses


@dataclasses.dataclass
class Player:
    twitch_id: str
    username: str

    # it should be either "player_1" or "player_2"
    player_team: str


@dataclasses.dataclass
class Character:
    hp: float
    energy: float


@dataclasses.dataclass
class GameStatus:
    game_state: str
    p1_stats: Character
    p2_stats: Character
