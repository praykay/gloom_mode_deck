import random
import argparse

class ModDeck():
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.load_deck()

    def load_deck(self, action=None):
        with open('decks/'+ self.deck_name +'.txt') as f:
            deck = [s.rstrip('\n') for s in f.readlines()]
            random.shuffle(deck)
        self.deck = deck
    
    def get_next_card(self, action=None):
        card = self.deck.pop()
        if len(self.deck) == 0:
            self.load_deck()
        print(card)
        return card

    def add_card(self, action):
        with open('decks/'+self.deck_name+'.txt', 'a') as f:
            f.write('\n')
            f.write(action[1])
        self.load_deck()

    def remove_card(self, action):
        if action[1] in self.deck:
            self.load_deck()
            self.deck.remove(action[1])
            self.deck = [d+'\n' for d in self.deck]
            with open('decks/'+self.deck_name+'.txt', 'w') as f:
                f.writelines(self.deck)
            self.load_deck()
        else:
            print(action[1], 'is not in the deck')

    def print_deck(self, action=None):
        print(self.deck)
        

    def game(self):
        action = input("Enter action ").lower().split(" ")
        self.parse_action(action)
    
    def parse_action(self, action):
        actions = {'roll': self.get_next_card,
                    'r': self.get_next_card,
                    'next': self.get_next_card,
                    'add': self.add_card,
                    'load': self.load_deck,
                    'shuffle': self.load_deck,
                    'remove': self.remove_card,
                    'print': self.print_deck
                    }
        if action[0] in actions.keys():
            return actions[action[0]](action)
        else:
            print("You Idiot. Enter shit right")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck_names", "-d", nargs='+', help="Name of character's deck to load")
    parser.add_argument("--create", "-c", nargs='+', help="Enter name of new deck you wish to create. It will create a base mod deck and character mods can be added removed")
    args = parser.parse_args()
    if args.create != None:
        names = [n.lower() for n in args.create]
        for name in names:
            create_new_deck(name)
    if args.deck_names != None:
        d = args.deck_names
        print(d)
        decks = [ds.lower() for ds in d]
        chars = {d:ModDeck(d) for d in decks}
        while True:
            char = input('Select Character ')
            if char in chars.keys():
                deck = chars[char]
                deck.game()
            else:
                print('Did not find character name. Please Retry')

def create_new_deck(name):
    with open('decks/base.txt') as f:
        deck = [s.rstrip('\n') for s in f.readlines()]
        with open('decks/' + name + '.txt', 'w+') as g:
            for d in deck:
                g.write(d+'\n')
if __name__ == "__main__":
    parse_args()