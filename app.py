from flask import Flask, render_template, request, redirect, session
from db_util import Database

app = Flask(__name__)

db = Database()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        data = {'name': request.form.get('name'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'basket': '',
        'bookmarks': ''}
        print(data)
        if len(db.select('email', data['email'], 'users')) != 0 or len(db.select('name', data['name'], 'users')) != 0:
            context = {'error': 'true'}
            return render_template('authorization.html', **context)
        db.insert(data, 'users')
        # to use data about user
        context = {
            'name': data['name'],
            'email': data['email']
        }
        return redirect('/shop')
    else:
        return render_template('authorization.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        print(name)
        data = db.select('name', name, 'users')

        if len(data) != 0:
            if data[0][-4] == password:

                # add session
                session['username'] = name
                return redirect('/shop')
            else:
                context = {'error': 'password'}
                return render_template('log_in.html', **context)
        else:
            context = {'error': 'name'}
            return render_template('log_in.html', **context)
        # print(name)
        # print(data)
    else:
        context = {'error': 'no'}
        return render_template('log_in.html', **context)

@app.route('/shop')
def shop():

    products = db.select('', '', 'products')
    # print(products)
    context = {
        'username': session['username'],
        'data': products
    }
    return render_template('shop.html', **context)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    try:
        comments = db.get_comments(product_id)
    except Exception:
        comments = []
    product = db.select('id', product_id, 'products')
    rate_list_tuples = db.get_rate(product_id)
    rate_list = list(map(lambda x: x[0], rate_list_tuples))

    # get rate as a list of all user ratings
    if len(rate_list_tuples) != 0:
        rate =  sum(rate_list) // len(rate_list_tuples)
    else:
        rate = None
    context = {
        'let_rate': True,
        'data': product,
        'comments': comments,
        'rate': rate,
        'username': session['username']
    }
    if request.method == 'POST':
        review = request.form.get('review')
        rating = request.form.get('rating')
        #add to bd
        db.add_review(review, rating, product_id, session['username'])
        context = {
            'username': session['username'],
            'let_rate': False,
            'data': product,
            'comments': comments,
            'rate': rate
        }
    return render_template('product.html', **context)

@app.route('/basket<user_name>')
def basket(user_name):
    data1 = '1'
    data2 = '1'
    products_in_basket = db.get_basket(user_name)
    if not products_in_basket[0][0]:
        data1 = ''
    else:
        products_in_basket = products_in_basket[0][0].split(',')
    product_in_bookmarks = db.get_bookmarks(user_name)
    if not product_in_bookmarks[0][0]:
        data2 = ''
    else:
        product_in_bookmarks = product_in_bookmarks[0][0].split(',')
    if data1 != '':
        for i in products_in_basket:
            data1 += str(db.select('id', int(i), 'products')[0][0])
    if data2 != '':
        for i in product_in_bookmarks:
            data2 += str(db.select('id', int(i), 'products')[0][0])

    data1 = set(data1)
    data2 = set(data2)
    basket = []
    bookmarks = []
    for i in data1:
        product = db.select('id', int(i), 'products')[0]
        basket.append(product)
    for i in data2:
        product = db.select('id', int(i), 'products')[0]
        bookmarks.append(product)
    context = {
        'products': basket,
        'wishlist': bookmarks
    }
    return render_template('basket.html', **context)

@app.route('/add_basket<product_id>')
def add_basket(product_id):
    db.add_to_basket(session['username'], product_id)
    return redirect(f"/basket{session['username']}")



@app.route('/add_bookmarks<product_id>')
def add_bookmarks(product_id):
    db.add_to_bookmarks(session['username'], product_id)
    return redirect(f"/basket{session['username']}")


@app.route('/add_all_bookmarks')
def add_all_bookmarks():
    user = session['username']
    bookmarks = db.select('name', user, 'users')[0]
    print(bookmarks)
    for i in bookmarks:
        db.add_to_basket(user, int(i))
    return redirect(f'basket{user}')

if __name__ == '__main__':
    app.run(debug=True)
