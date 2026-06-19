import random
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# グローバルな定数、PEP8基準
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
    
    # 1. まず重複度順に「5枚すべて」を並べ替えたリストを作る
    sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    compare_list = []
    for num, count in sorted_counts:
        compare_list.extend([num] * count)
    
    count_pattern = sorted(counts.values())

    is_royal = royal(hand)
    is_flush = flush(hand)
    is_straight = straight(hand)

    # 2. 5枚の数字がバラバラな役は、「一番強いカードの数字1枚」だけを比較用にすれば絶対にバグらない
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
    
    # Aを14としているのでA-5は例外として扱う
    if numbers == [2, 3, 4, 5, 14]:
        return True
    
    for i in range(4):
        if numbers[i + 1] - numbers[i] != 1:
            return False
    return True


def change_num(hand):
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
    console.print(Panel("[yellow]あなたのハンド[/yellow]", expand=False))
    
    for i, card in enumerate(hand, start=1):
        suit = card[0]
        rank = card[1:]
        color = "red" if suit in ["♥", "♦"] else "white"
        console.print(f"{i}: [{color}]{card}[/{color}]")

    while True:
        choice = input("\n交換したいカードの番号をスペース区切りで入力 \nなければEnter：")
        if choice == "":
            return hand
        
        indexes = choice.split()
        valid = True
        for index in indexes:
            if not index.isdigit() or not 1 <= int(index) <= 5:
                valid = False

        if len(indexes) != len(set(indexes)):
            console.print("[bold red]同じ番号は入力できません[/bold red]")
            continue        

        if not valid:
            console.print("[bold red]１～５の数字を入力してください。[/bold red]")
            continue
        break

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
    for _ in range(5):
        hand_list.append(deck.pop())


def print_rich_hand(title, hand):
    """手札をリッチなカード形式で横並びに表示する"""
    table = Table(title=title, show_header=False, border_style="bright_blue", box=None)
    
    for _ in range(len(hand)):
        table.add_column(justify="center", width=6)
        
    row_cells = []
    for card in hand:
        suit = card[0]
        rank = card[1:]
        
        if suit in ["♥", "♦"]:
            color = "red"
        else:
            color = "bright_white"  # Windowsや主要環境で安定するカラー名に変更
            
        # エラー箇所: 'gray' から標準で確実に通る 'bright_black' (暗い灰) もしくは 'blue' 等に変更。ここでは 'white' に設定
        card_panel = Panel(f"[{color}]{suit}\n{rank}[/{color}]", border_style="white")
        row_cells.append(card_panel)
        
    table.add_row(*row_cells)
    console.print(table)


def play_game(player_chips):
    console.print(Panel(f"[bold yellow]現在の持ちチップ: {player_chips} 枚[/bold yellow]", border_style="yellow", expand=False))

    while True:
        bet_input = input(f"ベットする枚数を入力してください (1 ～ {player_chips}): ")
        if not bet_input.isdigit():
            console.print("[red]数字を入力してください。[/red]")
            continue
        bet = int(bet_input)
        if not 1 <= bet <= player_chips:
            console.print(f"[red]1 から {player_chips} の範囲で入力してください。[/red]")
            continue
        break

    player_chips -= bet

    deck = make_deck()
    random.shuffle(deck)
    player_hand = []
    dealer_hand = []
    deal_cards(deck, player_hand)
    deal_cards(deck, dealer_hand)

    # カード交換前の手札を表示
    print_rich_hand("[cyan]◆ 交換前の手札 ◆[/cyan]", player_hand)
    player_hand = exchange_cards(player_hand, deck)

    # 最終手札を綺麗に並べて表示
    print_rich_hand("[green]★ あなたの最終手札 ★[/green]", player_hand)
    print_rich_hand("[magenta]♠ ディーラーの手札 ♠[/magenta]", dealer_hand)

    player_result = judge_hand(player_hand)
    dealer_result = judge_hand(dealer_hand)

    player_role_name = [k for k, v in HAND_RANK.items() if v == player_result[0]][0]
    dealer_role_name = [k for k, v in HAND_RANK.items() if v == dealer_result[0]][0]

    console.print(f"\nプレイヤーの役：[bold green]{player_role_name}[/bold green]")
    console.print(f"ディーラーの役：[bold magenta]{dealer_role_name}[/bold magenta]")

    result = compare_hands(player_result, dealer_result)
    
    if result == "勝ち":
        odds = HAND_ODDS[player_role_name]
        winnings = bet * odds
        player_chips += bet + winnings
        console.print(Panel(f"[bold gold1] 判定：{result} !! [/bold gold1]\n役の倍率: {odds}倍 / {winnings} 枚のボーナスを獲得！", border_style="gold1"))
    elif result == "引き分け":
        player_chips += bet
        console.print(Panel(f"[bold white] 判定：{result} [/bold white]\nベットしたチップが戻ります。", border_style="white"))
    else:
        console.print(Panel(f"[bold red] 判定：{result} ... [/bold red]\nベットした {bet} 枚のチップが没収されました。", border_style="red"))

    return player_chips


if __name__ == "__main__":
    chips = 100

    while True:
        chips = play_game(chips)

        if chips <= 0:
            console.print("\n[bold red]チップがなくなりました！ゲームオーバーです。[/bold red]")
            break

        answer = input("\nもう一回？ (y/n)：")
        if answer.lower() != "y":
            console.print(f"\n最終持ちチップ: [bold yellow]{chips}[/bold yellow] 枚")
            console.print("Thank you for playing.")
            break