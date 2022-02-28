import mysql.connector as ms


x = ms.connect(host='localhost', user='root',
               passwd='Naresh@2004', database='athish')
cur = x.cursor(buffered=True)

# use it for the first time use the  commented block of code by commenting every other line below except the one which are already commented!!⚠

# cur.execute('create table product(id int,name varchar(30),qty int,price_per_item float)')
# cur.execute("insert into product values(1,'apples',30,40),(2,'oranges',40,20),(3,'mango',30,25),(4,'strawberry',80,20),(5,'watermelon',20,60)")
# x.commit()
# cur.execute('create table feedback(name varchar(30),review varchar(150))')
#cur.execute("create table customer(product_name varchar(30),qty int,amount float)")


def display_items():
    cur.execute('select name,price_per_item,qty from product')
    data = cur.fetchall()
    print('(name , price per unit , qty available)')
    for i in data:
        print(i)
    print('\n')


def display_basket():
    cur.execute('select * from customer')
    data = cur.fetchall()
    for i in data:
        print(i)
    print('\n')


def check_item(itemname):
    itempresent = 0
    cur.execute("select distinct product_name from customer")
    data = cur.fetchall()
    l = []
    for i in data:
        if i[0] == itemname:
            return True
    return False


while True:
    print('--------------availabe functions--------------\n')
    print('actions that can be done using this billing system software are : \n')
    print("1.display all the available items in the product \n")
    print("2.add item to my basket \n")
    print('3.remove item form my basket \n')
    print('4.show basket\n')
    print('5.generate the bill \n')
    print('6.quit market\n')
    print('7.feedback\n')
    print('8.add item to the market[admin privillige]\n')
    ch = int(input('Enter your your choice : '))
    print('\n')

    if ch in [1, 2, 3, 4, 5, 6, 7, 8]:
        if ch == 1:
            display_items()
            dec = input('do you want to perform any other task (y/n) :')
            if dec == 'n':
                print('visit again later 🙏')
                break
            else:
                continue

        elif ch == 2:

            boolean = 1
            while boolean:
                print('available items in the store currently are : ')
                print('(id,name,qty,price per item)')
                cur.execute('select id,name,qty,price_per_item from product')
                data = cur.fetchall()
                for i in data:
                    print(i)
                print('\n')
                item_id = input('select item id to add item to the basket : ')
                cur.execute(
                    'select qty from product where id={}'.format(item_id))
                data2 = cur.fetchall()
                len = data2[0]
                if len == 0:
                    print('the select item is curretly out of stock')
                    ch1 = input('want to add any other items ? (y/n) : ')
                    if ch1 == n:
                        boolean = 0
                        break
                else:
                    print('selected item is available in the market ✔')
                    no_itemsadded = int(
                        input('enter the qty of items to be added to the basket : '))
                    cur.execute(
                        'select price_per_item,name from product where id={}'.format(item_id))
                    data2 = cur.fetchone()
                    pu, cname = data2[0], data2[1]
                    cost = pu * no_itemsadded
                    cur.execute("insert into customer values('{}',{},{})".format(
                        cname, no_itemsadded, cost))
                    print('\n item added succesfully😊')
                    x.commit()
                    cur.execute(
                        "update product set qty=qty-{} where id={}".format(no_itemsadded, item_id))
                    ch2 = input('do you want to add more items : (y/n) ')
                    if ch2 == 'n':
                        break
                    else:
                        continue

        elif ch == 3:
            print('--------items in your basket are--------\n')
            display_basket()
            itemname = input(
                'enter item name to remove the item from the basket : ')
            if check_item(itemname):
                print('entered item is present in the market,')
                ch4 = input(
                    'confirmation for removal of item from the basket : (ok/no) ')
                if ch4 == 'ok':
                    cur.execute(
                        "select sum(qty) from customer group by product_name having product_name = '{}' ".format(itemname))
                    data3 = cur.fetchall()

                    cur.execute(
                        "delete from customer where product_name = '{}'".format(itemname))
                    x.commit()
                    print('item removed succesfully')

                    cur.execute(
                        "update product set qty=qty+{} where name='{}'".format(data3[0][0], itemname))
                    x.commit()
                    print('item returned to the market...\n')
                    print('returning home....')

                else:
                    print('operation terminated')
                    print('returning home....')
                    continue
            else:
                print(
                    'the entered item is not avaliable in the basket please enter valid name...')
                print('returning home....')
                continue

        elif ch == 4:
            display_basket()

        elif ch == 5:
            print('generating the bill............')
            cur.execute("select sum(amount) from customer")
            data5 = cur.fetchall()
            print(data5[0][0])

        elif ch == 6:
            print('--------leaving the market🛒--------')
            break

        elif ch == 7:
            name = input('please kindly provide your name😌: ')
            review = input('enter your feed-back here 👇 : [max(150) words]\n')
            cur.execute(
                "insert into feedback values('{}','{}')".format(name, review))
            x.commit()
            print('your feedback has been noted')
            print('thank you for the feedback visit again.🙏')
            print('\n')
            print('returning home.......')
            continue

        elif ch == 8:
            # password is fullmetal
            while True:
                password = input('enter password to access : ')
                if password == 'fullmetal':
                    print('correct password✔')
                    print('now you can add items to the market')
                    print('already existing items in the market are : ')
                    display_items()
                    item_id = int(
                        input('enter item id to be added in the market : '))
                    item_name = input(
                        'enter item name to be added in the market : ')
                    qty = int(input('enter the quantity of item to be added'))
                    pricePerItem = float(input('enter the cost per item : '))
                    query = "insert into product values({},'{}',{},{})".format(
                        item_id, item_name, qty, pricePerItem)
                    cur.execute(query)
                    x.commit()
                    print('row added into the market successfully')
                    ch8 = input(
                        'do you want to add more items to your market?(y/n)')
                    if ch8 == 'n':
                        print('returning to the home page.......')
                        break
                    else:
                        continue
                else:
                    print('incorrect password...❌')
                    print('returning to the home page.......')
                    break

    else:
        print('invalid input!!!')
        print('try again....😟')
        break
