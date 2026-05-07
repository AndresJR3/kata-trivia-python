# trivia/question_deck.py
from collections import deque

class QuestionDeck:
    CATEGORIES = ["Pop", "Science", "Sports", "Rock"]

    def __init__(self, questions_per_category: int = 50):
        self._deck = {
            "Pop":     deque(f"Pop Question {i}"     for i in range(questions_per_category)),
            "Science": deque(f"Science Question {i}" for i in range(questions_per_category)),
            "Sports":  deque(f"Sports Question {i}"  for i in range(questions_per_category)),
            "Rock":    deque(f"Rock Question {i}"    for i in range(questions_per_category)),
        }

    def next_question(self, category: str) -> str:
        return self._deck[category].popleft()

