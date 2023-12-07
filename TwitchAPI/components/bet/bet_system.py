from typing import Tuple

from components.databases.bet_db import BetDatabase


class BetSystem():
    def __init__(self, bet_db: BetDatabase):
        """Initialize BetSystem.

        Args:
            bet_db (BetDatabase): BetDatabase object
        """
        self.bet_db = bet_db

        # For current match
        # Map user id to chosen player and bet amount
        self.current_match: dict[str, Tuple[int, int]] = {}

        # For next match
        # Map user id to chosen player and bet amount
        self.next_match: dict[str, Tuple[int, int]] = {}

    def get_balance(self, user_id: str) -> int:
        """Get balance of a user.

        Args:
            user_id (str): Twitch User ID of user

        Returns:
            int: Balance of user
        """
        return self.bet_db.get_balance(user_id)

    def bet(self, user_id: str, amount: int, player: int) -> Tuple[bool, str]:
        """Place a bet

        Args:
            user_id (str): Twitch User ID
            amount (int): Amount of bet
            player (int): Player to bet on

        Returns:
            Tuple[bool, str]: Status and reason for failing
        """
        already_bet_player, already_bet_amount = self.next_match.get(user_id, (None, 0))
        if already_bet_player is not None and already_bet_player != player:
            return False, f"You cannot bet on player {player} if you have already placed a bet on player {already_bet_player}."

        if self.get_balance(user_id) < amount:
            return False, "Balance not enough."

        if self.bet_db.bet(user_id, amount) is True:
            self.next_match[user_id] = player, already_bet_amount + amount
            return True, ""
        else:
            return False, "Unspecified error."

    def award(self, user_id: str, amount: int):
        """Award balance to a user.

        Args:
            user_id (str): Twitch ID of user
            amount (int): Amount to award
        """
        self.bet_db.award(user_id, amount)

    def round_finish(self, winner: int, players_list: list[str], amount_for_winner: int = 5000):
        """This will reward the gamblers and players to win the round.
        Also reassign betting list for next round.

        Args:
            winner (int): ID of character that win the round
            players_list (list[str]): List of players to award for winning
            amount_for_winner (int, optional): Amount to reward to each winner. Defaults to 5000.
        """
        assert winner in [1, 2], "winner must be either 1 or 2"

        # Award the gamblers who win
        winning = [(user_id, amount) for user_id, (player, amount) in self.current_match.items() if player == winner]
        rate = 1 + (len(winning) / len(self.current_match))
        for user_id, amount in winning:
            self.award(user_id, int(amount * rate))

        # Award the players who win
        for user_id in players_list:
            self.award(user_id, amount_for_winner)

        # Assign current_match to next_match and next_match to a new dictionary
        self.current_match = self.next_match
        self.next_match = {}