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
    #10が二桁
    return [card[1:] for card in hand]


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

    numbers = sorted(change_num(hand))
    
    #Aを14としているのでA-5は例外として扱う
    if numbers == [2, 3, 4, 5, 14]:
        return True
    
    for i in range(4):

        if numbers[i + 1] - numbers[i] != 1:
            return False

    return True


def change_num(hand):
    """
    数字に変換
    
    辞書型の対応表を作成。Aは1だが、ロイヤルストレートの兼ね合いや、同じ役の場合Kより強い扱いになるので14として扱う。
    まずキーが対応表にあるかを判定する。対応表にあるキーはその値を、それ以外はint型に直してからリストに追加する。
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


def exchange_cards(hand, deck):
    print("\nあなたのハンド:")

    for i, card in enumerate(hand, start=1):
        print(f"{i}: {card}")

    choice = input("番号をスペース区切りで入力: ")

    if choice == "":
        return hand
    
    indexes = choice.split()

    for index in sorted(indexes, reverse=True):
        del hand[int(index) - 1]

    while len(hand) < 5:
        hand.append(deck.pop())

    return hand

def compare_hands(player_role, dealer_role):
    if HAND_RANK[player_role] > HAND_RANK[dealer_role]:
        return "勝ち"
    
    elif HAND_RANK[player_role] < HAND_RANK[dealer_role]:
        return "負け"
    
    else:
        return "引き分け"














# ======================
# ランク対応
# ======================
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
player_hand = []
dealer_hand = []

for _ in range(5):
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())


# ======================
# ハンドを交換
# ======================
#.copy()は[:]で代替可能
before_hand = player_hand.copy()
player_hand = exchange_cards(player_hand, deck)

print(player_hand)


# ======================
# ハンドの役を判定
# ======================
before_role = judge_hand(before_hand)
player_role = judge_hand(player_hand)

print(f"交換前：{before_role}")
print(f"交換後：{player_role}")


# ======================
# 勝敗判定
# ======================
dealer_role = judge_hand(dealer_hand)

print(f"プレイヤー：{player_role}")
print(f"ディーラー：{dealer_role}")

print(f"判定：{compare_hands(player_role, dealer_role)}")


# ======================
# ハンドをデッキに戻し、もう一度
# ======================
