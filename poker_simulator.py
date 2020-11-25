"""
Poker Simulator and Probability Calculator
By: Shrey Ghai 
Collaborators: Payas Parab
In this project, We have created a poker simulator.
"""

import random
from copy import deepcopy

class Card: 
    def __init__(self, suit, card_type):
        """
        Creates a new card based on the suit and the number of the card.
        Example - Card("hearts", 3) would create a Card that represents the three of hearts.
        Input (suit): hearts, diamonds, spades, clubs
        Input (type): Integer between 2 and 14 (see note below). 
        Jack = 11, Queen = 12, King = 13, Ace = 14  
        """
        if suit not in ["\x1b[31m♥\x1b[0m", "\x1b[31m♦\x1b[0m", "♠", "♣"]:
            raise TypeError("You have input in an invalid suit")

        if (card_type > 14) or (card_type < 1):
            raise TypeError("You have input in an invalid card_type")

        self.suit = suit
        self.card_type = card_type
            
    def __repr__(self):
        if self.suit not in["\x1b[31m♥\x1b[0m", "\x1b[31m♦\x1b[0m"]:    
            if (self.card_type == 11):
                return "J" + self.suit

            if (self.card_type == 12):
                return "Q" + self.suit

            if (self.card_type == 13):
                return "K" + self.suit

            if (self.card_type == 14):
                return "A" + self.suit

            else:
                return str(self.card_type) + self.suit 
        else:
            if (self.card_type == 11):
                return "\x1b[31mJ\x1b[0m" + self.suit

            if (self.card_type == 12):
                return "\x1b[31mQ\x1b[0m" + self.suit

            if (self.card_type == 13):
                return "\x1b[31mK\x1b[0m" + self.suit

            if (self.card_type == 14):
                return "\x1b[31mA\x1b[0m" + self.suit

            else:
                return ("\x1b[31m"  + str(self.card_type) + "\x1b[0m") + self.suit 

def create_deck(): 
    """
    Description: Makes a standard deck of 52 playing cards
    Outputs: A list that represents a standard deck of 52 playing cards represented by the Card class
    """    
    deck = []
    
    for card_type in range(2,15):
        for suit in ["\x1b[31m♥\x1b[0m", "\x1b[31m♦\x1b[0m", "♠", "♣"]:
            current_card = Card(suit, card_type)    
            deck.append(current_card)
    return deck
        
def shuffle_deck(deck): 
    #https://pynative.com/python-random-shuffle/
    return random.sample(deck, len(deck))


class Deck:
    def __init__(self):
        self.deck = shuffle_deck(create_deck())

    def get_a_card(self):
        #Return card
        #Remove a card from self.deck and return
        card = self.deck[0]
        self.deck.remove(card)
        return card

    def reset_deck(self):
        self.deck = shuffle_deck(create_deck())

class Table:
    def __init__(self):
        self.table_cards = []        

    def flop(self, deck, print_bool = True):
        for i in range(0,3):    
            self.table_cards.append(deck.get_a_card())
        if (print_bool == True):
            print(self.table_cards)
         
    def turn(self, deck, print_bool = True):
        self.table_cards.append(deck.get_a_card())
        if (print_bool == True):
            print(self.table_cards)
         
    def river(self, deck, print_bool = True):
        self.table_cards.append(deck.get_a_card())
        if (print_bool == True):
            print(self.table_cards)
         
    def reset_table(self):
        self.table_cards = []
        
class Player:
    def __init__(self, name):
        self.player = name
        self.player_cards = []

    def __repr__(self):
        return self.player

    def deal_player(self, deck):
        for i in range(0,2):
            self.player_cards.append(deck.get_a_card())
        print(self.player + ":" + str(self.player_cards))

    def reset_player(self):
        self.player_cards = []

