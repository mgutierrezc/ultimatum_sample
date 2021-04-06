from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants
import config_leex_1

class Introduction(Page):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1


class Offer(Page):
    form_model = models.Group
    form_fields = ['amount_offered']

    def is_displayed(self):
        return self.player.id_in_group == 1


class WaitForProposer(WaitPage):
    pass


class Accept(Page):
    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2   #and not self.group.use_strategy_method

#
# class AcceptStrategy(Page):
#     form_model = models.Group
#     form_fields = ['response_{}'.format(int(i)) for i in
#                    Constants.offer_choices]
#
#     def is_displayed(self):
#         return self.player.id_in_group == 2 and self.group.use_strategy_method


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):


    def before_next_page(self):

        # pass payoff to new var
        self.player.round_payoff = self.player.payoff

        if config_leex_1.paid_game == Constants.name_in_url and config_leex_1.paid_round == self.round_number:
            self.player.payoff = self.player.payoff
        else:
            self.player.payoff = 0


page_sequence = [Introduction,
                 Offer,
                 WaitForProposer,
                 Accept,
                 ResultsWaitPage,
                 Results]
