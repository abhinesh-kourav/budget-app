def create_spend_chart(categories):
    line100 = '100|'
    line90 = ' 90|'
    line80 = ' 80|'
    line70 = ' 70|'
    line60 = ' 60|'
    line50 = ' 50|'
    line40 = ' 40|'
    line30 = ' 30|'
    line20 = ' 20|'
    line10 = ' 10|'
    line0 = '  0|'
    catLen = list()
    for category in categories:
        catLen.append(len(category.name))
        percent = get_percent(category, categories)
        line0 += " o " if percent>=0 else '   '
        line10 += " o " if percent>=10 else '   '
        line20 += " o " if percent>=20 else '   '
        line30 += " o " if percent>=30 else '   '
        line40 += " o " if percent>=40 else '   '
        line50 += " o " if percent>=50 else '   '
        line60 += " o " if percent>=60 else '   '
        line70 += " o " if percent>=70 else '   '
        line80 += " o " if percent>=80 else '   '
        line90 += " o " if percent>=90 else '   '
        line100 += " o " if percent>=100 else '   '
    dashLine = "    "
    for x in range(len(categories)*3+1):
        dashLine += '-'
    catAxis=''
    for x in range(max(catLen)):
        catAxis += '    '
        for category in categories:
            if x > len(category.name)-1:
                catAxis += "   "
            else:
                catAxis += " " + category.name[x] + ' '
        catAxis += ' \n'
    catAxis = catAxis.rstrip('\n')
    result = "Percentage spent by category\n" + line100 +" " + '\n' + line90 + " " + '\n' + line80 + " " + '\n' + line70 + " " +'\n'+ line60 + " " + '\n'+ line50 + " " + '\n'+ line40 + " " + '\n'+ line30 + " " + '\n'+ line20 + " " + '\n'+ line10 + " " + '\n'+ line0 + " " + '\n' + dashLine + '\n' + catAxis
    return result
    
    



def get_percent(category, categories):
    total_withdrawn = 0
    for cat in categories:
        withdrawn = cat.get_withdrawals()
        total_withdrawn += withdrawn
    percent = category.get_withdrawals()/total_withdrawn*100
    return percent

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        title = self.name.center(30)
        resTitle = title.replace(' ','*')+'\n'
        resStuff=''
        for item in self.ledger:
            decAmt = str(round(float(item['amount']),2))
            if len(decAmt.split('.')[1])==1:
                decAmt += '0'
            resStuff += item["description"][0:23] + decAmt.rjust(30-len(item["description"][0:23])) + '\n'
        resSum = "Total: "+ str(self.get_balance())
        result = resTitle + resStuff + resSum
        return result

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_amount = 0
        for item in self.ledger:
            total_amount += item['amount']
        return total_amount

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount,"Transfer to "+ category.name)
            category.deposit(amount, "Transfer from "+ self.name)
            return True
        return False

    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        return False

    def get_withdrawals(self):
        withdrawals = 0
        for item in self.ledger:
            if item["amount"] < 0:
                withdrawals += item['amount']
        withdrawals = -withdrawals
        return withdrawals