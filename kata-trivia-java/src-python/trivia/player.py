
class Player:
    def __init__(self, name: str):
        self.name         = name
        self.position     = 0
        self.coins        = 0
        self.in_penalty_box = False
    def advance(self, roll: int, board_size: int):
        self.position = ((self.position - 1 + roll) % board_size) + 1

    def add_coin(self):
        self.coins += 1

    def send_to_penalty_box(self):
        self.in_penalty_box = True

    def has_won(self, winning_coins: int) -> bool:
        return self.coins >= winning_coins
