from db.db_utils import get_connexion

def find_lvl(points):
    """
    Find the level of a customer based on their points.
    :param points:
    :return:
    """
    niveau = 0
    for i in range(1,11):
        points -= i
        if points >= 0:
            niveau += 1
        else :
            return niveau
    return niveau + points//10

def get_rewards_gained_by_customer(customer_number):
    """
    Get the rewards gained by a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:
        query = """
            SELECT r.label
            FROM Reward r
            JOIN Customer_Reward cr on r.id = cr.reward_id
            WHERE cr.customer_number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchall()
        return result

def add_points_to_customer(customer_number, points):
    """
    Add points to a customer.
    :param customer_number:
    :param points:
    :return:
    """
    total_points = get_customer_total_points(customer_number)
    level = get_customer_level(customer_number)
    new_lvl = find_lvl(total_points+points)
    games_to_use = get_games_to_use(customer_number) + new_lvl - level
    print(customer_number, points)
    print(total_points, level, games_to_use)
    set_customer_total_points(customer_number, total_points+points)
    set_customer_level(customer_number, new_lvl)
    set_customer_games_to_use(customer_number, games_to_use)

def add_order(customer_number):
    """
    Add an order to a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        INSERT INTO Orders (id, customer_number, date)
        VALUES (:id, :customer_number, CURRENT_TIMESTAMP);
        """

        cursor.execute(query, {"customer_number": customer_number, "id": generate_id()})

def generate_id():
    """
    Generate an id.
    :return:
    """
    with get_connexion() as cursor:
        query = """
        SELECT MAX(id) + 1
        FROM Orders;
        """

        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

def get_nb_orders(customer_number):
    """
    Get the number of orders of a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        SELECT COUNT(*)
        FROM Orders
        WHERE customer_number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()
        return result[0]


def get_user_role(customer_number):
    """
    Get the role of a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        SELECT role
        FROM Customer
        WHERE number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()
        return result[0]


def get_customer_level(customer_number):
    """
    Get the level of a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        SELECT level
        FROM Customer
        WHERE number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()
        return result[0]
    
def add_reward_to_customer(customer_number, reward_id):
    """
    Add a reward to a customer.
    :param customer_number:
    :param reward_id:
    :return:
    """
    with get_connexion() as cursor:
        query = """
            INSERT INTO Customer_Reward (customer_number, reward_id, date)
            VALUES (:customer_number, :reward_id, CURRENT_TIMESTAMP);
        """

        cursor.execute(query, {"customer_number": customer_number, "reward_id": reward_id})

def get_games_to_use(customer_number):
    """
    Get the level of a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        SELECT games_to_use
        FROM Customer
        WHERE number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()

        return result[0]
    
def validate_review(user, link_id):
    """
    Validate a review.
    :param user:
    :param link_id:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        INSERT INTO Customer_Links (customer_number, link_id)
        VALUES (:customer_number, :link_id);
        """

        cursor.execute(query, {"customer_number": user, "link_id": link_id})

def get_customer_total_points(customer_number):
    """
    Get the level of a customer.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:

        query = """
        SELECT total_points
        FROM Customer
        WHERE number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()
        return result[0]

def set_customer_level(customer_number, level):
    """
    Set the level of a customer.
    :param customer_number:
    :param level:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        UPDATE customer
        SET level = ?
        WHERE number = ?
        """

        cursor.execute(query, (level, customer_number))



def set_customer_total_points(customer_number, total_points):
    """
    Set the total points of a customer.
    :param customer_number:
    :param total_points:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        UPDATE Customer
        SET total_points = ?
        WHERE number = ?
        """

        cursor.execute(query, (total_points, customer_number))


def set_customer_games_to_use(customer_number, games_to_use):
    """
    Set the games to use of a customer.
    :param customer_number:
    :param games_to_use:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        UPDATE Customer
        SET games_to_use = ?
        WHERE number = ?
        """

        cursor.execute(query, (games_to_use, customer_number))



def list_customers():
    """
    List all Customer.
    :return:
    """
    with get_connexion() as cursor:

        query = """
        SELECT * FROM Customer;
        """

        cursor.execute(query)
        result = cursor.fetchall()
        return result


def remove_customer(customer_number):
    """
    Remove a customer
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:

        query = """
        DELETE FROM Customer
        WHERE number = :customer_number;
        """

        cursor.execute(query, {"customer_number": customer_number})


def get_lvl(data):
    """
    Get the level of a customer.
    :param data:
    :return:
    """
    with get_connexion() as cursor:
        phone = data['numero']
        sql = '''
            SELECT total_points FROM Customer WHERE number = ?
        '''
        cursor.execute(sql, (phone))
        result = cursor.fetchone()
        return int(result[0])
