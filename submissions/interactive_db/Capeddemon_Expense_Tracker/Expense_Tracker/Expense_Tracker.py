"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import datetime
from rxconfig import config
from sqlmodel import Field
import matplotlib.pyplot as plt
import reflex as rx
currentime = datetime.datetime.now()

with open("others/balance.txt", 'r') as f:
    balance = float(f.read())


class State(rx.State):
    """The app state."""
    expenseInfo = {"expense": None, "amount": 0.00, "date": None}
    showExpense = False
    balance = 0
    expenses = []
    dates = []
    amounts = []
    totalItems = []
    dateGraph2 = ""
    graphDataset1 = []
    graphDataset2 = []
    sumAmount = 0
    showUnivGraph = False
    showAmount = False

    def setExpenseInfo(self, value, valueType):
        self.expenseInfo[valueType] = value

    def addExpense(self):
        try:
            with rx.session() as session:
                self.expense = Expense(
                    expense=self.expenseInfo["expense"], date=self.expenseInfo["date"], amount=self.expenseInfo["amount"])
                session.add(self.expense)
                session.commit()
                rx.alert("Added Successfully")
        except:
            rx.alert("Cannot add.")

    def addBalance(self, amount):
        self.balance = amount

    def editBalance(self):
        with open("others/balance.txt", "r") as f:
            data = f.read()
            if data != "":
                rx.alert("Your's previous amount was ", data)

        with open("others/balance.txt", "w") as f:
            f.write(self.balance)

        rx.alert("Edited Successfully")

    def deleteExpense(self):
        try:
            with rx.session() as session:
                self.delExpense = session.query(Expense).filter_by(
                    expense=self.expenseInfo["expense"], date=self.expenseInfo["date"], amount=self.expenseInfo["amount"]).delete()
                session.commit()
        except:
            rx.alert("Cannot add.")

    def getExpenses(self):
        with rx.session() as session:
            self.expensesList = session.query(Expense).all()
        j = 1
        for i in self.expensesList:
            self.expenses.append(i.expense)
            self.amounts.append(i.amount)
            self.dates.append(i.date)
            self.totalItems.append(j)

            j += 1
        self.showExpense = True

    def amountSummary(self):
        with rx.session() as session:
            self.expensesList = session.query(Expense).all()
        sumAmount=0
        for i in self.expensesList:
            sumAmount+=float(i.amount)

        with open("others/balance.txt", "r") as f:
            self.balance = float(f.read())

        self.sumAmount = sumAmount
        self.showAmount = not (self.showAmount)

    def showGraph1(self):
        self.graphDataset1=[]
        
        with rx.session() as session:
            self.expensesList = session.query(Expense).all()
        newDate = ""
        for i in self.expensesList:
            if newDate==i.date:
                continue
            else:
                newDate = i.date
                sumAmount = 0
                for j in self.expensesList:
                    if j.date == i.date:
                        sumAmount += float(j.amount)

                self.graphDataset1.append({"date":i.date, "amount":sumAmount})
        print(self.graphDataset1)

        dates1 = []
        amount1 = []

        for i in self.graphDataset1:
            dates1.append(i["date"])
            amount1.append(i["amount"])
        plt.plot(dates1, amount1)
        plt.xlabel("Dates")
        plt.ylabel("Amount")
        plt.title("Universal Graph")
        plt.show()

        self.showUnivGraph = True

    def graph2date(self, dateGraph2):
        self.dateGraph2 = dateGraph2

    def showGraph2(self):
        self.graphDataset2=[]
        with rx.session() as session:
            self.graph2Data = session.query(Expense).filter_by(date=self.dateGraph2).all()
        
        for i in self.graph2Data:
            self.graphDataset2.append({"expense":i.expense, "amount":i.amount})
        print(self.graphDataset2)
        amount2=[]
        expense2=[]
        for i in self.graphDataset2:
            amount2.append(i["amount"])
            expense2.append(i["expense"])

        plt.bar(expense2, amount2)
        plt.xlabel("expenses")
        plt.ylabel("amount")
        plt.title(self.dateGraph2)
        plt.show()

class Expense(rx.Model, table=True):
    expense: str = Field()
    date: str = Field()
    amount: str = Field()


def addExpense() -> rx.Component:
    inputExpense = dict(border_width="1px", padding="1px", width="300px")
    buttonStyle = dict(shadow="rgba(0,0,0,0.15) 0px 2px 8px", bg="#18f252")
    return rx.vstack(
        rx.desktop_only(
            rx.hstack(
                rx.input(
                    placeholder="Expense - Food, books ...",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "expense")

                ),
                rx.input(
                    placeholder="Date",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(value, "date")

                ),
                rx.input(
                    placeholder="Amount",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "amount")

                )

            ),
        ),
        rx.mobile_and_tablet(
            rx.vstack(
                rx.input(
                    placeholder="Expense - Food, books ...",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "expense")

                ),
                rx.input(
                    placeholder="Date",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "date")

                ),
                rx.input(
                    placeholder="Amount",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "amount")

                ),

            ),
        ),
        rx.button("Add", style=buttonStyle, on_click=State.addExpense)

    )


def delExpenses() -> rx.Component:
    inputExpense = dict(border_width="1px", padding="1px", width="300px")
    buttonStyle = dict(shadow="rgba(0,0,0,0.15) 0px 2px 8px", bg="#f21818")
    return rx.vstack(
        rx.desktop_only(
            rx.hstack(
                rx.input(
                    placeholder="Expense - Food, books ...",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "expense")

                ),
                rx.input(
                    placeholder="Date",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(value, "date")

                ),
                rx.input(
                    placeholder="Amount",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "amount")

                )

            ),
        ),
        rx.mobile_and_tablet(
            rx.vstack(
                rx.input(
                    placeholder="Expense - Food, books ...",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "expense")

                ),
                rx.input(
                    placeholder="Date",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "date")

                ),
                rx.input(
                    placeholder="Amount",
                    style=inputExpense,
                    on_change=lambda value: State.setExpenseInfo(
                        value, "amount")

                ),

            ),
        ),
        rx.button("Delete", style=buttonStyle, on_click=State.deleteExpense)
    )


