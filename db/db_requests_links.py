from db.db_utils import get_connexion


def get_all_links():
    """
    Get the links.
    :return:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        SELECT * FROM Links
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def click_link(customer_number, link_id):
    """
    Handle a customer clicking on a link.
    :param customer_number:
    :param link_id:
    :return: True if the link was clicked, False otherwise.
    """
    with get_connexion() as cursor:
        # Test if already clicked
        query = """
        SELECT 1 FROM LinksCustomer WHERE customer_number = :customer_number AND idLink = :link_id;
        """
        cursor.execute(query, {"customer_number": customer_number, "link_id": link_id})
        result = cursor.fetchone()
        if result:
            return False

        query = """
        INSERT INTO LinksCustomer (customer_number, idLink)
        VALUES (:customer_number, :link_id)
        """
        cursor.execute(query, {"customer_number": customer_number, "link_id": link_id})

        set_customer_games_to_use(customer_number, get_games_to_use(customer_number)+1)
        return True

def get_links_customer(phone):
    """
    Get the links of a customer.
    :param phone:
    :return: All links and the links of the customer.
    """
    links = get_all_links()
    with get_connexion() as cursor:
        query = """
        SELECT link_id
        FROM Customer_Links 
        WHERE customer_number = :customer_number;
        """
        cursor.execute(query, {"customer_number": phone})
        result = cursor.fetchall()
        return links, result


def create_link(name, link):
    """
    Create a link.
    :param name:
    :param link:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        INSERT INTO Links (name, url)
        VALUES (:name, :link)
        """
        cursor.execute(query, {"name": name, "link": link})
        return True


def delete_link(ident):
    """
    Delete a link.
    :param ident:
    :return:
    """
    with get_connexion() as cursor:
        query = """
        DELETE FROM Links
        WHERE id = :ident;
        """
        cursor.execute(query, {"ident": ident})
        return True
