import random
import sys
import time
from abc import ABC, abstractmethod

random.seed()

class Die:
    def roll(self):
        return random.randint(1, 6)

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.total_score = 0
    
    def reset(self):
        self.total_score = 0

    @abstractmethod
    def decide_roll_or_hold(self, turn_score):
        pass

class HumanPlayer(Player):
    def decide_roll_or_hold(self, turn_score):
        return input("Roll again or hold? (r/h): ").strip().lower() == 'r'

class ComputerPlayer(Player):
    def decide_roll_or_hold(self, turn_score):
        threshold = min(25, 100 - self.total_score)
        return turn_score < threshold

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Unknown player type")

class Game:
    def __init__(self, player_types, num_players=2):
        self.players = [PlayerFactory.create_player(player_types[i], f"Player {i+1}") for i in range(num_players)]
        self.die = Die()
        self.current_player_index = 0
    
    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def play_turn(self, player):
        turn_score = 0
        while True:
            roll = self.die.roll()
            print(f"{player.name} rolled a {roll}.")
            if roll == 1:
                print(f"Sorry, {player.name}, you scored nothing this turn.")
                break
            else:
                turn_score += roll
                print(f"Current turn score: {turn_score}, Total score: {player.total_score}")
                if not player.decide_roll_or_hold(turn_score):
                    player.total_score += turn_score
                    print(f"{player.name} holds with a turn score of {turn_score}, total score: {player.total_score}.")
                    break
    
    def play_game(self):
        while True:
            for player in self.players:
                player.reset()
            self.current_player_index = 0
            while all(player.total_score < 100 for player in self.players):
                current_player = self.players[self.current_player_index]
                print(f"\n{current_player.name}'s turn:")
                self.play_turn(current_player)
                if current_player.total_score >= 100:
                    print(f"{current_player.name} wins with a score of {current_player.total_score}!")
                    break
                self.switch_player()
            if input("\nPlay another game? (yes/no): ").strip().lower() != 'yes':
                break

class TimedGameProxy(Game):
    def play_game(self):
        start_time = time.time()
        while True:
            for player in self.players:
                player.reset()
            self.current_player_index = 0
            while all(player.total_score < 100 for player in self.players) and time.time() - start_time < 60:
                current_player = self.players[self.current_player_index]
                print(f"\n{current_player.name}'s turn:")
                self.play_turn(current_player)
                if current_player.total_score >= 100:
                    print(f"{current_player.name} wins with a score of {current_player.total_score}!")
                    break
                self.switch_player()
            else:
                winner = max(self.players, key=lambda p: p.total_score)
                print(f"Time's up! {winner.name} wins with the highest score of {winner.total_score}!")
            if input("\nPlay another game? (yes/no): ").strip().lower() != 'yes':
                break

if __name__ == "__main__":
    player_types = ['human', 'human']
    timed = False

    for i, arg in enumerate(sys.argv):
        if arg == "--player1":
            player_types[0] = sys.argv[i + 1]
        elif arg == "--player2":
            player_types[1] = sys.argv[i + 1]
        elif arg == "--timed":
            timed = True

    if timed:
        game = TimedGameProxy(player_types=player_types)
    else:
        game = Game(player_types=player_types)
    
    game.play_game()