import random
from collections import Counter
import itertools

# --- 役の判定ロジック（以前のコードを再利用） ---
HAND_RANK = {
    "役なし": 0, "ワンペア": 1, "ツーペア": 2, "スリーカード": 3,
    "ストレート": 4, "フラッシュ": 5, "フルハウス": 6, "フォーカード": 7,
    "ストレートフラッシュ": 8, "ロイヤルストレートフラッシュ": 9
}

def rank_in_hand(hand): return [card[1:] for card in hand]
def suit_in_hand(hand): return [card[0] for card in hand]

def change_num(hand):
    ranks = rank_in_hand(hand)
    convert = {"J": 11, "Q": 12, "K": 13, "A": 14}
    return [convert[rank] if rank in convert else int(rank) for rank in ranks]

def flush(hand): return len(set(suit_in_hand(hand))) == 1

def straight(hand):
    numbers = sorted(change_num(hand))
    if numbers == [2, 3, 4, 5, 14]: return True
    return all(numbers[i + 1] - numbers[i] == 1 for i in range(4))

def royal(hand):
    if flush(hand):
        return sorted(change_num(hand)) == [10, 11, 12, 13, 14]
    return False

def judge_five_cards(hand):
    """5枚のカードの役を判定する"""
    ranks = rank_in_hand(hand)
    counts = sorted(Counter(ranks).values())
    is_royal, is_flush, is_straight = royal(hand), flush(hand), straight(hand)

    if is_royal: return "ロイヤルストレートフラッシュ"
    if is_flush and is_straight: return "ストレートフラッシュ"
    if counts == [1, 4]: return "フォーカード"
    if counts == [2, 3]: return "フルハウス"
    if is_flush: return "フラッシュ"
    if is_straight: return "ストレート"
    if counts == [1, 1, 3]: return "スリーカード"
    if counts == [1, 2, 2]: return "ツーペア"
    if counts == [1, 1, 1, 2]: return "ワンペア"
    return "役なし"

def get_best_hand(seven_cards):
    """7枚のカードから最強の5枚の役を見つける"""
    best_rank = -1
    best_role = "役なし"
    
    # itertools.combinationsを使って7枚から5枚を選ぶ全組み合わせ(21通り)を試す
    for five_cards in itertools.combinations(seven_cards, 5):
        role = judge_five_cards(list(five_cards))
        rank = HAND_RANK[role]
        if rank > best_rank:
            best_rank = rank
            best_role = role
            
    return best_role, best_rank

# --- ゲーム進行ロジック ---
def make_deck():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    return [f"{suit}{rank}" for suit in suits for rank in ranks]

def play_texas_holdem():
    deck = make_deck()
    random.shuffle(deck)

    # 1. プリフロップ（手札を2枚ずつ配る）
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    community_cards = []

    print("\n" + "="*30)
    print("♠♥ テキサスホールデム ♦♣")
    print("="*30)
    print(f"あなたの手札: {player_hand}")
    input("Enterを押してフロップ（共有カード3枚）へ...")

    # 2. フロップ（共有カード3枚）
    community_cards.extend([deck.pop(), deck.pop(), deck.pop()])
    print(f"\n[フロップ] 共有カード: {community_cards}")
    print(f"あなたの手札: {player_hand}")
    input("Enterを押してターン（共有カード1枚追加）へ...")

    # 3. ターン（共有カード1枚）
    community_cards.append(deck.pop())
    print(f"\n[ターン] 共有カード: {community_cards}")
    print(f"あなたの手札: {player_hand}")
    input("Enterを押してリバー（共有カード1枚追加）へ...")

    # 4. リバー（共有カード1枚）
    community_cards.append(deck.pop())
    print(f"\n[リバー] 共有カード: {community_cards}")
    print(f"あなたの手札: {player_hand}")
    input("\nEnterを押してショーダウン（判定）へ...！")

    # 5. ショーダウン（勝敗判定）
    print("\n" + "="*30)
    print("✨ ショーダウン ✨")
    print("="*30)
    print(f"最終共有カード: {community_cards}")
    print(f"あなたの手札: {player_hand}")
    print(f"ディーラーの手札: {dealer_hand}")

    # 7枚のカードを結合
    player_seven = player_hand + community_cards
    dealer_seven = dealer_hand + community_cards

    # 最強の役を計算
    player_role, player_rank = get_best_hand(player_seven)
    dealer_role, dealer_rank = get_best_hand(dealer_seven)

    print(f"\nあなたの役: {player_role}")
    print(f"ディーラーの役: {dealer_role}")

    if player_rank > dealer_rank:
        print("\n🎉 あなたの勝ちです！ 🎉")
    elif player_rank < dealer_rank:
        print("\n💀 あなたの負けです... 💀")
    else:
        print("\n🤝 引き分け（チョップ）です 🤝")

if __name__ == "__main__":
    while True:
        play_texas_holdem()
        answer = input("\nもう一回プレイしますか？ (y/n): ")
        if answer.lower() != "y":
            print("Thank you for playing!")
            break