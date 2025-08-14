from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

purchases = []
buyer_info = {}

@app.route('/')
def index():
    return render_template('index.html', purchases=purchases)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    total_price = price * quantity

    purchases.append({
        'item_name': item_name,
        'price': price,
        'quantity': quantity,
        'total_price': total_price
    })

    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        buyer_info['name'] = request.form['buyer_name']
        buyer_info['address'] = request.form['buyer_address']
        return redirect(url_for('show_invoice'))

    total_bill = sum(item['total_price'] for item in purchases)
    return render_template('checkout.html', purchases=purchases, total_bill=total_bill)

@app.route('/show_invoice')
def show_invoice():
    if not purchases or not buyer_info:
        return redirect(url_for('index'))
    
    total_bill = sum(item['total_price'] for item in purchases)
    return render_template('invoice.html', purchases=purchases, total_bill=total_bill, buyer_info=buyer_info)

@app.route('/clear_all')
def clear_all():
    purchases.clear()
    buyer_info.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)