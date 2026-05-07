from collections import deque
# Andrés Jaime Rodríguez - 2024-06
from trivia.player import Player
from trivia.question_deck import QuestionDeck


# REFACTOR ME
class Game:
    BOARD_SIZE = 12
    WINNING_COINS = 6
    MAX_PLAYERS = 4
    QUESTION_PER_CATEGORY = 50
       
    def __init__(self):

        self.players_list = []

        self.pop_questions = deque()
        self.science_questions = deque()
        self.sports_questions = deque()
        self.rock_questions = deque()

        self.question_deck = QuestionDeck(self.QUESTION_PER_CATEGORY)

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append(f"Pop Question {i}")
            self.science_questions.append(f"Science Question {i}")
            self.sports_questions.append(f"Sports Question {i}")
            self.rock_questions.append(self.create_rock_question(i))
    
    def add(self, player_name):
        player = Player(player_name)
        player.position = 1  # Initial position as per original -> 0
        self.players_list.append(player)
        print(f"{player_name} was added")
        print(f"They are player number {len(self.players_list)}")
        return True


    def create_rock_question(self, index):
        return f"Rock Question {index}"

    def is_playable(self):
        return self.how_many_players() >= 2

    def how_many_players(self):
        return len(self.players_list)

# se puede refactorizar el método roll para evitar la duplicación de código 
# en el caso de estar en penalti o no, y así mejorar la legibilidad del código
    def roll(self, roll):
        player = self.players_list[self.current_player]
        print(f"{player.name} is the current player")
        print(f"They have rolled a {roll}")

        if player.in_penalty_box:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(f"{player.name} is getting out of the penalty box")
                self._move_and_ask(roll)
            else:
                print(f"{player.name} is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            self._move_and_ask(roll)


    def _ask_question(self):
        category = self._current_category()
        if category == "Pop":
            print(self.pop_questions.popleft())
        if category == "Science":
            print(self.science_questions.popleft())
        if category == "Sports":
            print(self.sports_questions.popleft())
        if category == "Rock":
            print(self.rock_questions.popleft())

    def _current_category(self):
        player = self.players_list[self.current_player]
        pos = player.position - 1
        if pos in (0, 4, 8):
            return "Pop"
        if pos in (1, 5, 9):
            return "Science"
        if pos in (2, 6, 10):
            return "Sports"
        return "Rock"

    def handle_correct_answer(self):
        player = self.players_list[self.current_player]
        if player.in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                player.add_coin()
                print(f"{player.name} now has {player.coins} Gold Coins.")

                winner = self._did_player_win()
                self._advance_to_next_player()

                return winner
            else:
                self._advance_to_next_player()
                return True
        else:
            print("Answer was corrent!!!!")
            player.add_coin()
            print(f"{player.name} now has {player.coins} Gold Coins.")

            winner = self._did_player_win()
            self._advance_to_next_player()

            return winner

    def wrong_answer(self):
        print("Question was incorrectly answered")
        player = self.players_list[self.current_player]
        print(f"{player.name} was sent to the penalty box")
        player.send_to_penalty_box()

        self._advance_to_next_player()
        return True

    def _did_player_win(self):
        player = self.players_list[self.current_player]
        return not player.has_won(self.WINNING_COINS)
    
    def _advance_to_next_player(self):
        self.current_player += 1
        if self.current_player == len(self.players_list):
            self.current_player = 0

#   extraemos de roll el código que mueve al jugador y pregunta 
#   para evitar la duplicación de código en el caso de estar en penalti o no
    def _move_and_ask(self, roll):
        player = self.players_list[self.current_player]
        player.advance(roll, self.BOARD_SIZE)
        print(f"{player.name}'s new location is {player.position}")
        print(f"The category is {self._current_category()}")
        self._ask_question()

    def _ask_question(self):
        category = self._current_category()
        print(self.question_deck.next_question(category))

