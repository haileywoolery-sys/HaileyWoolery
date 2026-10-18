class Category:
    """
    Represents a single budget category (e.g., Food, Clothing, Entertainment)
    tracked through an internal financial ledger.
    """
    def __init__(self, name):
        self.name = name
        self.ledger = []  # Holds a history of transactions as dictionaries: {"amount": float, "description": str}

    def deposit(self, amount, description=""):
        """Adds a positive amount and an optional description to the ledger."""
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        Deducts an amount from the ledger if sufficient funds exist.
        Returns True if successful, False otherwise.
        """
        if self.check_funds(amount):
            # Withdrawals are stored as negative numbers
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        """Calculates and returns the current balance based on all ledger transactions."""
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, budget_category):
        """
        Transfers an amount from the current category to a target budget category.
        Returns True if successful, False otherwise.
        """
        if self.check_funds(amount):
            # Withdraw from this category and deposit into the target category
            self.withdraw(amount, f"Transfer to {budget_category.name}")
            budget_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        """Helper method that checks if the category has enough money for a transaction."""
        return self.get_balance() >= amount

    def __str__(self):
        """
        Formats the ledger into a printable bank-statement layout.
        Centers the title and aligns transaction descriptions and amounts cleanly.
        """
        # Centered title row, 30 characters wide, padded with asterisks (e.g., *************Food*************)
        title = f"{self.name:*^30}\n"
        
        items = ""
        for item in self.ledger:
            # Truncate descriptions to 23 characters and amounts to 7 characters max
            desc = item["description"][:23]
            amt = f"{item['amount']:.2f}"[:7]
            # Left-align description (23 chars) and right-align amount (7 chars)
            items += f"{desc:<23}{amt:>7}\n"
            
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    """
    Generates a visual bar chart (using text) representing the percentage 
    of total spending belonging to each budget category.
    """
    # 1. Calculate the total withdrawals (spending) for each category
    spent_per_category = []
    for cat in categories:
        # Sum only the negative amounts in the ledger
        spent = sum(-item["amount"] for item in cat.ledger if item["amount"] < 0)
        spent_per_category.append(spent)
        
    total_spent = sum(spent_per_category)
    
    # 2. Convert raw spending to rounded-down percentages (multiples of 10)
    if total_spent == 0:
        percentages = [0] * len(categories)
    else:
        # Math trick: // 10 * 10 removes the ones digit, rounding down to the nearest 10% (e.g., 76% -> 70%)
        percentages = [int((spent / total_spent) * 100 // 10 * 10) for spent in spent_per_category]

    # 3. Build the chart y-axis and plot points ("o") from 100% down to 0%
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "  # Right-align percentages with a width of 3
        for pct in percentages:
            # Print an 'o' if the category's percentage meets or exceeds the current line level
            chart += "o  " if pct >= i else "   "
        chart += "\n"
        
    # 4. Add the horizontal divider line beneath the bars
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    # 5. Print category names vertically at the bottom of the chart
    names = [cat.name for cat in categories]
    max_len = max(len(name) for name in names)
    # Right-pad all names with spaces to match the length of the longest name
    padded_names = [name.ljust(max_len) for name in names]
    
    # Iterate row by row through the vertical text characters
    for i in range(max_len):
        chart += "     "  # Initial margin to match the chart axis spacing
        for name in padded_names:
            chart += f"{name[i]}  "
        chart += "\n"
            
    return chart.rstrip("\n")  # Strip trailing newline for clean output parsing