class Game: 
    def __init__(self, players):
        self.deck = Deck()
        self.table = Table()
        self.players = {}
        self.cards_dealt = False
        for i in range(0, len(players)):
            player = Player(players[i])
            self.players[players[i]] = player

    def deal(self):
        for player_name in self.players.keys():
            self.players[player_name].deal_player(self.deck)
        self.cards_dealt = True

    def flop(self, print_bool = True):
        self.table.flop(self.deck, print_bool)

    def turn(self, print_bool = True):
        self.table.turn(self.deck, print_bool)

    def river(self, print_bool = True):
        self.table.river(self.deck, print_bool)

    def reset(self):
        self.deck.reset_deck()
        self.table.reset_table()
        for i in self.players.keys():
            self.players[i].reset_player()


def current_winner(game, return_bool = False):

    total_cards = {}
    for player_name in game.players.keys():
        total_cards[player_name] = game.players[player_name].player_cards + game.table.table_cards

    rankings = {}
    ranking_vals = {}
    residuals = {}
    for player_name in total_cards.keys():
        rankings[player_name] = get_ranking(total_cards[player_name])
    for player_name in total_cards.keys():
        ranking_vals[player_name] = get_ranking_vals(rankings[player_name], total_cards[player_name])
    for player_name in total_cards.keys():
        residuals[player_name] = get_residuals(rankings[player_name], ranking_vals[player_name], total_cards[player_name])

    winner = []
    highest_ranking = max(rankings.values())
    top_ranking_players = []
    for player_name in rankings.keys():
        if (rankings[player_name] == highest_ranking):
            top_ranking_players.append(player_name)

    if len(top_ranking_players) > 1:
        best_player = top_ranking_players[0]
        ranking_val_winners = [best_player]
        best_ranking_vals = ranking_vals[best_player]
        for player_name in top_ranking_players[1:]:
            _curr_ranking_vals = ranking_vals[player_name]
            if _curr_ranking_vals == best_ranking_vals:
                ranking_val_winners.append(player_name)
            for i in range(len(best_ranking_vals)):
                if best_ranking_vals[i] < _curr_ranking_vals[i]:
                    best_player = player_name
                    best_ranking_vals = _curr_ranking_vals
                    ranking_val_winners = [best_player]
                    break
        if len(ranking_val_winners) > 1:
            best_residual_player = ranking_val_winners[0]
            residual_val_winners = [best_residual_player]
            best_residual_vals = residuals[best_residual_player]
            if len(best_residual_vals) == 0:
                winner = ranking_val_winners
            for player_name in ranking_val_winners[1:]:
                _curr_residual_vals = residuals[player_name]
                if(_curr_residual_vals == best_residual_vals):
                    residual_val_winners.append(player_name)
                for i in range(len(best_residual_vals)):
                    if best_residual_vals[i] < _curr_residual_vals[i]:
                        best_residual_player = player_name
                        best_residual_vals = _curr_residual_vals
                        residual_val_winners = [best_residual_player]
                        break
            winner = residual_val_winners
        else:
            winner = ranking_val_winners 
    else:
        winner = top_ranking_players

    if(return_bool == True):
        return winner

    if (len(winner) == 1):
        print('{} is the current winner'.format(winner[0]))
        determine_hand(winner[0], game)
    else:
        print('{} are tied'.format(" and ".join(winner))) 
        for i in winner:    
            determine_hand(i, game)


