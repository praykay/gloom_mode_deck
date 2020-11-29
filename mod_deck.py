import random
import argparse

class ModDeck():
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.load_deck()
        self.discard = []
        self.bless_count = 0
        self.curse_count = 0
        

    def load_deck(self, action=None):
        with open('decks/'+ self.deck_name +'.txt') as f:
            deck = [s.rstrip('\n') for s in f.readlines()]
            random.shuffle(deck)
        self.deck = deck
        return True


    def shuffle(self, action=None):
        filtered = [card for card in self.discard if card != 'bless' and card != 'curse']
        self.deck = filtered + self.deck
        random.shuffle(self.deck)
        self.discard = []
        return True
    
    def get_next_card(self, action=None):
        card = self.deck.pop()
        if len(self.deck) == 0:
            self.load_deck()
        print(card)
        if card == 'bless':
            self.bless_count -= 1
        if card == 'curse':
            self.curse_count -= 1
        self.discard.append(card)
        return True

    def add_card(self, action):
        with open('decks/'+self.deck_name+'.txt', 'a') as f:
            f.write('\n')
            f.write(action[1])
        self.load_deck()
        return True

    def add_blurse(self, action):
        index = random.randint(0, len(self.deck))
        front = self.deck[0:index]
        back = self.deck[index:len(self.deck)]
        front.append(action[1])
        if action[1] == 'bless':
            self.bless_count += 1
        if action[1] == 'curse':
            self.curse_count +=1
        self.deck = front + back
        return True


    def remove_card(self, action):
        self.load_deck()
        if action[1] in self.deck:
            self.deck.remove(action[1])
            self.deck = [d+'\n' for d in self.deck if d.strip()]
            with open('decks/'+self.deck_name+'.txt', 'w') as f:
                f.writelines(self.deck)
            self.load_deck()
        else:
            print(action[1], 'is not in the deck')
            return 0
        return 1

    def replace_card(self, action):
        if len(action) !=3:
            print('Could not parse replace. Expecting command to be in format of replace card_to_remove card_to_add')
        else:
           val = self.remove_card(['', action[1]])
           if val == 1:
               self.add_card(['', action[2]])
           else:
               print('Replaced failed. Please try again')
        return True 

    def print_deck(self, action=None):
        print(self.deck)
        return True

    def exit_character(self, action):
        return False

    def game(self):
        still_chars_turn = True
        while still_chars_turn:
            action = input("Enter action ").lower().split(" ")
            still_chars_turn = self.parse_action(action)
    
    def parse_action(self, action):
        actions = {'roll': self.get_next_card,
                    'r': self.get_next_card,
                    'next': self.get_next_card,
                    'add': self.add_card,
                    'blurse': self.add_blurse,
                    'load': self.load_deck,
                    'shuffle': self.shuffle,
                    'remove': self.remove_card,
                    'print': self.print_deck,
                    'exit': self.exit_character,
                    'e': self.exit_character,
                    'quit': self.exit_character,
                    'q': self.exit_character,
                    'replace': self.replace_card
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
            elif char == 'blurse':
                bless = 0
                curse = 0
                for c in chars.keys():
                    bless += chars[c].bless_count
                    curse += chars[c].curse_count
                    print(c, 'Blesses',chars[c].bless_count, 'Curses',chars[c].curse_count)
                print('Total Blesses:', bless, 'Curses:', curse)

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