def edit_balance() -> rx.Component:
    buttonStyle = dict(shadow="rgba(0,0,0,0.15) 0px 2px 8px")
    inputStyle = dict(border_width="1px", padding="1px", width="300px")
    return rx.box(
        rx.vstack(
            rx.input(
                placeholder="New Amount",
                style=inputStyle,
                on_change=lambda value: State.addBalance(value)
            ),
            rx.tablet_and_desktop(
                rx.hstack(

                    rx.button("Add Balance", style=buttonStyle,
                              bg="cyan", on_click=State.editBalance),
                    rx.button("Change Balance", style=buttonStyle,
                              bg="green", on_click=State.editBalance),

                )
            ),
            rx.mobile_only(
                rx.vstack(
                    rx.button("Add Balance", style=buttonStyle,
                              bg="cyan", on_click=State.editBalance),
                    rx.button("Change Balance", style=buttonStyle,
                              bg="green", on_click=State.editBalance),
                )
            )
        )
    )


def showEachExpense(expenseVal: rx.Var[str]) -> rx.Component:
    return rx.list_item(
        rx.text(f"{expenseVal} -> ", font_size="18px",
                align="center", color="cyan")
    )


def showEachDate(dateVal: rx.Var[str]) -> rx.Component:
    return rx.list_item(
        rx.text(f"{dateVal} -> ", font_size="18px",
                align="center", color="orange")
    )


def showEachAmount(amountVal: rx.Var[float]) -> rx.Component:
    return rx.list_item(
        rx.text(f"{amountVal}", font_size="18px",
                align="center", color="green")
    )


def showNumber(number: rx.Var[int]) -> rx.Component:
    return rx.list_item(
        rx.text(f"{number} .", font_size="20px", align="center")
    )


def showAllExpense() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.list(
                    rx.foreach(State.totalItems, lambda item: showNumber(item))
                ),
                rx.list(


                    rx.foreach(State.expenses,
                               lambda item: showEachExpense(item)),


                ),
                rx.list(
                    rx.foreach(State.dates, lambda item: showEachDate(item)),

                ),
                rx.list(
                    rx.foreach(State.amounts,
                               lambda item: showEachAmount(item)),

                )
            )

        ),

    )


def index() -> rx.Component:
    buttonStyle = dict(shadow="rgba(0,0,0,0.15) 0px 2px 8px")
    inputStyle = dict(border_width="1px", padding="1px", width="300px")
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(),
                             right="0", position="fixed"),
        rx.vstack(
            rx.heading("Welcome to Expense Tracker",
                       font_size="35px", align="center"),
            rx.box(
                rx.vstack(
                    rx.text(
                        f"Today's date is - {currentime.day}/{currentime.month}/{currentime.year}", font_size="20px"),
                    rx.text("Time is money", align="center",
                            font_size="20px", color="green")
                )
            ),
            rx.box(
                rx.vstack(
                    rx.tablet_and_desktop(
                        rx.heading(
                            "Manage your expenses and see how much you are saving seamlessly.", center="align", font_size="25px"),
                        rx.heading(
                            "See the the detailed analysis of your expenses through the graph.", center="align", font_size="25px")
                    ),
                    rx.mobile_only(
                        rx.text("Manage your expenses and see how much you are saving seamlessly.",
                                center="align", font_size="25px"),
                        rx.text("See the the detailed analysis of your expenses through the graph.",
                                center="align", font_size="25px")

                    )
                )
            ),
            rx.divider(),
            rx.box(
                rx.vstack(
                    rx.heading("Balance/Money You Have", align="center"),
                    
                    edit_balance(),

                )
            ),
            rx.box(
                rx.vstack(
                    rx.text("Add Your Expenses", font_size="30px"),
                    addExpense(),
                    delExpenses()
                ),
            ),
            rx.box(
                rx.vstack(
                    rx.button("Show Expenses", style=buttonStyle,
                              color="cyan", on_click=State.getExpenses()),
                    rx.cond(
                        State.showExpense,
                        rx.box(showAllExpense()),
                        rx.text('')
                    ),

                )
            ),
            rx.box(
                rx.vstack(
                    rx.button("Show Summary", style=buttonStyle,
                              color="cyan", on_click=State.amountSummary()),
                    rx.cond(
                        State.showAmount,
                        rx.text(
                            f"Total expense till date - {State.sumAmount} and amount left {(State.balance) - State.sumAmount}"),
                        rx.text('')
                    ),
                )
            ),
            rx.box(
                rx.vstack(
                    rx.button("Universal Graph", style=buttonStyle,
                              color="cyan", on_click=State.showGraph1()),
                    rx.box(
                        rx.vstack(
                        rx.text("Enter date to see the expense of particular date - ", font_size="18px", align="center"),
                        rx.input(
                            placeholder="date",
                            style=inputStyle,
                            on_change=lambda value:State.graph2date(value)
                        ),
                    rx.button("See Graph", style=buttonStyle,
                              color="cyan", on_click=State.showGraph2()),
                    
                    ),
                    
                    spacing="1.5em",
                    )
                )
            ),
        

            spacing="1.5em",
            font_size="2em",
            padding_top="5%",

        ),
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
