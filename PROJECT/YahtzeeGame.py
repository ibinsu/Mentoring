import tkinter as tk
from random import randint
from tkinter import messagebox


class YahtzeeGame:
    def __init__(self, master, num_players=2):
        self.master = master
        self.master.title("Yahtzee Game")

        self.num_players = num_players
        self.current_player = 0
        self.players = [f"플레이어 {i + 1}" for i in range(num_players)]
        self.total_turns = 0
        self.max_turns = 13

        self.player_turn_label = tk.Label(self.master, text="")
        self.player_turn_label.pack()

        self.dice_frame = tk.Frame(self.master)
        self.dice_frame.pack(pady=10)
        self.dice_values = [0] * 5
        self.selected_dice = [False] * 5
        self.roll_count = 0
        self.max_rolls = 3

        self.dice_buttons = []
        for i in range(5):
            button = tk.Button(self.dice_frame, text="-", width=2, height=1, command=lambda i=i: self.toggle_dice(i))
            button.pack(side=tk.LEFT, padx=5)
            self.dice_buttons.append(button)

        roll_button = tk.Button(self.dice_frame, text="Roll Dice", command=self.roll_dice)
        roll_button.pack()

        self.roll_count_label = tk.Label(self.dice_frame, text="Roll {}/{}".format(self.roll_count, self.max_rolls))
        self.roll_count_label.pack()

        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(pady=10)
        self.create_score_table()


        self.update_player_turn()

    def roll_dice(self):
        if self.roll_count < self.max_rolls:
            self.roll_count += 1
            self.roll_count_label.config(text="Roll {}/{}".format(self.roll_count, self.max_rolls))
            for i in range(5):
                if not self.selected_dice[i]:
                    self.dice_values[i] = randint(1, 6)
                    self.dice_buttons[i].config(text=str(self.dice_values[i]))

    def toggle_dice(self, index):
        self.selected_dice[index] = not self.selected_dice[index]
        if self.selected_dice[index]:
            self.dice_buttons[index].config(relief=tk.SUNKEN)
        else:
            self.dice_buttons[index].config(relief=tk.RAISED)

    def create_score_table(self):
        self.categories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Bonus",
                           "Three of a Kind", "Four of a Kind", "Full House",
                           "Small Straight", "Large Straight", "Yahtzee", "Chance","Total"]

        self.scores = [{category: None for category in self.categories} for _ in range(2)]
        for row, category in enumerate(self.categories):
            category_label = tk.Label(self.score_frame, text=category, width=15, borderwidth=1, relief="solid")
            category_label.grid(row=row, column=0)

            score_label1 = tk.Label(self.score_frame, text="-", width=5, borderwidth=1, relief="solid")
            score_label1.grid(row=row, column=1)
            score_label2 = tk.Label(self.score_frame, text="-", width=5, borderwidth=1, relief="solid")
            score_label2.grid(row=row, column=2)

            if category not in ["Bonus","Total"]:
                score_button = tk.Button(self.score_frame, text="Set Score",command=lambda cat=category: self.set_score(cat))
                score_button.grid(row=row, column=3)

    def set_score(self, category):
        cur = self.current_player
        if all(value == 0 for value in self.dice_values):
            return

        if self.scores[cur][category] is None :  # 이미 점수가 있으면 설정하지 않음
            points = self.calculate_points(category)
            self.scores[cur][category] = points

            # 표에 설정한 점수 업데이트
            index = self.categories.index(category)
            score_label = self.score_frame.grid_slaves(row=index, column=cur+1)[0]
            score_label.config(text=str(points))

            if category in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
                # Calculate sum of Ones to Sixes
                upper_section_sum = sum(
                    self.scores[cur][cat] for cat in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"] if
                    self.scores[cur][cat] is not None)
                index = self.categories.index("Bonus")
                # Check if the sum is 63 or more, and if so, add bonus points
                if upper_section_sum >= 63:
                    bonus_points = 35
                    self.scores[cur]["Bonus"] = bonus_points
                    bonus_label = self.score_frame.grid_slaves(row=index, column=cur + 1)[0]
                    bonus_label.config(text=str(bonus_points))

            index = self.categories.index("Total")
            total_score = 0
            for category in self.categories:
                if self.scores[cur][category] is not None:
                    total_score += self.scores[cur][category]
                    total_label = self.score_frame.grid_slaves(row=index, column=cur + 1)[0]
                    total_label.config(text=str(total_score))
            self.scores[cur]["Total"] = total_score


            self.current_player = (self.current_player + 1) % self.num_players
            self.update_player_turn()

    def calculate_points(self, category):
        # Check for categories Ones to Sixes
        if category in ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes']:
            if category == 'Ones':
                value = 1
            elif category == 'Twos':
                value = 2
            elif category == 'Threes':
                value = 3
            elif category == 'Fours':
                value = 4
            elif category == 'Fives':
                value = 5
            elif category == 'Sixes':
                value = 6
            return self.dice_values.count(value) * value


        # Three of a Kind
        elif category == 'Three of a Kind':
            for value in set(self.dice_values):
                if self.dice_values.count(value) >= 3:
                    return sum(self.dice_values)
            return 0

        # Four of a Kind
        elif category == 'Four of a Kind':
            for value in set(self.dice_values):
                if self.dice_values.count(value) >= 4:
                    return sum(self.dice_values)
            return 0

        # Full House
        elif category == 'Full House':
            counts = [self.dice_values.count(value) for value in set(self.dice_values)]
            if 2 in counts and 3 in counts:
                return 25
            return 0

        # Small Straight
        elif category == 'Small Straight':
            sorted_values = sorted(set(self.dice_values))
            if any(sorted_values[i] + 1 != sorted_values[i + 1] for i in range(len(sorted_values) - 1)):
                return 0
            return 30

        # Large Straight
        elif category == 'Large Straight':
            sorted_values = sorted(set(self.dice_values))
            if sorted_values != [1, 2, 3, 4, 5] and sorted_values != [2, 3, 4, 5, 6]:
                return 0
            return 40

        # Yahtzee
        elif category == 'Yahtzee':
            if self.dice_values.count(self.dice_values[0]) == 5:
                return 50
            return 0

        # Chance
        elif category == 'Chance':
            return sum(self.dice_values)

        # Invalid category
        else:
            return 0

    def reset_dice(self):
        self.dice_values = [0] * 5
        self.selected_dice = [False] * 5
        self.roll_count = 0

        self.roll_count_label.config(text="Roll {}/{}".format(self.roll_count, self.max_rolls))
        for i in range(5):
            self.dice_buttons[i].config(text="-")
            self.dice_buttons[i].config(relief=tk.RAISED)

    def update_player_turn(self):
        if self.current_player == 0:
            self.total_turns += 1
        self.reset_dice()
        self.player_turn_label.config(text=f"{self.total_turns}/{self.max_turns} {self.players[self.current_player]}의 차례입니다!")
        if self.total_turns > self.max_turns:
            self.determine_winner()


    def determine_winner(self):
        total_score_player1 = self.scores[0]["Total"]
        total_score_player2 = self.scores[1]["Total"]

        if total_score_player1 > total_score_player2:
            winner = self.players[0]
        elif total_score_player1 < total_score_player2:
            winner = self.players[1]
        else:
            winner = "It's a tie!"

        message = f"Winner: {winner}"
        messagebox.showinfo("Game Result", message)
        self.reset_game()

    def reset_game(self):
        # Reset all game-related variables
        self.current_player = 0
        self.total_turns = 0

        # Reset scores
        for cur in range(2):
            for category in self.categories:
                self.scores[cur][category] = None
                index = self.categories.index(category)
                bonus_label = self.score_frame.grid_slaves(row=index, column=cur + 1)[0]
                bonus_label.config(text="-")

        # Reset dice and roll count
        self.reset_dice()
        # Update player turn label
        self.update_player_turn()


if __name__ == "__main__":
    root = tk.Tk()
    yahtzee_game = YahtzeeGame(root, num_players=2)
    root.mainloop()
