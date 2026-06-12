"""
=====================================================
関数で一つずつ役の判定を作ろうとしたが、まとめたほうが楽だった

countをやめ、counterで視認性をあげた
キーとして要素を指定するとその個数を取得できる。
要素として存在しない値を指定すると0を返す。

most_common()メソッド
(要素, 出現回数)という形のタプルを出現回数順に並べたリストを返す。
=====================================================
"""
#def pair(): rank = rank_in_hand(hand) 
#pair_count = 0 
#for r in set(rank): 
#   if rank.count(r) == 2: 
#       pair_count += 1 
#
#       if pair_count == 1: 
#           print("ワンペア") 
#       elif pair_count == 2:
#           print("ツーペア") 
#       else: 
#           return None 
#
#
#def threecard(): 
#   rank = rank_in_hand(hand)
#   pair_rank = 0
#   if pair_rank == 3:

"""
=====================================================
リスト内包表記に書き換え
=====================================================
"""
#def rank_in_hand(hand):
#    ranks = []
#
#    for card in hand:
#        ranks.append(card[1:])#1:は10以降は二桁になるため
#
#    return ranks
#
#
#def suit_in_hand(hand):
#    suits = []
#    
#    for card in hand:
#        suits.append(card[0])
#
#    return suits
