import tkinter as tk
import random

import poker_logic


def start_game():

    deck = poker_logic.make_deck()
    random.shuffle(deck)

    player_hand = []

    poker_logic.deal_cards(deck, player_hand)

    hand_text = ""

    for i, card in enumerate(player_hand, start=1):
        hand_text += f"{i}: {card}\n"

    hand_label.config(text=hand_text)


root = tk.Tk()

root.title("Draw Poker")
root.geometry("300x300")

title_label = tk.Label(
    root,
    text="Draw Poker",
    font=("Meiryo", 16)
)
title_label.pack(pady=10)

start_button = tk.Button(
    root,
    text="ゲーム開始",
    command=start_game
)
start_button.pack(pady=10)

hand_label = tk.Label(
    root,
    text="ゲーム開始を押してください",
    justify="left",
    font=("Meiryo", 12)
)
hand_label.pack(pady=10)

root.mainloop()