def hand_output(hand_list, player_name):
    ranking = hand_list[0]
    ranking_vals = hand_list[1]
    residuals = hand_list[2]

    def convert_int_to_name(ranking_val_int):
        if (ranking_val_int == 2):
            return "Two"
        if (ranking_val_int == 3):
            return "Three"
        if (ranking_val_int == 4):
            return "Four"
        if (ranking_val_int == 5):
            return "Five"
        if (ranking_val_int == 6):
            return "Six"
        if (ranking_val_int == 7):
            return "Seven"
        if (ranking_val_int == 8):
            return "Eight"
        if (ranking_val_int == 9):
            return "Nine"
        if (ranking_val_int == 10):
            return "Ten"
        if (ranking_val_int == 11):
            return "Jack" 
        if (ranking_val_int == 12):
            return "Queen" 
        if (ranking_val_int == 13):
            return "King"
        if (ranking_val_int == 14):
            return "Ace"

    #TODO Account for current winner pre-flop (empty residuals)
    if (ranking == 10):
        print('{} has a Royal Flush!'.format(player_name))
    if (ranking == 9):
        print('{} has a {} high Straight Flush.'.format(player_name, convert_int_to_name(ranking_vals[0])))
    if (ranking == 8):
        print('{} has a Four of a Kind of {}s with {} high'.format(player_name, convert_int_to_name(ranking_vals[0]), convert_int_to_name(residuals[0])))
    if (ranking == 7):
        print('{} has a Full House with {}s full of {}s'.format(player_name, convert_int_to_name(ranking_vals[0]), convert_int_to_name(ranking_vals[1])))
    if (ranking == 6):
        print('{} has a {} high Flush'.format(player_name, convert_int_to_name(ranking_vals[0])))
    if (ranking == 5):
        print('{} has a {} high Straight'.format(player_name, convert_int_to_name(ranking_vals[0])))
    if (ranking == 4):
        print('{} has a Three of a Kind of {}s with {} high'.format(player_name, convert_int_to_name(ranking_vals[0]), convert_int_to_name(residuals[0])))
    if (ranking == 3):
        print('{} has a Two Pair with a pair of {}s and pair of {}s with {} high'.format(player_name, convert_int_to_name(ranking_vals[0]), convert_int_to_name(ranking_vals[1]), convert_int_to_name(residuals[0])))
    if (ranking == 2):
        print('{} has a Pair of {}s with {} high'.format(player_name, convert_int_to_name(ranking_vals[0]), convert_int_to_name(residuals[0])))
    if (ranking == 1):
        print('{} has {} high'.format(player_name, convert_int_to_name(ranking_vals[0])))



def determine_hand(player_name, game):
    """
    Inputs: 
        - player_name string
    
    Outputs =
        - Ranking (1-10, 10 being royal flush, 1 being high card)
        - Constituents of the ranking (for example number of the pair/high of the straight)
        - Residual cards - leftovers for breaking a tie
    Steps
    1. Get the table cards
    2. Get the player cards
    3. Rank current
    4. Get constituents of ranking
    5. Get the residual cards 
    """
    table_cards = game.table.table_cards 
    player_cards = game.players[player_name].player_cards
    total_cards = player_cards + table_cards
    
    ranking = get_ranking(total_cards)
    ranking_vals = get_ranking_vals(ranking, total_cards)
    residuals = get_residuals(ranking, ranking_vals, total_cards)

    return hand_output([ranking, ranking_vals, residuals], player_name)
    

def get_ranking(total_cards):
    '''
    Returns an integer for the ranking of the hand
    '''
    card_counts = find_card_counts(total_cards)
    if (straight(total_cards) and flush(total_cards) and ace(total_cards)):
        return 10 #royal flush
    if (straight(total_cards) and flush(total_cards)):
        return 9 #straight flush
    if (four_of_a_kind(card_counts)):
        return 8
    if (full_house(card_counts)):
        return 7
    if (flush(total_cards)):
        return 6 #flush
    if (straight(total_cards)):
        return 5 #straight
    if (three_of_a_kind(card_counts)):
        return 4
    if (two_pair(card_counts)):
        return 3 
    if (pair(card_counts)):
        return 2
    else:
        return 1 

