import random


blackjackTable = [2,3,4,5,6,7,8,9,10,"A","K","Q","J"]
hitTable = [2,3,4,4,5,5,"A"]
cardConversion = {"A":1, "K":10, "Q":10, "J":10}
class BlackjackGame():
    win = False
    finished = False
    bust =False
    credits = 0

    userHand = 0
    dealerHand = 0
    userHits = 1
    userCards = []
    dealerCards = []
    def __init__(self, credits) -> None:
        self.credits = credits
        self.win = False
        self.finished = False
        self.bust = False
        self.userCards = []
        self.dealerCards = []
        self.userHand = 0
        self.dealerHand = 0
        self.userHits = 1
        self.userCards.append(random.choice(blackjackTable))
        self.userCards.append(random.choice(blackjackTable))
        
        self.dealerCards.append(random.choice(blackjackTable))


        print(self.dealerCards, self.userCards)
        for card in self.userCards:
            if isinstance(card,int):
                self.userHand += card
            else:
                self.userHand += cardConversion[card]
        
        for card in self.dealerCards:
            if isinstance(card,int):
                self.dealerHand += card
            else:
                self.dealerHand += cardConversion[card]

        print(self.dealerCards, self.dealerHand, self.userCards, self.userHand)
        pass

    def NextFrame(self, hit):
        if self.finished:
            raise Exception("Game is finished")
        if hit:
            self.userHits += 1
            self.userCards.append(random.choice(hitTable))
            self.userHand = 0
            for card in self.userCards:
                if isinstance(card,int):
                    self.userHand += card
                else:
                    self.userHand += cardConversion[card]
            print(self.userCards)
            if self.userHand > 21:
                self.finished = True
                self.win = False
                self.bust = True
                return {
                    "GameStatus": "bust"
                }
            else:
                return {
                    "GameStatus": "notFinished"
                }
       
        else:
            for i in range(0,self.userHits):

                self.dealerCards.append(random.choice(hitTable))

            self.dealerHand = 0
            for card in self.dealerCards:
                if isinstance(card,int):
                    self.dealerHand += card
                else:
                    self.dealerHand += cardConversion[card]

            if self.dealerHand > 21:
                self.finished = True
                self.win =True
                self.bust = True
                return {
                    "GameStatus": "dealerBust"
                }
            elif self.userHand > self.dealerHand:
                self.finished = True
                self.win = True
                self.bust = False
                return {
                    "GameStatus": "win"
                }
            else:
                self.finished = True
                self.win = False
                self.bust = False
                return {
                    "GameStatus": "lost"
                }
            
