class ExpenseItem:
    total = 0
    def __init__(self, name='', amount=0):
        self.name = name.lower()
        self.previous_amount = amount
        self.amount = amount
        self.flag = False
        
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

    def set_amount(self, amount):
        self.previous_amount = self.amount
        self.amount = round(amount, 2)

    def get_amount(self):
        return self.amount

    def update_total(self):
        if self.flag == True:
            ExpenseItem.total -= self.previous_amount
        self.flag = True
        ExpenseItem.total += self.amount
    
