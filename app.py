from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Global account (for demo)
balance = 0
transactions = []

@app.route('/')
def index():
    return render_template('index.html', balance=balance)

@app.route('/deposit', methods=['POST'])
def deposit():
    global balance
    amount = float(request.form['amount'])
    balance += amount
    transactions.append(("Deposit", amount))
    return render_template('index.html', balance=balance, message=f"Deposited ₹{amount}")

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    amount = float(request.form['amount'])
    if amount > balance:
        return render_template('index.html', balance=balance, message="❌ Insufficient balance!")
    balance -= amount
    transactions.append(("Withdraw", amount))
    return render_template('index.html', balance=balance, message=f"Withdrew ₹{amount}")

@app.route('/transactions')
def show_transactions():
    df = pd.DataFrame(transactions, columns=["Type", "Amount"])
    return render_template('transactions.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

@app.route('/plot')
def plot():
    df = pd.DataFrame(transactions, columns=["Type", "Amount"])
    if df.empty:
        return "No transactions yet."
    img = BytesIO()
    df.groupby("Type")["Amount"].sum().plot(kind='bar', color=['green', 'red'])
    plt.title("Transaction Summary")
    plt.ylabel("Amount (₹)")
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return f'<img src="data:image/png;base64,{plot_url}"/>'

if __name__ == '__main__':
    app.run(debug=True)
