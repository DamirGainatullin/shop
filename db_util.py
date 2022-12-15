import psycopg2

class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="shop",
            user="postgres",
            password="admin",
            host="127.0.0.1",
            port=5432
        )
        self.cur = self.con.cursor()

    def insert(self, data, table):
        if table=='users':
            self.cur.execute(f"INSERT INTO users(name, password, email, basket, bookmarks) values ('{data['name']}', '{data['password']}', '{data['email']}', '{data['basket']}', '{data['bookmarks']}');\n")
            self.con.commit()
        elif table=='products':
            self.cur.execute(f"INSERT INTO products (name, vendor_code, description, price, img) values ('{data['name']}', '{data['vendor_code']}', '{data['description']}', {data['price']}, '{data['img']}');\n")
            self.con.commit()

    def select(self, filter, value, table):
        if table=='users':
            if filter != '' and value!='':
                self.cur.execute(f"SELECT * FROM users WHERE {filter} = '{value}';\n")
            return self.cur.fetchall()
        elif table == 'products':
            if filter !='' and value!='':
                self.cur.execute(f"SELECT * FROM products WHERE products.{filter} = '{value}'")
            else:
                self.cur.execute(f"SELECT * FROM products")
            return self.cur.fetchall()

    # def show_review(self, id):
    #     self.cur.execute(f"SELECT review FROM rating WHERE product_id = {id};")
    #     return self.cur.fetchall()
    #
    # def show_rating(self, id):
    #     self.cur.execute(f"SELECT rate FROM rating WHERE product_id = {id};")
    #     return self.cur.fetchall()
    def get_comments(self, id):
        self.cur.execute(f"SELECT review,rate,user_name FROM rating WHERE product_id = {id};")
        return self.cur.fetchall()


    def add_review(self, review, rating, id, user_name):
        self.cur.execute(f"INSERT INTO rating VALUES ({id}, '{review}', {rating}, '{user_name}')")
        self.con.commit()

    def get_rate(self, id):
        self.cur.execute(f"SELECT rate FROM rating WHERE product_id = {id}")
        return self.cur.fetchall()

    def get_basket(self, user_name):
        self.cur.execute(f"SELECT basket FROM users WHERE name = '{user_name}'")
        return self.cur.fetchall()

    def get_bookmarks(self, user_name):
        self.cur.execute(f"SELECT bookmarks FROM users WHERE name = '{user_name}'")
        return self.cur.fetchall()


    def add_to_basket(self, user_name, product_id):
        self.cur.execute(f"SELECT basket FROM users WHERE name = '{user_name}'")
        basket_before = self.cur.fetchall()[0][0]
        if basket_before == '':
            basket_now = product_id
        else:
            basket_now = basket_before + ',' + product_id
        self.cur.execute(f"UPDATE users SET basket = '{basket_now}' WHERE name = '{user_name}'")
        self.con.commit()



    def add_to_bookmarks(self, user_name, product_id):
        self.cur.execute(f"SELECT bookmarks FROM users WHERE name = '{user_name}'")
        basket_before = self.cur.fetchall()[0][0]
        if basket_before == '':
            basket_now = product_id
        else:
            basket_now = basket_before + ',' + product_id
        self.cur.execute(f"UPDATE users SET bookmarks = '{basket_now}' WHERE name = '{user_name}'")
        self.con.commit()
    # def get_rating(self, id):
        # self.cur.execute(f"")