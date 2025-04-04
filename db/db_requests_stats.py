from datetime import datetime, timedelta
from db.db_utils import get_connexion


def count_visit_rate_last_100_days(customer_number):
    """
    Count the number of days a customer has visited the store in the last 100 days.
    :param customer_number:
    :return: an integer representing the number of days.
    """
    with get_connexion() as cursor:
        date_limit = datetime.now() - timedelta(days=100)
        date_limit_str = date_limit.strftime("%Y-%m-%d")

        query = """
        SELECT COUNT(DISTINCT DATE(date))
        FROM Orders
        WHERE customer_number = ? AND date >= ?;
        """

        cursor.execute(query, (customer_number, date_limit_str))
        result = cursor.fetchone()
        return result[0]


def count_visit_rate_last_100_days_in_part(customer_number, part_of_day):
    """
    Count the number of days a customer has visited the store in the last 100 days in a specific part of the day.
    :param customer_number:
    :param part_of_day: 0 for morning, 1 for noon, 2 for evening
    :return: an integer representing the number of days.
    """
    with get_connexion() as cursor:

        date_limit = datetime.now() - timedelta(days=100)
        date_limit_str = date_limit.strftime("%Y-%m-%d")

        query = """
        SELECT COUNT(DISTINCT DATE(date))
        FROM Orders
        WHERE customer_number = ?  AND date >= ? AND part_of_day = ?;
        """

        cursor.execute(query, (customer_number, date_limit_str, part_of_day))
        result = cursor.fetchone()
        return result[0]

def count_morning_visit_rate_last_100_days(customer_number):
    """
    Count the number of days a customer has visited the store in the last 100 days in the morning.
    :param customer_number:
    :return:
    """
    return count_visit_rate_last_100_days_in_part(customer_number, 0)

def count_noon_visit_rate_last_100_days(customer_number):
    """
    Count the number of days a customer has visited the store in the last 100 days at noon.
    :param customer_number:
    :return:
    """
    return count_visit_rate_last_100_days_in_part(customer_number, 1)

def count_evening_visit_rate_last_100_days(customer_number):
    """
    Count the number of days a customer has visited the store in the last 100 days in the evening.
    :param customer_number:
    :return:
    """
    return count_visit_rate_last_100_days_in_part(customer_number, 2)


def notif_succes_rate_in_last_100_days(customer_number):
    """
    Get the success rate of notifications in the last 100 days.
    :param customer_number:
    :return:
    """
    with get_connexion() as cursor:

        query1 = """
        SELECT COUNT(*) 
        FROM Notification n
        JOIN Orders o
            ON n.customer_number = o.customer_number
            AND o.date BETWEEN n.date AND DATETIME(n.date, '+24 hours')
        WHERE n.customer_number = :customer_number
        AND n.date >= DATETIME('now', '-100 days');
        """

        query2 = """
        SELECT COUNT(*)
        FROM Notification
        WHERE customer_number = :customer_number
        AND date >= DATETIME('now', '-100 days');
        """

        cursor.execute(query1, {"customer_number": customer_number})
        nb_notifs_succes = cursor.fetchone()[0]

        cursor.execute(query2, {"customer_number": customer_number})
        nb_notifs = cursor.fetchone()[0]

        if nb_notifs == 0:
            return -1
        return nb_notifs_succes/nb_notifs

