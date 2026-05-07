from collections import deque
# Andrés Jaime Rodríguez - 2024-06
from trivia.player import Player

# REFACTOR ME
class Game:
    BOARD_SIZE = 12
    WINNING_COINS = 6
    MAX_PLAYERS = 4
    QUESTION_PER_CATEGORY = 50
       
    def __init__(self):

        self.players_list = []
        # por qué son 6? y qué significa ganar 6?
        self.players = []
        self.places = [0] * self.BOARD_SIZE  # posición del jugador i
        self.purses = [0] * self.BOARD_SIZE  # monedas del jugador i
        self.in_penalty_box = [False] * self.BOARD_SIZE  # ¿está en penalti el jugador i?

        # agregamos el atributo players_list para almacenar los objetos Player, lo que 
        # mejora la legibilidad del código y evita el uso de índices 
        # para acceder a las propiedades de los jugadores

        self.pop_questions = deque()
        self.science_questions = deque()
        self.sports_questions = deque()
        self.rock_questions = deque()

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        # por qué son 50 preguntas? no se especifica en el código original, pero se asume que es un número suficiente para jugar sin quedarse sin preguntas
        for i in range(50):
            self.pop_questions.append(f"Pop Question {i}")
            self.science_questions.append(f"Science Question {i}")
            self.sports_questions.append(f"Sports Question {i}")
            self.rock_questions.append(self.create_rock_question(i))
    
    def add(self, player_name):
        player = Player(player_name)
        self.players_list.append(player)
        print(f"{player_name} was added")
        print(f"They are player number {len(self.players_list)}")
        return True


    def create_rock_question(self, index):
        return f"Rock Question {index}"

    def is_playable(self):
        return self.how_many_players() >= 2

    def add(self, player_name):
        self.places[self.how_many_players()] = 1
        self.purses[self.how_many_players()] = 0
        self.in_penalty_box[self.how_many_players()] = False
        self.players.append(player_name)

        print(f"{player_name} was added")
        print(f"They are player number {len(self.players)}")
        return True

    def how_many_players(self):
        return len(self.players)

# se puede refactorizar el método roll para evitar la duplicación de código 
# en el caso de estar en penalti o no, y así mejorar la legibilidad del código
    def roll(self, roll):
        print(f"{self.players[self.current_player]} is the current player")
        print(f"They have rolled a {roll}")

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(f"{self.players[self.current_player]} is getting out of the penalty box")
                self._move_and_ask(roll)
            else:
                print(f"{self.players[self.current_player]} is not getting out of the penalty box")
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
        pos = self.places[self.current_player] - 1
        if pos in (0, 4, 8):
            return "Pop"
        if pos in (1, 5, 9):
            return "Science"
        if pos in (2, 6, 10):
            return "Sports"
        return "Rock"

    def handle_correct_answer(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                self.purses[self.current_player] += 1
                print(f"{self.players[self.current_player]} now has {self.purses[self.current_player]} Gold Coins.")

                winner = self._did_player_win()
                self._advance_to_next_player()

                return winner
            else:
                self._advance_to_next_player()
                return True
        else:
            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print(f"{self.players[self.current_player]} now has {self.purses[self.current_player]} Gold Coins.")

            winner = self._did_player_win()
            self._advance_to_next_player()

            return winner

    def wrong_answer(self):
        print("Question was incorrectly answered")
        print(f"{self.players[self.current_player]} was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == self.WINNING_COINS) # añadimos la propiedad WINNING_COINS para evitar el número mágico 6
    
    def _advance_to_next_player(self):
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

#   extraemos de roll el código que mueve al jugador y pregunta 
#   para evitar la duplicación de código en el caso de estar en penalti o no
    def _move_and_ask(self, roll):
        self.places[self.current_player] += roll
        if self.places[self.current_player] > self.BOARD_SIZE:
            self.places[self.current_player] -= self.BOARD_SIZE
        print(f"{self.players[self.current_player]}'s new location is "
            f"{self.places[self.current_player]}")
        print(f"The category is {self._current_category()}")
        self._ask_question()
 