def get_ranking_vals(ranking, total_cards):
    card_counts = find_card_counts(total_cards)
    
    if ranking == 9: #Returns high of number cards
        number_cards = []
        for card in total_cards: 
            number_cards.append(card.card_type)
        number_cards.sort()
        streak = 0
        for i in range(1, len(number_cards)):
            if (number_cards[i] == number_cards[i-1] + 1):
                streak += 1
            else:
                if streak >= 4:
                    return number_cards[i-1]
        return [number_cards[len(number_cards) - 1]]

    if ranking == 8: #Return 4 of a kind card
        for i in card_counts:
            if (card_counts[i] == 4):
                return [i]
    
    if ranking == 7: #Returns list with items [3 of kind, pair]
        full_house = []
        for i in card_counts:
            if(card_counts[i] == 3):
                full_house.append(i)
        for i in card_counts:
            if(card_counts[i] == 2):
                full_house.append(i)
        return full_house

    if ranking == 6: #Returns 5 flush cards in order 
        suits = {}
        suits['spade'] = 0
        suits['club'] = 0
        suits['heart'] = 0
        suits['diamond'] = 0
        
        # Count cards per suit
        for card in total_cards:
            if card.suit == "\x1b[31m♥\x1b[0m":
                suits['heart'] += 1
            if card.suit == "\x1b[31m♦\x1b[0m":
                suits['diamond'] += 1
            if card.suit == "♠":
                suits['spade'] += 1
            if card.suit == "♣":
                suits['club'] += 1
        for i in suits:
            if (suits[i] >= 5):
                flush_suit = i

        # Convert flush suit string to symbol
        flush_suit_search = None
        if flush_suit == 'heart':
            flush_suit_search = "\x1b[31m♥\x1b[0m"
        if flush_suit == 'diamond':
            flush_suit_search = "\x1b[31m♦\x1b[0m"
        if flush_suit == 'club':
            flush_suit_search = "♣"
        if flush_suit == 'spade':
            flush_suit_search = "♠"

        flush_suit_card_types = []
        
        for card in total_cards:
            if (flush_suit_search == card.suit):
                flush_suit_card_types.append(card.card_type)

        flush_suit_card_types.sort(reverse = True)

        return flush_suit_card_types[0:5] 
        
    if ranking == 5: #Returns highest card in straight
        number_cards = []
        for card in total_cards: 
            number_cards.append(card.card_type)
        number_cards.sort()
        streak = 0
        for i in range(1, len(number_cards)):
            if (number_cards[i] == number_cards[i-1] + 1):
                streak += 1
            else:
                if streak >= 4:
                    return [number_cards[i-1]]
        return [number_cards[len(number_cards) - 1]]

    if ranking == 4: #Returns three of a kind card
        for i in card_counts:
            if(card_counts[i] == 3):
                return [i]

    if ranking == 3: #Returns two highest pairs in list
        pairs = []
        for i in card_counts:
            if(card_counts[i] == 2):
                pairs.append(i)
        pairs.sort(reverse = True)
        return pairs[0:2]

    if ranking == 2: #Returns pair type
        for i in card_counts:
            if(card_counts[i] == 2):
                return [i]

    else:
        return [max(card_counts.keys())] #Returns highest card


def get_residuals(ranking, ranking_vals, total_cards):
    number_cards = []
    for card in total_cards: 
        number_cards.append(card.card_type)
    number_cards.sort(reverse = True)

    if ranking == 8: 
        number_cards = [i for i in number_cards if i not in ranking_vals]
        return [number_cards[0]]
    if ranking == 4: 
        number_cards = [i for i in number_cards if i not in ranking_vals]
        return number_cards[0:2]
    if ranking == 3: 
        number_cards = [i for i in number_cards if i not in ranking_vals]
        return [number_cards[0]]
    if ranking == 2: 
        number_cards = [i for i in number_cards if i not in ranking_vals]
        return number_cards[0:3]
    if ranking == 1: 
        number_cards = [i for i in number_cards if i not in ranking_vals]
        return number_cards[0:4]
    else:
        return [] #Empty list when no residuals for current hand

def flush(total_cards):
    spade = 0
    club = 0
    heart = 0
    diamond = 0
    flush = False
    for card in total_cards:
        if card.suit == "\x1b[31m♥\x1b[0m":
            heart += 1
        if card.suit == "\x1b[31m♦\x1b[0m":
            diamond += 1
        if card.suit == "♠":
            spade += 1
        if card.suit == "♣":
            club += 1
    if (heart >= 5 or diamond >= 5 or spade >= 5 or club >= 5):
        flush = True 
    return flush

