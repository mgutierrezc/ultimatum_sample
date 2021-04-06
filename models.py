from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import config_leex_1

doc = """
Ultimatum game with two treatments: direct response 
In the former, one player makes an offer and the other either accepts or rejects.
It comes in two flavors, with and without hypothetical questions about the second player's 
response to offers other than the one that is made.
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 4

    instructions_template = 'ultimatum/Instructions.html'

    endowment = c(config_leex_1.UG_endowment) ## Notice this come from a config file

    payoff_if_rejected = c(0)

    offer_increment = c(1)

    offer_choices = currency_range(0, endowment, offer_increment)

    offer_choices_count = len(offer_choices)

    keep_give_amounts = []

    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)

        #for g in self.get_groups():
            #if 'treatment' in self.session.config:
                #g.use_strategy_method = self.session.config['use_strategy_method']
            #else:
             #   g.use_strategy_method = random.choice([True, False])
    
    def vars_for_admin_report(self):        
        avg_proposal = 0
        accepted_offers = 0

        num_groups = len(self.get_groups())
        no_offers = True

        for group in self.get_groups():
            if group.amount_offered != None:
                avg_proposal += group.amount_offered/num_groups
                
            if group.offer_accepted != None:
                accepted_offers += int(group.offer_accepted)

            if group.offer_accepted != None and group.amount_offered != None:
                if no_offers is True:
                    no_offers = False


        #TODO: debug this vars
        acceptance_percent = accepted_offers/num_groups*100 
        rejection_percent = 100 - acceptance_percent

        if no_offers is False:
            return {
                        'avg_proposal': avg_proposal,
                        'acceptance_percent': str(acceptance_percent) + "%",
                        'rejection_percent': str(rejection_percent) + "%",
                    }
        else:
            return {
                'avg_proposal': '(no data)',
                'acceptance_percent': '(no data)',
                'rejection_percent': '(no data)',
            }


def question(amount):
    return 'Acep    tarías una oferta de {}?'.format(c(amount))


class Group(BaseGroup):
    # use_strategy_method = models.BooleanField(
    #     doc="""Whether this group uses strategy method"""
    # )
    #
    amount_offered = models.CurrencyField(choices=Constants.offer_choices)
    #
    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)"
    )

    # for admin report
    # avg_proposal = models.CurrencyField(initial=0)
    # acceptance_percent = models.FloatField(initial=0)
    # rejection_percent = models.FloatField(initial=0)

    #
    # # for strategy method
    # response_0 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(0))
    # response_10 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(10))
    # response_20 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(20))
    # response_30 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(30))
    # response_40 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(40))
    # response_50 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(50))
    # response_60 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(60))
    # response_70 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(70))
    # response_80 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(80))
    # response_90 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(90))
    # response_100 = models.BooleanField(
    #     widget=widgets.RadioSelectHorizontal(), verbose_name=question(100))
    #

    def set_payoffs(self):
        p1, p2 = self.get_players()

        # if self.use_strategy_method:
        #     self.offer_accepted = getattr(self, 'response_{}'.format(
        #         int(self.amount_offered)))

        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):

    round_payoff = models.CurrencyField()

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'
