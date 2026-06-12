import tkinter as tk
import random
import poker_logic


#ウィンドウ
root = tk.Tk()
root.title("Draw Poker")

#Label == 文字を表示する
hand_label = tk.Label(root, text="")
hand_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()


def start_game():

    deck = poker_logic.make_deck()
    random.shuffle(deck)

    player_hand = []
    dealer_hand = []

    poker_logic.deal_cards(deck, player_hand)
    poker_logic.deal_cards(deck, dealer_hand)

    hand_label.config(
        text="\n".join(player_hand)
    )

start_button = tk.Button(
    root,
    text="ゲーム開始",
    command=start_game
)

start_button.pack()

root.mainloop()