def straight(total_cards):
    number_cards = []
    for card in total_cards: 
        number_cards.append(card.card_type)
    if 14 in number_cards:
        number_cards.append(1)
    number_cards.sort()
    current_streak = 0
    for i in range(1, len(number_cards)):
        if (number_cards[i] == number_cards[i-1]):
            current_streak = current_streak
        elif (number_cards[i] == number_cards[i-1] + 1):
            current_streak += 1
            if (current_streak >= 4): 
                return True
        else:
            current_streak = 0
    return False

def ace(total_cards):
    number_cards = []
    for card in total_cards: 
        number_cards.append(card.card_type)
    return (14 in number_cards)

def find_card_counts(total_cards):

    card_counts = {}
    for card in total_cards:
        if (card.card_type not in card_counts.keys()):
            card_counts[card.card_type] = 1
        else:
            card_counts[card.card_type] += 1
    return card_counts

def four_of_a_kind(card_counts):
    return (4 in card_counts.values())

def three_of_a_kind(card_counts):
    return (3 in card_counts.values())

def full_house(card_counts):
    return (pair(card_counts) and three_of_a_kind(card_counts))

def pair(card_counts):
    return pair_counts(card_counts) == 1

def two_pair(card_counts):
    return pair_counts(card_counts) == 2

def pair_counts(card_counts):
    '''
    Return 1 if 1 pair
    Return 2 if 2 or 3 pair
    '''
    pairs = 0
    for i in card_counts.values():
        if (i == 2):
            pairs += 1
    if (pairs == 1):
        return 1
    if (pairs == 2 or pairs == 3):
        return 2
                
def determine_probability(game, number_simulations, print_sim = False):
    if (game.cards_dealt == False):
        print("Please deal cards") 
        return

    if (len(game.table.table_cards) == 5):
        current_winner(game)
        return
    
    current_game = deepcopy(game)
    game_winners = {}
    for player in game.players:
        game_winners[player] = 0
    game_winners['split'] = 0

    if (len(game.table.table_cards) == 0):
        for i in range(0, number_simulations):
            current_game.flop(print_bool = False)
            current_game.turn(print_bool = False)
            if (print_sim == True):
	            print('Simulation {}'.format(i+1))
	            current_game.river(print_bool = True)
	            current_winner(current_game, return_bool = False)
	            print()
            winner = current_winner(current_game, return_bool = True)
            if(len(winner) == 1):
                game_winners[winner[0]] += 1
            else:
                game_winners['split'] += 1
            current_game = deepcopy(game)
            current_game.deck.deck = shuffle_deck(current_game.deck.deck)

    if (len(game.table.table_cards) == 3):
        for i in range(0, number_simulations):
            current_game.turn(print_bool = False)
            if (print_sim == True):
	            print('Simulation {}'.format(i+1))
	            current_game.river(print_bool = True)
	            current_winner(current_game, return_bool = False)
	            print()
            winner = current_winner(current_game, return_bool = True)
            if(len(winner) == 1):
                game_winners[winner[0]] += 1
            else:
                game_winners['split'] += 1
            current_game = deepcopy(game)
            current_game.deck.deck = shuffle_deck(current_game.deck.deck)

    if (len(game.table.table_cards) == 4):
        for i in range(0, number_simulations):
            if (print_sim == True):
	            print('Simulation {}'.format(i+1))
	            current_game.river(print_bool = True)
	            current_winner(current_game, return_bool = False)
	            print()
            winner = current_winner(current_game, return_bool = True)
            if(len(winner) == 1):
                game_winners[winner[0]] += 1
            else:
                game_winners['split'] += 1
            current_game = deepcopy(game)
            current_game.deck.deck = shuffle_deck(current_game.deck.deck)

    percentages = {k: '{}%'.format(round((v/number_simulations) * 100)) for k, v in game_winners.items()}
    return percentages
