import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pandeyji_eatery"
)
def total_price_per_order(order_id):
     cursor = cnx.cursor()

     query = f"SELECT get_total_order_price({order_id})"
     cursor.execute(query)

     result = cursor.fetchone()[0]

     cursor.close()
     return result
def insert_order_iterm(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        #calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        #commiting the changes
        cnx.commit()

        cursor.close()

        print("Order item inserted successfully")

        cnx.rollback()

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        cnx.rollback()
        return -1

def get_next_order_id():
    cursor = cnx.cursor()

    query = "select max(order_id) from orders"
    cursor.execute(query)

    #fetching the result
    result = cursor.fetchone()[0]

    cursor.close()

    if result is None:
        return 1
    else:
        return result+1


def get_order_status(order_id):
    cursor = cnx.cursor()
    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None