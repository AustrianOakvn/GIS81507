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

    def get_top_user_and_balance(self, top_k: int = 5) -> list[Tuple[str, int]]:
        """Get top users with most balance

        Args:
            top_k (int, optional): Number of users. Defaults to 5.

        Returns:
            list[Tuple[str, int]]: List of tuples of user name and balance
        """
        top_list: list[Tuple[str, str, int]] = self.bet_db.top_balance(top_k)
        return [(i[1], i[2]) for i in top_list]

    def get_top_bet_by_character(self, character_id: int, top_k: int = 5) -> list[Tuple[str, int]]:
        """Get top bet (of current match) by character ID

        Args:
            character_id (int): Character ID
            top_k (int, optional): Number of players. Defaults to 5.

        Returns:
            list[Tuple[str, int]]: List of tuples of user_name, amount
        """
        assert character_id in [1, 2]

        bet_list: list[Tuple[str, int]] = [(user_id, amount) for user_id, (c_id, amount) in self.current_match.items() if character_id == c_id]
        bet_list = sorted(bet_list, key=lambda x: x[1], reverse=True)[:top_k]

        # Resolve user_id to user_name
        bet_list = [(self.bet_db.get_name(i[0]), i[1]) for i in bet_list]

        return bet_list

    def get_balance(self, user_id: str, user_name: str) -> int:
        """Get balance of a user.

        Args:
            user_id (str): Twitch User ID of user
            user_name (str): Username

        Returns:
            int: Balance of user
        """
        return self.bet_db.get_balance_update_username(user_id, user_name)

    def bet(self, user_id: str, user_name: str, amount: int, player: int) -> Tuple[bool, str]:
        """Place a bet

        Args:
            user_id (str): Twitch User ID
            user_name (str): Username
            amount (int): Amount of bet
            player (int): Player to bet on

        Returns:
            Tuple[bool, str]: Status and reason for failing
        """
        already_bet_player, already_bet_amount = self.next_match.get((user_id, user_name), (None, 0))
        if already_bet_player is not None and already_bet_player != player:
            return False, f"You cannot bet on player {player} if you have already placed a bet on player {already_bet_player}."

        if self.get_balance(user_id, user_name) < amount:
            return False, "Balance not enough."

        if self.bet_db.bet(user_id, user_name, amount) is True:
            self.next_match[(user_id, user_name)] = player, already_bet_amount + amount
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
        assert winner in [0, 1, 2], "winner must be either 0 (draw), 1 (p1 wins) or 2 (p2 wins)"

        # Award the gamblers who win
        if winner == 0:
            # Return money to all gamblers
            winning = [(user_id, amount) for (user_id, user_name), (_, amount) in self.current_match.items()]
        else:  # Winner = 1 or 2
            winning = [(user_id, amount) for (user_id, user_name), (player, amount) in self.current_match.items() if player == winner]

        if len(winning) != 0:
            if winner == 0:
                # Draw. Return the exact money.
                rate = 1
            else:
                # Either 1 or 2 won. Calculate rate and return
                rate = 1 + (len(winning) / len(self.current_match))

            for user_id, amount in winning:
                self.award(user_id, int(amount * rate))

        # Award the players who win
        for user_id in players_list:
            self.award(user_id, amount_for_winner)

        # Assign current_match to next_match and next_match to a new dictionary
        self.current_match = self.next_match
        self.next_match = {}
