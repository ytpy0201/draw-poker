from collections import Counter

# 役の強さを定義する定数
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

def judge_hand(hand):
    ranks = rank_in_hand(hand)
    values = Counter(ranks).values()
    counts = sorted(values)

    is_royal = royal(hand)
    is_flush = flush(hand)
    is_straight = straight(hand)

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

def rank_in_hand(hand):
    return [card[1:] for card in hand]

def suit_in_hand(hand):
    return [card[0] for card in hand]

def royal(hand):
    if flush(hand):
        numbers = sorted(change_num(hand))
        return numbers == [10, 11, 12, 13, 14]
    return False

def flush(hand):
    suits = suit_in_hand(hand)
    return len(set(suits)) == 1

def straight(hand):
    numbers = sorted(change_num(hand))
    
    # A-5の例外処理
    if numbers == [2, 3, 4, 5, 14]:
        return True
    
    # すべての隣り合うカードの差が1であるか確認
    return all(numbers[i + 1] - numbers[i] == 1 for i in range(4))

def change_num(hand):
    ranks = rank_in_hand(hand)
    convert = {"J": 11, "Q": 12, "K": 13, "A": 14}
    
    # 内包表記を使ってすっきりと記述
    return [convert[rank] if rank in convert else int(rank) for rank in ranks]

def compare_hands(player_role, dealer_role):
    if HAND_RANK[player_role] > HAND_RANK[dealer_role]:
        return "勝ち"
    elif HAND_RANK[player_role] < HAND_RANK[dealer_role]:
        return "負け"
    else:
        return "引き分け"

def make_deck():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    return [f"{suit}{rank}" for suit in suits for rank in ranks]

def deal_cards(deck, hand_list):
    for _ in range(5):
        hand_list.append(deck.pop())