from flask import Flask, request, render_template_string
import threading
import mysql.connector

application = Flask(__name__)

def get_accounts():
    cnx = mysql.connector.connect(
        host='atm-sql-data.mysql.database.azure.com',
        user='atmdata',
        password='FDMgroup123',
        database='bankaccount'
    )
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM accbal")
    rows = cursor.fetchall()
    # Convert Decimal instances to float
    accounts = {str(row[0]): float(row[1]) for row in rows}
    cursor.close()
    cnx.close()
    return accounts

def simulate_atm(accounts, account_number):
    balance = accounts.get(account_number)
    if balance is not None:
        return f"The balance for account {account_number} is {balance}"
    else:
        return "Account not found"

template = """
<!DOCTYPE html>
<html>
<body>
    <form method="POST">
        <label for="account_number">Account Number:</label><br>
        <input type="text" id="account_number" name="account_number"><br>
        <input type="submit" value="Submit">
    </form>
    {% if result %}
        <p>{{ result }}</p>
    {% endif %}
</body>
</html>
"""

@application.route('/', methods=['GET', 'POST'])
def index():
    accounts = get_accounts()
    result = None
    if request.method == 'POST':
        account_number = request.form.get("account_number")
        result = simulate_atm(accounts, account_number)
    return render_template_string(template, accounts=accounts, result=result)


if __name__ == '__main__':
    application.run()