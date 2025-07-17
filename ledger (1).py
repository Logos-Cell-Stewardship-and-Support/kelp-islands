"""SeaBrick Ledger: Manages allocation, staking, and conviction logic."""

from collections import defaultdict

class SeaBrickLedger:
    def __init__(self):
        self.balances = defaultdict(int)
        self.stakes = defaultdict(lambda: defaultdict(int))
        self.conviction = defaultdict(lambda: defaultdict(float))
        self.decay_rate = 0.9  # conviction decay per round

    def mint(self, user, amount):
        self.balances[user] += amount

    def transfer(self, sender, recipient, amount):
        if self.balances[sender] >= amount:
            self.balances[sender] -= amount
            self.balances[recipient] += amount
            return True
        return False

    def stake(self, user, project_id, amount):
        if self.balances[user] >= amount:
            self.balances[user] -= amount
            self.stakes[user][project_id] += amount
            return True
        return False

    def update_conviction(self):
        for user, projects in self.stakes.items():
            for project_id, amount in projects.items():
                self.conviction[user][project_id] = (
                    self.conviction[user][project_id] * self.decay_rate + amount
                )

    def total_staked(self, project_id):
        return sum(stake[project_id] for stake in self.stakes.values())

    def conviction_score(self, project_id):
        return sum(conv[project_id] for conv in self.conviction.values())
