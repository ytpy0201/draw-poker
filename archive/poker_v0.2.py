import random
from collections import Counter

# ======================
# 役を判定
# ======================
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
    return [card[1:] for card in hand]#10が二桁


def suit_in_hand(hand):
    return [card[0] for card in hand]


def royal(hand):
    if flush(hand):
        hand = sorted(change_num(hand))
        if hand == [10, 11, 12, 13, 14]:
            return True
    return False


def flush(hand):
    suits = suit_in_hand(hand)
    if len(set(suits)) == 1:
        return True
    else:
        return False


def straight(hand):

    hand = change_num(hand)
    hand = sorted(hand)
    
    
    if hand == [2, 3, 4, 5, 14]:#Aを14としているのでA-5は例外として扱う
        return True
    
    for i in range(4):

        if hand[i + 1] - hand[i] != 1:
            return False

    return True


def change_num(hand):
    """
    数字に変換
    
    辞書型の対応表を作成。Aは1だが、ロイヤルストレートの兼ね合いや、同じ役の場合Kより強い扱いになるので14として扱う。
    まずキーが対応表にあるかを判定する。対応表にあるキーはその値を、それ以外はint型に直してからのリストに追加する。
    """
    ranks = rank_in_hand(hand)
    convert = {
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
}
    converted = []
    
    for rank in ranks:
        if rank in convert:
            converted.append(convert[rank])
        else:
            converted.append(int(rank))
        
    return converted


# ======================
# デッキ作成
# ======================
deck = []
suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7",
         "8", "9", "10", "J", "Q", "K"]

for suit in suits:
    for rank in ranks:
        deck.append(f"{suit}{rank}")


random.shuffle(deck)


# ======================
# ハンドを配る
# ======================
hands = [[],[],[],[]]

for _ in range(5):
    for hand in hands:
        hand.append(deck.pop())

for i, hand in enumerate(hands, start=1):
    print(f"Player{i}: {hand}")

# ======================
# ハンドを交換
# ======================

# ======================
# ハンドの役を判定
# ======================

# ======================
# 勝敗判定
# ======================

# ======================
# ハンドをデッキに戻す
# ======================
