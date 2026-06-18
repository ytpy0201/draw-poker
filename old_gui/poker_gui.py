import tkinter as tk
import random
import poker_logic

class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw Poker")
        self.root.geometry("350x600")

        # ゲームの状態を管理するプロパティ（globalの代わり）
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.card_vars = []

        # 画面の構築
        self.setup_ui()

    def setup_ui(self):
        """ウィジェットの初期配置を行う"""
        title_label = tk.Label(self.root, text="Draw Poker", font=("Meiryo", 16))
        title_label.pack(pady=10)

        start_button = tk.Button(self.root, text="ゲーム開始", command=self.start_game)
        start_button.pack(pady=10)

        self.cards_frame = tk.Frame(self.root)
        self.cards_frame.pack(pady=10)

        # 初期状態は無効(disabled)にして誤操作を防ぐ
        self.exchange_button = tk.Button(
            self.root, text="交換する", command=self.exchange_cards_gui, state="disabled"
        )
        self.exchange_button.pack(pady=10)

        self.role_label = tk.Label(self.root, text="あなたの役：")
        self.role_label.pack(pady=5)

        dealer_title_label = tk.Label(self.root, text="ディーラーの手札")
        dealer_title_label.pack()

        self.dealer_cards_frame = tk.Frame(self.root)
        self.dealer_cards_frame.pack(pady=10)

        self.dealer_role_label = tk.Label(self.root, text="ディーラーの役：")
        self.dealer_role_label.pack(pady=5)

        self.result_label = tk.Label(self.root, text="結果：")
        self.result_label.pack(pady=5)

    def show_hand(self):
        """プレイヤーの手札（チェックボックス）を表示する"""
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        self.card_vars = []
        for i, card in enumerate(self.player_hand):
            var = tk.BooleanVar()
            check = tk.Checkbutton(self.cards_frame, text=card, variable=var, font=("Meiryo", 12))
            check.grid(row=0, column=i, padx=5)
            self.card_vars.append(var)

    def show_dealer_hand(self):
        """ディーラーの手札を表示する"""
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(self.dealer_hand):
            label = tk.Label(self.dealer_cards_frame, text=card, font=("Meiryo", 12))
            label.grid(row=0, column=i, padx=5)

    def start_game(self):
        """ゲームを初期化して開始する"""
        self.deck = poker_logic.make_deck()
        random.shuffle(self.deck)

        self.player_hand = []
        self.dealer_hand = []

        poker_logic.deal_cards(self.deck, self.player_hand)
        poker_logic.deal_cards(self.deck, self.dealer_hand)

        self.show_hand()
        
        # 次のゲーム開始時に前回のディーラー手札をクリア
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()

        # ボタンを有効化
        self.exchange_button.config(state="normal")

        player_role = poker_logic.judge_hand(self.player_hand)
        self.role_label.config(text=f"あなたの役：{player_role}")
        self.dealer_role_label.config(text="ディーラーの役：？？？")
        self.result_label.config(text="結果：")

    def exchange_cards_gui(self):
        """選択されたカードを交換し、結果を判定する"""
        selected_indexes = [i for i, var in enumerate(self.card_vars) if var.get()]

        # 後ろのインデックスから順に削除（安全な削除）
        for index in sorted(selected_indexes, reverse=True):
            del self.player_hand[index]

        while len(self.player_hand) < 5:
            self.player_hand.append(self.deck.pop())

        self.show_hand()

        # 役の判定と勝敗比較
        player_role = poker_logic.judge_hand(self.player_hand)
        dealer_role = poker_logic.judge_hand(self.dealer_hand)
        result = poker_logic.compare_hands(player_role, dealer_role)

        # 画面表示の更新
        self.role_label.config(text=f"あなたの役：{player_role}")
        self.dealer_role_label.config(text=f"ディーラーの役：{dealer_role}")
        self.result_label.config(text=f"結果：{result}")

        self.show_dealer_hand()
        
        # 交換後はボタンを無効化
        self.exchange_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()