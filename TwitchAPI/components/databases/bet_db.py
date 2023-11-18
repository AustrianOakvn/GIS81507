import logging
from typing import Tuple

from components.databases.database import Database


logger = logging.getLogger(__name__)


class BetDatabase(Database):
    def __init__(self):
        super().__init__("bet")

        # Check if need init
        if not self.check_if_table_exists("balance"):
            # Need to init balance
            logger.info('Table `balance` not found. Creating...')
            self.create_balance_table()
            logger.info('Created table `balance`.')

    def create_balance_table(self):
        """Create `balance` table to store players' balance."""
        self.get_cursor().execute("""
            CREATE TABLE IF NOT EXISTS balance (
                id text PRIMARY KEY,
                available integer
            );
        """)
        self.commit_db()

    def insert_new_user(self, user_id: str, initial_balance: int = 1000):
        """Create a new user record.

        Args:
            user_id (str): Twitch ID of user
            initial_balance (int, optional): Initial balance for new user. Defaults to 1000.
        """
        self.get_cursor().execute("""
            INSERT INTO balance VALUES (?,?)
        """, (user_id, initial_balance))
        logger.info("Created user %s with initial balance of %d.", user_id, initial_balance)

    def user_exists(self, user_id: str) -> bool:
        """Check if user exists in database.

        Args:
            user_id (str): Twitch ID of user

        Returns:
            bool: True if exists, else False.
        """
        results = self.get_cursor().execute("SELECT * FROM balance WHERE id = ?", (user_id,)).fetchall()
        if len(results) == 0:
            return False
        return True

    def get_balance(self, user_id: str) -> int:
        """Get current balance of a user

        Args:
            user_id (str): Twitch ID of user

        Returns:
            int: Current balance of the user
        """
        # Check if user exists or not. If not, create a new record.
        if not self.user_exists(user_id):
            self.insert_new_user(user_id)
            self.commit_db()

        result: Tuple[str, int] = self.get_cursor().execute(
            "SELECT * FROM balance WHERE id = ?", (user_id,)
        ).fetchone()

        return result[1]

    def bet(self, user_id: str, amount: int) -> bool:
        """Subtract amount from user's available balance (if enough).

        Args:
            user_id (str): Twitch ID of user
            amount (int): Amount to subtract

        Returns:
            bool: Whether if the amount was subtracted (True) or not (False).
        """
        current_balance = self.get_balance(user_id)
        new_balance = current_balance - amount
        if new_balance < 0:
            logging.debug("Bet command from %s is not processed. Reason: insufficient balance.", user_id)
            return False

        # Update new balance
        self.get_cursor().execute(
            "UPDATE balance SET available = ? WHERE id = ?",
            (new_balance, user_id)
        )
        self.commit_db()
        logger.debug(
            "Subtracted %d from the balance of %s. New balance: %d",
            amount, user_id, new_balance
        )
        return True

    def award(self, user_id: str, amount: int) -> int:
        """Award amount to user's available balance.

        Args:
            user_id (str): Twitch ID of user
            amount (int): Amount to add

        Returns:
            int: New balance
        """
        current_balance = self.get_balance(user_id)
        new_balance = current_balance + amount

        # Update new balance
        self.get_cursor().execute(
            "UPDATE balance SET available = ? WHERE id = ?",
            (new_balance, user_id)
        )
        self.commit_db()
        logger.debug(
            "Added %d to the balance of %s. New balance: %d",
            amount, user_id, new_balance
        )
        return new_balance
