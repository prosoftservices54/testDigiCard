from db.db_utils import get_connexion


def has_at_least_one_link(customer_number):
    """
    Check if a customer has at least one link.
    :param customer_number: The customer number
    :return: True if the customer has at least one link, False otherwise.
    """
    with get_connexion() as cursor:

        query = '''
            SELECT 
                EXISTS (
                    SELECT 1
                    FROM Customer
                    JOIN Customer_Links ON Customer.number = Customer_Links.customer_number
                    WHERE Customer.number = :customer_number 
                ) AS has_games_to_use;
        '''

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()[0]
        return result == 1


def play_game_if_available(customer_number):
    """
    Handle a customer playing a game.
    :param customer_number: The customer number
    :return: True if the customer can play, False otherwise.
    """
    with get_connexion() as cursor:

        query = '''
            UPDATE Customer
            SET games_to_use = games_to_use - 1
            WHERE number = :customer_number AND games_to_use > 0;
        '''

        cursor.execute(query, {"customer_number": customer_number})

        if cursor.rowcount == 0 or not has_at_least_one_link(customer_number):
            return False

        return True


def get_games_to_use(customer_number):
    """
    Get the number of games that a customer can play.
    :param customer_number: The customer number
    :return: The number of games that a customer can play.
    """
    with get_connexion() as cursor:

        query = '''
            SELECT games_to_use
            FROM Customer
            WHERE number = :customer_number;
        '''

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchone()
        return result[0]


if __name__ == "__main__":
    print(play_game_if_available('+33 6 12 34 56 78'))
    print(has_at_least_one_link('+33 6 12 34 56 78'))
