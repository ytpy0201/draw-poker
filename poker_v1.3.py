import random
from collections import Counter

#グローバルな定数、PEP8基準
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
HAND_ODDS = {
    "ロイヤルストレートフラッシュ": 100,
    "ストレートフラッシュ": 50,
    "フォーカード": 25,
    "フルハウス": 8,
    "フラッシュ": 5,
    "ストレート": 4,
    "スリーカード": 3,
    "ツーペア": 2,
    "ワンペア": 1,
    "役なし": 0
}

def judge_hand(hand):
    numbers = sorted(change_num(hand), reverse=True)
    counts = Counter(numbers)
    
    # 1. まず重複度順に「5枚すべて」を並べ替えたリストを作る（ワンペア、ツーペア、三連、フルハ、フォー用）
    # 例: [14, 14, 10, 10, 5] -> [(14, 2), (10, 2), (5, 1)] -> [14, 14, 10, 10, 5]
    # 例: [14, 14, 14, 5, 2] -> [(14, 3), (5, 1), (2, 1)] -> [14, 14, 14, 5, 2]
    sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    compare_list = []
    for num, count in sorted_counts:
        compare_list.extend([num] * count)
    
    count_pattern = sorted(counts.values())

    is_royal = royal(hand)
    is_flush = flush(hand)
    is_straight = straight(hand)

    # 2. 5枚の数字がバラバラな役（ストレート、フラッシュ、役なしなど）は、
    # 「一番強いカードの数字1枚」だけを比較用にすれば絶対にバグらない
    if is_straight:
        if numbers == [14, 5, 4, 3, 2]:
            compare_list = [5]  # A-5のストレートは「5」が最上位カード
        else:
            compare_list = [max(numbers)]  # 通常のストレートは最大値
    elif is_flush or count_pattern == [1, 1, 1, 1, 1]:  # フラッシュ、または役なし
        compare_list = numbers  # 強い順に1枚ずつ比較

    # 役の判定とリターン
    if is_royal:
        return HAND_RANK["ロイヤルストレートフラッシュ"], [14]
    elif is_flush and is_straight:
        return HAND_RANK["ストレートフラッシュ"], compare_list
    elif count_pattern == [1, 4]:
        return HAND_RANK["フォーカード"], compare_list
    elif count_pattern == [2, 3]:
        return HAND_RANK["フルハウス"], compare_list
    elif is_flush:
        return HAND_RANK["フラッシュ"], compare_list
    elif is_straight:
        return HAND_RANK["ストレート"], compare_list
    elif count_pattern == [1, 1, 3]:
        return HAND_RANK["スリーカード"], compare_list
    elif count_pattern == [1, 2, 2]:
        return HAND_RANK["ツーペア"], compare_list
    elif count_pattern == [1, 1, 1, 2]:
        return HAND_RANK["ワンペア"], compare_list
    else:
        return HAND_RANK["役なし"], compare_list


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
    """数字に変換
    
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


def exchange_cards(hand, deck):
    print("\nあなたのハンド:")

    for i, card in enumerate(hand, start=1):
            print(f"{i}: {card}")


    while True:

        choice = input("\n交換したいカードの番号をスペース区切りで入力 \nなければEnter：")

        if choice == "":
            return hand
        
        #文字列を分割してリスト化
        indexes = choice.split()
        
        #有効
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

    #昇順にして削除
    for index in sorted(indexes, reverse=True):
        del hand[int(index) - 1]

    while len(hand) < 5:

        hand.append(deck.pop())

    return hand


def compare_hands(player_result, dealer_result):
    if player_result > dealer_result:
        return "勝ち"
    elif player_result < dealer_result:
        return "負け"
    else:
        return "引き分け"


def make_deck():
    deck = []
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "J", "Q", "K"]

    for suit in suits:
        for rank in ranks:
            deck.append(f"{suit}{rank}")
    return deck


def deal_cards(deck, hand_list):
    #捨て変数
    for _ in range(5):
        hand_list.append(deck.pop())


def play_game(player_chips):
    print(f"\n=====================================")
    print(f"現在の持ちチップ: {player_chips} 枚")
    print(f"=====================================")

    # 1. ベット額の入力
    while True:
        bet_input = input(f"ベットする枚数を入力してください (1 ～ {player_chips}): ")
        if not bet_input.isdigit():
            print("数字を入力してください。")
            continue
        bet = int(bet_input)
        if not 1 <= bet <= player_chips:
            print(f"1 から {player_chips} の範囲で入力してください。")
            continue
        break

    # ベット分を先に引く
    player_chips -= bet

    # カードの配布と交換（既存の処理）
    deck = make_deck()
    random.shuffle(deck)
    player_hand = []
    dealer_hand = []
    deal_cards(deck, player_hand)
    deal_cards(deck, dealer_hand)

    player_hand = exchange_cards(player_hand, deck)

    print(f"\nあなたの手札：\n{player_hand}")
    print(f"ディーラー：\n{dealer_hand}")

    player_result = judge_hand(player_hand)
    dealer_result = judge_hand(dealer_hand)

    player_role_name = [k for k, v in HAND_RANK.items() if v == player_result[0]][0]
    dealer_role_name = [k for k, v in HAND_RANK.items() if v == dealer_result[0]][0]

    print(f"\nプレイヤー：{player_role_name}")
    print(f"ディーラー：{dealer_role_name}")

    # 2. 勝敗判定とチップの計算
    result = compare_hands(player_result, dealer_result)
    print(f"\n判定：{result}")

    if result == "勝ち":
        odds = HAND_ODDS[player_role_name]
        winnings = bet * odds
        # 勝った場合は、賭け金（bet）の払い戻し ＋ 役に応じたボーナス
        # ※配当が1倍（ワンペア）なら、賭けた分がそのまま戻ってくるイメージです
        player_chips += bet + winnings
        print(f"【勝利！】役の倍率: {odds}倍 / {winnings} 枚のボーナスチップを獲得！")
    elif result == "引き分け":
        player_chips += bet
        print("【引き分け】ベットしたチップが戻ります。")
    else:
        print(f"【敗北…】ベットした {bet} 枚のチップが没収されました。")

    return player_chips


#繰り返す
if __name__ == "__main__":
    # 初期チップを設定
    chips = 100

    while True:
        # ゲームを実行し、終わったら新しいチップ残高を受け取る
        chips = play_game(chips)

        # チップがなくなったら終了
        if chips <= 0:
            print("\nチップがなくなりました！ゲームオーバーです。")
            break

        answer = input("\nもう一回？ (y/n)：")
        if answer.lower() != "y":
            print(f"\n最終持ちチップ: {chips} 枚")
            print("Thank you for playing.")
            break
