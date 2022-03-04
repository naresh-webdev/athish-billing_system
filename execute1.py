import mysql.connector as ms


x = ms.connect(host='localhost', user='root',
               passwd='')
# buffered is an attribute ,If buffered is True , the cursor fetches all rows from the server after an operation is executed.

cur = x.cursor(buffered=True)

cur.execute('create database athish_new')
cur.execute('use athish_new')

#  -- this is for creating the product table which is basically the market--
cur.execute(
    'create table product(id int,name varchar(30),qty int,price_per_item float)')
cur.execute("insert into product values(1,'apples',30,40),(2,'oranges',40,20),(3,'mango',30,25),(4,'strawberry',80,20),(5,'watermelon',20,60)")
x.commit()


cur.execute('create table feedback(name varchar(30),review varchar(150))')
cur.execute(
    "create table customer(product_name varchar(30),qty int,amount float)")

print('tables created successfully \n now execute the second file..')
