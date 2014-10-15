#!/usr/bin/env python3

class Valuation(object):
    def __init__(self, shares=0, total_shares=1, date='', price_per_share=0, amount_raised=0, percent=0, deals=None):
        # EACH DEAL OBJECT SHOULD END UP WITH THE FOLLOWING STATS:
        # self.shares
        # self.total_shares
        # self.percent
        # self.price_per_share
        # self.amount_raised
        # self.premomey
        # self.postmoney
        
        self.deals = deals
        self.price_per_share = price_per_share
        self.amount_raised = amount_raised
        self.percent = percent
        self.date = date
        if deals:
            # it does this if this is two or more SH01s being added together
            alltotalshares = []
            self.shares = 0
            self.price_per_share = []
            for i in range(len(deals)):
                self.shares += deals[i].shares
                alltotalshares.append(deals[i].total_shares)
                self.amount_raised += deals[i].shares * deals[i].price_per_share
                self.price_per_share.append(deals[i].price_per_share)
            self.total_shares = max(alltotalshares)
            self.percent = self.shares / self.total_shares
        else:
            # simple deal
            self.shares = shares
            if self.shares == 1:
                self.plural = ''
            else: self.plural = 's'
            self.total_shares = total_shares
            # FIGURE OUT THE PERCENTAGE AND SHARES
            if not self.percent: # normally percent is not entered:
                self.percent = self.shares / self.total_shares
            elif not self.shares: # instead if percent is entered but shares are not:
                self.shares = self.percent * self.total_shares
            elif not self.total_shares: # instead if percent and shares are entered but total shares are not:
                self.total_shares = self.shares / self.percent
            # FIGURE OUT THE AMOUNT RAISED AND PRICE PER SHARE
            if not self.amount_raised: # normally amount raised is not entered:
                self.amount_raised = self.shares * self.price_per_share
            elif not self.price_per_share: # instead if amount raised is entered but price per share isn't:
                self.price_per_share = self.amount_raised / self.shares
            self.d_price_per_share = str(round(self.price_per_share, 4))
        # FIGURE OUT PRE- AND POST-MONEY
        self.postmoney = self.amount_raised / self.percent
        self.premoney = self.postmoney - self.amount_raised
        # VALUES FOR DISPLAY
        self.d_percent = str(round(100 * self.percent, 4))
        self.d_postmoney = str(round(self.postmoney, 4))
        self.d_premoney = str(round(self.premoney, 4))
        self.d_amount_raised = str(round(self.amount_raised, 4))
    
    def get_message(self): # creates a message that can be output in the gui
        shares_message = ''
        shares_bought_message = ''
        if self.deals:
            for i in range(len(self.deals)):
                shares_message += str(self.deals[i].shares) + " share" + self.deals[i].plural + " @ " + self.deals[i].d_price_per_share + " per share\n"
            shares_bought_message = "Total shares bought: " + str(self.shares) + "\n"
        else:
            shares_message = str(self.shares) + " share" + self.plural + " @ " + self.d_price_per_share + " per share\n"
        message = '\n#################################\n' + \
               shares_message + shares_bought_message + \
               self.d_percent + "% of " + str(self.total_shares) + " total shares" \
               "\n" + "Amount raised: " + self.d_amount_raised + \
               "\nPre-money: " + self.d_premoney + \
               "\nPost-money: " + self.d_postmoney
        return message



