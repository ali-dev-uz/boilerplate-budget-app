class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        output = self.category.center(30, "*") + "\n"
        for item in self.ledger:
            output += f"{item['description'][:23]:23} {item['amount']:.2f}\n"
        output += f"Total: {self.get_balance():.2f}"
        return output


def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    spent = [(c.category, sum(item["amount"] for item in c.ledger if item["amount"] < 0)) for c in categories]
    total_spent = sum(spent_value for _, spent_value in spent)

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for category, spent_value in spent:
            bar = "o" if (spent_value / total_spent) * 100 >= i else " "
            chart += bar.rjust(3) + "  "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    max_len = max(len(category.category) for category in categories)
    for i in range(max_len):
        chart += "     "
        for category in categories:
            if i < len(category.category):
                chart += category.category[i] + "  "
            else:
                chart += "   "
        chart += "\n"

    return chart
