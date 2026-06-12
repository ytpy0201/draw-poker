import random 


def rank_in_hand(hand): 
    rank = [] 
    for card in hand:
        rank.append(card[1:]) 
        return rank 

def pair(): 
    rank = rank_in_hand(hand) 
    pair_count = 0 
    for r in set(rank): 
        if rank.count(r) == 2: 
            pair_count += 1 
    if pair_count == 1: 
            print("ワンペア") 
    elif pair_count == 2: 
            print("ツーペア") 
    else: return None 
            

def threecard(): 
    rank = rank_in_hand(hand) 
    pair_rank = 0
    if pair_rank == 3: 

deck = [] 
suits = ["♠", "♥", "♦", "♣"] 
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
for suit in suits: 
    for rank in ranks: 
        deck.append(f"{suit}{rank}") 

random.shuffle(deck) 

hands = [[],[],[],[]] 
for _ in range(5): 
    for hand in hands: 
        hand.append(deck.pop()) 

for i, hand in enumerate(hands, start=1): 
    print(f"Player{i}: {hand}")