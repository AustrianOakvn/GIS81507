from pydantic import BaseModel

class Player(BaseModel):
    name: str
    balance: int


class LeaderBoard(BaseModel):
    players: list[Player]


class CurrentMatch(BaseModel):
    players: list[Player]
