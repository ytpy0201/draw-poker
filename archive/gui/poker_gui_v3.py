import tkinter as tk
import random

import poker_logic


# ------------------
# グローバル変数
# ------------------

player_hand = []
dealer_hand = []
deck = []

card_vars = []


# ------------------
# 手札表示
# ------------------

def show_hand():

    global card_vars

    # 古いチェックボックスを削除
    for widget in cards_frame.winfo_children():
        widget.destroy()

    card_vars = []

    # 新しいチェックボックスを作成
    for card in player_hand:

        var = tk.BooleanVar()

        check = tk.Checkbutton(
            cards_frame,
            text=card,
            variable=var
        )

        check.pack(anchor="w")

        card_vars.append(var)


# ------------------
# ゲーム開始
# ------------------

def start_game():

    global player_hand
    global dealer_hand
    global deck

    deck = poker_logic.make_deck()
    random.shuffle(deck)

    player_hand = []
    dealer_hand = []

    poker_logic.deal_cards(deck, player_hand)
    poker_logic.deal_cards(deck, dealer_hand)

    show_hand()


# ------------------
# GUI
# ------------------

root = tk.Tk()

root.title("Draw Poker")
root.geometry("300x400")


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


cards_frame = tk.Frame(root)
cards_frame.pack(pady=10)


root.mainloop()