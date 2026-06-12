#def straight(hand):
#    hand = sorted(hand)
#    if hand[4] - hand[3] == 1:
#        if hand[3] - hand[2] == 1:
#            if hand[2] - hand[1] == 1:
#                if hand[1] - hand[0] == 1:
#                    print("これはストレートです。")
#
#hand = [14,13,12,11,10]
#
#straight(hand)


#def straight(hand):
#    hand = sorted(hand)
#
#    for i in range(4):
#        t_or_f =  hand[i+1] - hand[i] == 1
#        if t_or_f == False:
#            break


#def straight(hand):
#    hand = sorted(hand)
#
#    is_straight = True
#
#    for i in range(4):
#        if hand[i + 1] - hand[i] != 1:
#            is_straight = False
#            break
#
#    if is_straight:
#        print("ストレート")


def straight(hand):
    hand = change_num(hand)
    hand = sorted(hand)
    
    
    if hand == [2, 3, 4, 5, 14]:
        return "ストレート"
    
    for i in range(4):

        if hand[i + 1] - hand[i] != 1:
            return

    return "ストレート"


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
    

def rank_in_hand(hand):
    ranks = [card[1:] for card in hand]
    return ranks