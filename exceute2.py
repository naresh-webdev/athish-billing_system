import mysql.connector as ms


x = ms.connect(host='localhost', user='root',
               passwd='Naresh@2004', database='athish_new')
cur = x.cursor(buffered=True)

try:

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

    def display_items_admin():
        cur.execute('select * from product')
        data = cur.fetchall()
        print('(id, name, qty, price per item )')
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

    def check_item_market(itemname):
        itempresent=0
        cur.execute('select distinct name from product')
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
                    cur.execute(
                        'select id,name,qty,price_per_item from product')
                    data = cur.fetchall()
                    for i in data:
                        print(i)
                    print('\n')
                    item_id = input(
                        'select item id to add item to the basket : ')
                    no_itemsadded = int(
                        input('enter the qty of items to be added to the basket : '))

                    cur.execute(
                        'select qty from product where id={}'.format(item_id))
                    data2 = cur.fetchall()
                    leng = data2[0][0]
                    if leng < no_itemsadded:
                        print('the select qty is more than the availabe qty 😟😟😟')
                        ch1 = input('want to add any other items ? (y/n) : ')
                        if ch1 == 'n':
                            boolean = 0
                            break
                    else:
                        print('selected item is available in the market ✔')

                        cur.execute(
                            'select price_per_item,name from product where id={}'.format(item_id))
                        data2 = cur.fetchone()
                        pu, cname = data2[0], data2[1]
                        cost = pu * no_itemsadded
                        cur.execute("insert into customer values('{}',{},{})".format(
                            cname, no_itemsadded, cost))
                        print('\n item added succesfully😊')

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
                review = input(
                    'enter your feed-back here 👇 : [max(150) words]\n')
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
                password = input('enter password to access : ')
                if password == 'fullmetal':
                    print('correct password✔')
                    print(
                        'now you can perform two options to chose from admin privilliges')
                    while True:
                        print(
                            '1.add new item to the table')
                        print('2.update items in the table')
                        print('3.retun item to the market')
                        print('4.remove item from the market')
                        ch8 = int(input('enter your choice : '))
                        if ch8 in [1, 2,3,4]:
                            if ch8 == 1:
                                print('already existing items in the market are : ')
                                display_items_admin()
                                item_id = int(
                                    input('enter item id to be added in the market : '))
                                item_name = input(
                                    'enter item name to be added in the market : ')
                                qty = int(
                                    input('enter the quantity of item to be added : '))
                                pricePerItem = float(
                                    input('enter the cost per item : '))
                                query = "insert into product values({},'{}',{},{})".format(
                                    item_id, item_name, qty, pricePerItem)
                                cur.execute(query)
                                x.commit()
                                print('row added into the market successfully')
                            elif ch8 == 2:
                                print('already existing items in the market are : ')
                                display_items_admin()
                                item_id_to_update = int(
                                    input('enter the item id to update the item id in market : '))
                                cur.execute('select id from product')
                                data8 = cur.fetchall()
                                list8 = []
                                for k in data8:
                                    list8.append(k[0])
                                if item_id_to_update in list8:
                                    print(
                                        'item is available in the market you can now perform update option.')
                                    qty_to_update = int(
                                        input('enter the new item qty be replace for the old one : '))
                                    cur.execute('update product set qty = {} where id={}'.format(
                                        qty_to_update, item_id_to_update))
                                print('item added successfully. ')
                            elif ch8 == 3:
                                print('---return back the product into the market--')
                                return_id = int(input('enter item id to be returned : '))
                                return_name = input('enter item name : ')
                                return_qty = int(input('enter qty : '))
                                cur.execute("insert into remove_items values({},'{}',{})".format(return_id,return_name,return_qty))
                                x.commit()
                                print('item added successfully')
                            elif ch8 == 4:
                                print("--removing an item from the market--")
                                remove_name = input('enter name of the item to remove from the market : ')
                                if check_item_market(remove_name):
                                  cur.execute("delete from product where name='{}' ".format(remove_name))
                                  x.commit()
                                  print('item removed from the market successfully')
                                else :
                                  print('the entered item is not present in the market')
                                  print('try again')
                                                
                            else:
                              
                                print('invalid input.. ')
                                break

                        ch81 = input(
                            'do you want to add more items to your market?(y/n)')
                        if ch81 == 'n':
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




finally:
    print('The progarm ended.....')
