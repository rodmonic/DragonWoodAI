import shortuuid
from collections import Counter
from itertools import chain
from neat.nn import FeedForwardNetwork

from Dragonwood.Card import Adventurer_Card, Dragonwood_Card
from Dragonwood.Deck import Adventurer_Deck


class Player():

    def __init__(self, risk_level: float, risk_adjustment: float, name: str, card_mask: list[str] = [], is_robot: bool = False, ):
        self.hand = []
        self.uuid = shortuuid.uuid()[:8]
        self.name = name
        self.risk_level = risk_level
        self.risk_adjustment = risk_adjustment
        self.points = 0
        self.dragonwood_cards = []
        self.strike_modifier = 0
        self.stomp_modifier = 0
        self.scream_modifier = 0
        self.card_mask = card_mask
        self.is_robot = is_robot
        self.fitness = 0


    def get_player_details(self) -> dict:

        return {
            "player_uuid": self.uuid,
            "name": self.name,
            "points": self.points,
            "risk_level": self.risk_level,
            "risk_adjustment": self.risk_adjustment,
            "scream_modifier": self.scream_modifier,
            "strike_modifier": self.strike_modifier,
            "stomp_modifier": self.stomp_modifier,
            }

    def find_attack_options(self) -> tuple[
                            list[list[Adventurer_Card]],
                            list[list[Adventurer_Card]],
                            list[list[Adventurer_Card]]
                            ]:

        attack_options = []

        # strike - finding straights
        attack_options.extend([("strike", x) for x in self.find_strikes()])
        # stomp - finding duplicate values
        attack_options.extend([("stomp", x) for x in self.find_stomps()])
        # scream - finding duplicate suits
        attack_options.extend([("scream", x) for x in self.find_screams()])

        return attack_options

    def find_strikes(self) -> list[list[Adventurer_Card]]:
        sorted_hand = sorted(self.hand, key=lambda card: (card.value))

        consecutive_pairs = zip(sorted_hand, sorted_hand[1:])
        adventurers = []
        # intialise temp list with first hand in sorted list
        adventurers_temp = [sorted_hand[0]]
        for current_card, next_card in consecutive_pairs:
            # skip card it it is the same vallue
            if current_card.value == next_card.value:
                continue

            # add next card if it is in straight
            if current_card.value + 1 == next_card.value:
                adventurers_temp.append(next_card)
            else:
                # reset temp list if no straight
                adventurers_temp = [next_card]

            # finally if temp list is bigger than actual list copy it over.
            if len(adventurers_temp) > len(adventurers):
                adventurers = adventurers_temp.copy()

        # finally return all smaller lists within choices list
        return [adventurers[0:x+1] for x in range(len(adventurers))]

    def find_stomps(self) -> list[list[Adventurer_Card]]:
        element_counts = Counter(x.value for x in self.hand)
        max_element, _ = max(element_counts.items(), key=lambda x: x[1])
        adventurers = [x for x in self.hand if x.value == max_element]

        # finally return all smaller lists within choices list
        return [adventurers[0:x+1] for x in range(len(adventurers))]

    def find_screams(self) -> list[list[Adventurer_Card]]:
        element_counts = Counter(x.suit for x in self.hand)
        max_element, _ = max(element_counts.items(), key=lambda x: x[0])
        adventurers = [x for x in self.hand if x.suit == max_element]

        # finally return all smaller lists within choices list
        return [adventurers[0:x+1] for x in range(len(adventurers))]

    def decide_by_rules(self, landscape: list[Dragonwood_Card], dice_ev: float, attack_options) -> dict:

        candidate_decisions = self.get_candidate_decisions(landscape, dice_ev, attack_options)

        if not candidate_decisions:
            return {"decision": "reload"}

        # Use key=lambda x: x[3] to get the element with the smallest positive difference
        selected_option = min(candidate_decisions, key=lambda x: x[3])

        return {
            "decision": selected_option[0],      # strike/stomp/scream
            "card": selected_option[1],          # the card  within the landscape
            "adventurers":  selected_option[2],  # the adventurers used
        }

    def get_candidate_decisions(self, landscape: list[Dragonwood_Card], dice_ev: float, attack_options) -> list[list[Adventurer_Card]]:

        candidate_decisions = []

        for card in landscape:

            # skip card if in card_mask
            if card.name in self.card_mask:
                continue

            for attack_option in attack_options:

                threshold = len(attack_option[1]) * (self.risk_level + dice_ev) + getattr(self, f'{attack_option[0]}_modifier') + self.risk_adjustment
                if threshold > getattr(card, attack_option[0]):
                    candidate_decisions.append([attack_option[0], card, attack_option[1], threshold - getattr(card, attack_option[0])])

        return candidate_decisions

    def discard_card(self, adventurer_deck: Adventurer_Deck) -> None:

        attack_options = self.find_attack_options()
        # find all cards in choices

        card_list = list(chain.from_iterable([x[1] for x in attack_options]))
        all_attack_option_cards = set(card_list)

        potential_cards = [(i, x) for i, x in enumerate(self.hand) if x not in all_attack_option_cards]

        if potential_cards:
            adventurer_deck.discard.append(potential_cards[0][1])
            del self.hand[potential_cards[0][0]]
        else:
            adventurer_deck.discard.append(self.hand[0])
            del self.hand[0]
