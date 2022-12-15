import psycopg2

con = psycopg2.connect(
    dbname="shop",
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port=5432
)

cur = con.cursor()

# creating User
# cur.execute("CREATE TABLE users(id serial PRIMARY KEY , name varchar NOT NULL , password varchar NOT NULL )")
# cur.execute("ALTER TABLE users ADD COLUMN email text;")

#creating Product
# cur.execute("CREATE TABLE products(id serial PRIMARY KEY , name varchar NOT NULL , vendor_code varchar NOT NULL, description varchar NOT NULL)")
# cur.execute("ALTER TABLE products ADD COLUMN rating int;")
# cur.execute("UPDATE products set rating = 5 WHERE id = 4")
# cur.execute("alter table products ALTER COLUMN review set default 'empty'")
con.commit()
cur.close()