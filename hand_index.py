import pydealer
from build_hand import list_from_stack, build_match_low, low_ranks


class hand_info:
    def __init__(self,hand_stack):
        self.hand_stack = hand_stack
        self.card = hand_stack[0].value
        self.value_list = list_from_stack(self.hand_stack)
        self.pip_list = list(x.value.replace("10","T")[0] for x in hand_stack)
        self.suit_list = list(x.suit[0] for x in hand_stack)
        self.low_list = build_match_low(self.value_list)
        
    def build_index(self):
        if len(list(set(self.suit_list))) == 1:
            i_suit_list = ['x','x','x','x']
        elif len(list(set(self.suit_list))) == 2:
            if self.suit_list.count(self.suit_list[0]) == 1: i_suit_list = ['x','y','y','y']
            elif self.suit_list.count(self.suit_list[0]) == 2: 
                if self.suit_list[0] == self.suit_list[1]: i_suit_list = ['x','x','y','y']
                elif self.suit_list[0] == self.suit_list[2]: i_suit_list = ['x','y','x','y']
                elif self.suit_list[0] == self.suit_list[3]: i_suit_list = ['x','y','y','x']
            elif self.suit_list.count(self.suit_list[0]) == 3:
                if self.suit_list[0] != self.suit_list[1]: i_suit_list = ['x','y','x','x']
                elif self.suit_list[0] != self.suit_list[2]: i_suit_list = ['x','x','y','y']
                elif self.suit_list[0] != self.suit_list[3]: i_suit_list = ['x','x','x','y']
            else:
                print('We have a problem here')
                i_suit_list = ['1','1','2','2']
                
        elif len(list(set(self.suit_list))) == 3:
            if self.suit_list[0] == self.suit_list[1]: 
                i_suit_list = ['x','x','y','z']
            elif self.suit_list[0] == self.suit_list[2]: 
                i_suit_list = ['x','y','x','z']
            elif self.suit_list[0] == self.suit_list[3]: 
                i_suit_list = ['x','y','z','x']
            elif self.suit_list[1] == self.suit_list[2]: 
                i_suit_list = ['x','y','y','z']
            elif self.suit_list[2] == self.suit_list[3]: 
                i_suit_list = ['x','y','z','z']
            elif self.suit_list[1] == self.suit_list[3]: 
                i_suit_list = ['x','y','z','y']
            else: 
                print('We have a problem here')
                i_suit_list = ['1','1','1','2']
        elif len(list(set(self.suit_list))) == 4:
            i_suit_list = ['x','y','z','a']
        else: print('We have a problem here')
        return(i_suit_list)
        
        
        
#deck = pydealer.Deck()
#hand = pydealer.Stack()
#deck.shuffle()
#
#hand = deck.deal(4)
#hand.sort(ranks=low_ranks)
#
#sean = hand_info(hand)
#
#print(sean.hand_stack)
#print(sean.value_list)
#print(sean.low_list)
#
#print(sean.card)
#print(sean.pip_list)
#print(sean.suit_list)
#
#sean.build_index()


    

