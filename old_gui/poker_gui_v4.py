import tkinter as tk
import random

import poker_logic


player_hand = []
dealer_hand = []
deck = []

card_vars = []


def show_hand():

    global card_vars

    for widget in cards_frame.winfo_children():
        widget.destroy()

    card_vars = []

    for i, card in enumerate(player_hand):

        var = tk.BooleanVar()

        check = tk.Checkbutton(
            cards_frame,
            text=card,
            variable=var
        )

        check.grid(
            row=0,
            column=i,
            padx=5
        )

        card_vars.append(var)


def show_dealer_hand():

    for widget in dealer_cards_frame.winfo_children():
        widget.destroy()

    for i, card in enumerate(dealer_hand):

        label = tk.Label(
            dealer_cards_frame,
            text=card,
            font=("Meiryo", 12)
        )

        label.grid(
            row=0,
            column=i,
            padx=5
        )


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

    exchange_button.config(state="normal")

    for widget in dealer_cards_frame.winfo_children():
        widget.destroy()

    player_role = poker_logic.judge_hand(player_hand)

    role_label.config(
        text=f"あなたの役：{player_role}"
    )

    dealer_role_label.config(
        text="ディーラーの役：？？？"
    )

    result_label.config(
        text="結果："
    )


def exchange_cards_gui():

    global player_hand
    global deck

    selected_indexes = []

    for i, var in enumerate(card_vars):

        if var.get():
            selected_indexes.append(i)

    for index in sorted(selected_indexes, reverse=True):
        del player_hand[index]

    while len(player_hand) < 5:
        player_hand.append(deck.pop())

    show_hand()

    player_role = poker_logic.judge_hand(player_hand)
    dealer_role = poker_logic.judge_hand(dealer_hand)

    result = poker_logic.compare_hands(
        player_role,
        dealer_role
    )

    role_label.config(
        text=f"あなたの役：{player_role}"
    )

    dealer_role_label.config(
        text=f"ディーラーの役：{dealer_role}"
    )

    result_label.config(
        text=f"結果：{result}"
    )

    show_dealer_hand()

    exchange_button.config(state="disabled")


root = tk.Tk()

root.title("Draw Poker")
root.geometry("350x600")


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


exchange_button = tk.Button(
    root,
    text="交換する",
    command=exchange_cards_gui
)
exchange_button.pack(pady=10)


role_label = tk.Label(
    root,
    text="あなたの役："
)
role_label.pack(pady=5)


dealer_title_label = tk.Label(
    root,
    text="ディーラーの手札"
)
dealer_title_label.pack()


dealer_cards_frame = tk.Frame(root)
dealer_cards_frame.pack(pady=10)


dealer_role_label = tk.Label(
    root,
    text="ディーラーの役："
)
dealer_role_label.pack(pady=5)


result_label = tk.Label(
    root,
    text="結果："
)
result_label.pack(pady=5)


root.mainloop()