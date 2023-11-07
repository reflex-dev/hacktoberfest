# Expense Tracker

Manage your expenses and see how much you are saving seamlessly

## Getting Started
- First of all you need to clone this repo
- Go to the Capeddemon_Expense_Tracker folder
 Run this command - 
 `
 pip3 install requirements.txt
 `
- Run reflex
`
reflex run
`
- Enter the account balance or money you currently have. It will be added in balance.txt
- Then, enter the expenses, date, and amount spend. Click on add.
- Similarly enter the same thing accordingly to delete particular expenses
- Show expenses to see what you have deleted and added.
- Show summary to see much is left.
- Enter the left amount again and click on add or change to update
- See the universal and particular date graphs.


### Tutorial

https://github.com/CapedDemon/reflex-hacktoberfest/assets/93109967/fe822038-f5f8-48d1-84be-d0455a6603c4



## Libraries Used
- reflex
- matplotlib

## Docs
- The full frontend is made using reflex. 
- The database is sqlite and uses a simpler model
`
class Expense(rx.Model, table=True):
    expense: str = Field()
    date: str = Field()
    amount: str = Field()
`

- Also the user can see a full details of his/her expenses with the help of the graph
- The universal graph shows a line graph where how much amount is spend in particular dates are shown.
- The graph of a particular date shows in which places you have spend the most.

