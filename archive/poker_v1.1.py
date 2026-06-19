import random
from collections import Counter

class PokerGame:
    # クラス定数（全インスタンスで共通の設定）
    HAND_RANK = {
        "役なし": 0,
        "ワンペア": 1,
        "ツーペア": 2,
        "スリーカード": 3,
        "ストレート": 4,
        "フラッシュ": 5,
        "フルハウス": 6,
        "フォーカード": 7,
        "ストレートフラッシュ": 8,
        "ロイヤルストレートフラッシュ": 9
    }

    def __init__(self):
        """インスタンス変数の初期化"""
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

    def play_game(self):
        """1ゲームの流れを制御する"""
        self._make_deck()
        
        self.player_hand = self._deal_cards()
        self.dealer_hand = self._deal_cards()

        self.player_hand = self._exchange_cards(self.player_hand)

        print(f"\nあなたの手札：\n{self.player_hand}")
        print(f"ディーラー：\n{self.dealer_hand}")

        player_role = self._judge_hand(self.player_hand)
        dealer_role = self._judge_hand(self.dealer_hand)

        print(f"\nプレイヤー：{player_role}")
        print(f"ディーラー：{dealer_role}")

        print(f"\n判定：{self._compare_hands(player_role, dealer_role)}")

    def start(self):
        """ゲームループを開始する"""
        while True:
            self.play_game()

            answer = input("\nもう一回？ (y/n)：")

            if answer.lower() != "y":
                print("Thank you for playing.")
                break

    # ----------------------------------------------------
    # 以下、クラス内部で使用するプライベートメソッド（_で開始）
    # ----------------------------------------------------

    def _make_deck(self):
        """デッキを作成しシャッフルする"""
        self.deck = []
        suits = ["♠", "♥", "♦", "♣"]
        ranks = ["A", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "J", "Q", "K"]

        for suit in suits:
            for rank in ranks:
                self.deck.append(f"{suit}{rank}")
        
        random.shuffle(self.deck)

    def _deal_cards(self):
        """デッキから5枚のカードを引いて返す"""
        return [self.deck.pop() for _ in range(5)]

    def _exchange_cards(self, hand):
        """プレイヤーのカード交換処理"""
        print("\nあなたのハンド:")

        for i, card in enumerate(hand, start=1):
            print(f"{i}: {card}")

        while True:
            choice = input("\n交換したいカードの番号をスペース区切りで入力 \nなければEnter：")

            if choice == "":
                return hand
            
            indexes = choice.split()
            valid = True

            for index in indexes:
                if not index.isdigit():
                    valid = False
                elif not 1 <= int(index) <= 5:
                    valid = False

            if len(indexes) != len(set(indexes)):
                print("同じ番号は入力できません")
                continue        

            if not valid:
                print("１～５の数字を入力してください。")
                continue

            break

        # 昇順にして削除（インデックスのズレを防ぐため後ろから削除）
        for index in sorted(indexes, reverse=True):
            del hand[int(index) - 1]

        # 足りない分をデッキから補充
        while len(hand) < 5:
            hand.append(self.deck.pop())

        return hand

    def _judge_hand(self, hand):
        """役の判定"""
        ranks = self._rank_in_hand(hand)
        values = Counter(ranks).values()
        counts = sorted(values)

        is_royal = self._royal(hand)
        is_flush = self._flush(hand)
        is_straight = self._straight(hand)

        if is_royal:
            return "ロイヤルストレートフラッシュ"
        elif is_flush and is_straight:
            return "ストレートフラッシュ"
        elif counts == [1, 4]:
            return "フォーカード"
        elif counts == [2, 3]:
            return "フルハウス"
        elif is_flush:
            return "フラッシュ"
        elif is_straight:
            return "ストレート"
        elif counts == [1, 1, 3]:
            return "スリーカード"
        elif counts == [1, 2, 2]:
            return "ツーペア"
        elif counts == [1, 1, 1, 2]:
            return "ワンペア"
        else:
            return "役なし"

    def _rank_in_hand(self, hand):
        return [card[1:] for card in hand]

    def _suit_in_hand(self, hand):
        return [card[0] for card in hand]

    def _royal(self, hand):
        if self._flush(hand):
            nums = sorted(self._change_num(hand))
            if nums == [10, 11, 12, 13, 14]:
                return True
        return False

    def _flush(self, hand):
        suits = self._suit_in_hand(hand)
        return len(set(suits)) == 1

    def _straight(self, hand):
        numbers = sorted(self._change_num(hand))
        
        if numbers == [2, 3, 4, 5, 14]:
            return True
        
        for i in range(4):
            if numbers[i + 1] - numbers[i] != 1:
                return False
        return True

    def _change_num(self, hand):
        """カードの数字を判定用のint型リストに変換"""
        ranks = self._rank_in_hand(hand)
        convert = {"J": 11, "Q": 12, "K": 13, "A": 14}
        converted = []
        
        for rank in ranks:
            if rank in convert:
                converted.append(convert[rank])
            else:
                converted.append(int(rank))
            
        return converted

    def _compare_hands(self, player_role, dealer_role):
        """プレイヤーとディーラーの役の強さを比較"""
        if self.HAND_RANK[player_role] > self.HAND_RANK[dealer_role]:
            return "勝ち"
        elif self.HAND_RANK[player_role] < self.HAND_RANK[dealer_role]:
            return "負け"
        else:
            return "引き分け"


if __name__ == "__main__":
    # クラスのインスタンス化とゲームの開始
    game = PokerGame()
    game.start()