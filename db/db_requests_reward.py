from db.db_utils import get_connexion
from db.parameters import WORKED_DELTA_TIME


def use_reward(reward_id):
    with get_connexion() as cursor:

        query = """
            UPDATE Customer_Reward
            SET date_used = CURRENT_TIMESTAMP,
                worked = CASE 
                    WHEN (strftime('%s', CURRENT_TIMESTAMP) - strftime('%s', date)) < :delta_time THEN 1
                    ELSE 0
                END
            WHERE id = :reward_id;
        """

        cursor.execute(query, {"reward_id": reward_id, "delta_time": WORKED_DELTA_TIME})


def get_customer_rewards_stats(customer_number):
    """
    Get the rewards stats for a customer
    :param customer_number: The customer number
    :return: a list of tuples (reward_id, reward_label, reward_count, reward_worked_percentage)
    """
    with get_connexion() as cursor:

        query = """
            SELECT r.id AS reward_id,
                r.label as reward_label,
                COUNT(cr.reward_id) as reward_count,
                1.0 * SUM(CASE WHEN cr.worked = 1 THEN 1 ELSE 0 END) / COUNT(cr.reward_id) as reward_worked_percentage
            FROM Reward r
            JOIN Customer_Reward cr on r.id = cr.reward_id
            JOIN Customer c on cr.customer_number = c.number
            WHERE c.number = :customer_number
            GROUP BY r.id;
        """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchall()
        return result


def get_list_reward(customer_number=None):
    """
    Get the list of rewards that a customer can claim.
    :param customer_number: The customer number
    :return: a list of tuples (label, value) representing the rewards.
    """
    with get_connexion() as cursor:
        if customer_number is None:
            query = """
            SELECT label, value, id
            FROM Reward;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        else:
            query = """
            SELECT label, value, id
            FROM Reward 
            WHERE level_required <= (
                SELECT total_points
                FROM Customer
                WHERE number = :customer_number
            );
            """

        cursor.execute(query, {"customer_number": customer_number})
        result = cursor.fetchall()
        return result


def get_global_rewards_stats():
    with get_connexion() as cursor:

        query = """
            SELECT r.id as reward_id,
            r.label as reward_label,
            COUNT(cr.reward_id) as reward_count,
            1.0 * SUM(CASE WHEN cr.worked = 1 THEN 1 ELSE 0 END) / COUNT(cr.reward_id) as reward_worked_percentage
            FROM Reward r
            JOIN Customer_Reward cr on r.id = cr.reward_id 
            GROUP BY r.id;
        """

        cursor.execute(query)
        result = cursor.fetchall()
        return result


def create_reward(reward):
    """
    Create a reward.
    :param reward:
    :return:
    """
    with get_connexion() as cursor:
            query = """
                INSERT INTO Reward (label)
                VALUES (:reward);
            """

            cursor.execute(query, {"reward": reward})



def delete_reward(ident):
    """
    Delete a reward.
    :param reward:
    :return:
    """
    with get_connexion() as cursor:
        query = """
            DELETE FROM Reward
            WHERE id = :id;
        """

        cursor.execute(query, {"id": ident})


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


if __name__ == "__main__":
    customer_number = '+33 6 12 34 56 78'
    reward_id = 1
    print(get_global_rewards_stats())
    # TODO user_reward test