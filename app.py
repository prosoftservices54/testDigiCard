from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

from db.db_requests_reward import get_list_reward
from db.db_requests_customer import *
from db.db_requests_links import get_all_links, get_links_customer, create_link, delete_link, click_link
from db.db_requests_reward import create_reward, delete_reward

app = Flask(__name__, static_folder='flask_resources/static', template_folder='flask_resources/templates')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/delete', methods=['POST'])
def debug():
    data = request.get_json()
    print("debug :", data)
    delete_reward(data["id"])
    return jsonify({
        "success": True,
    }), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    database = "db/database.sqlite"  # Nom du fichier de la base de données SQLite
    conn = sqlite3.connect(database)
    identifier = data['phone']
    password = data['password']
    """
    Permet à un utilisateur de se connecter.
    :param conn: La connexion à la base de données.
    :param identifier: Email ou numéro saisi par l'utilisateur.
    :param password: Mot de passe saisi par l'utilisateur.
    :return: True si l'utilisateur est authentifié, False sinon.
    """
    sql = '''
    SELECT * FROM Customer 
    WHERE (email = ? OR number = ?) AND password = ?
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (identifier, identifier, password))
        result = cur.fetchone()
        print(result)
        # get visits
        visits = get_nb_orders(result[0])
        rewards = get_rewards_gained_by_customer(result[0])
        if result:
            print("Connexion réussie. Bienvenue !")
            return jsonify({"success": True, "message": "Login successful", "data": {"phone": result[0], "role": result[4], "visits": visits, "rewards": rewards, "games": get_games_to_use(result[0])}})
        else:
            print("Identifiants incorrects. Veuillez réessayer.")
            return jsonify({"success": False, "message": "Login failed"})
    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion : {e}")
        return False

@app.route('/customer/reward/add', methods=['POST'])
def add_reward():
    data = request.get_json()
    add_reward_to_customer(data["phone"], data["reward"])
    return jsonify({
        "success": True,
    }), 201


# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    database = "db/database.sqlite"  # Nom du fichier de la base de données SQLite
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    phone = data['phone']
    password = data['password']
    birthdate = data['birthdate']
    gender = data['gender']
    """
    Permet à un utilisateur de se connecter.
    :param conn: La connexion à la base de données.
    :param identifier: Email ou numéro saisi par l'utilisateur.
    :param password: Mot de passe saisi par l'utilisateur.
    :return: True si l'utilisateur est authentifié, False sinon.
    """
    sql = '''
        INSERT INTO Customer (number, password, gender, birth_date, creation_date) 
        VALUES (?, ?, ?, ?, DATE('now'))
    '''
    cur.execute(sql, (phone, password, gender, birthdate))

    # Sauvegarder les changements dans la base de données
    conn.commit()

    # Fermer la connexion
    conn.close()

    # Retourner une réponse de succès
    return jsonify({"success": True, "message": "Inscription réussie."}), 201

@app.route('/niveau', methods=['POST'])
def lvl_niveau():
    data = request.get_json()
    total_points = get_lvl(data)
    if total_points is None:
        print("Client non trouvé ou erreur dans la base de données.")
        return jsonify({"success": False, "message": "Prout"}), 201
    niveau = find_lvl(total_points)
    return jsonify({
        "success": True,
        "message": "Niveau calculé avec succès",
        "niveau": niveau
    }), 200

@app.route('/link/create', methods=['POST'])
def create_link_route():
    data = request.get_json()
    name, link = data['name'], data['link']
    create_link(name, link)
    return jsonify({
        "success": True
    }), 201

@app.route('/reward/create', methods=['POST'])
def create_reward_route():
    data = request.get_json()
    reward = data['reward']
    create_reward(reward)
    return jsonify({
        "success": True
    }), 201

@app.route('/link/delete', methods=['POST'])
def delete_link_route():
    data = request.get_json()
    ident = data['id']
    delete_link(ident)
    return jsonify({
        "success": True
    }), 201

@app.route('/reward/delete', methods=['POST'])
def delete_reward_route():
    data = request.get_json()
    print("datatata delete :", data)
    reward = data['reward']
    delete_reward(reward)
    return jsonify({
        "success": True
    }), 201

@app.route('/link/update', methods=['POST'])
def update_link_route():
    data = request.get_json()
    print("datatata :", data)
    if 'id' not in data or 'name' not in data or 'link' not in data:
        create_link(data['name'], data['link'])
    else:
        ident, name, link = data['id'], data['name'], data['link']
        delete_link(ident)
        create_link(name, link)
    return jsonify({
        "success": True
    }), 201

@app.route('/reward/update', methods=['POST'])
def update_reward_route():
    data = request.get_json()
    print("datatata :",data)
    if 'id' not in data or 'reward' not in data:
        create_reward(data['reward'])
    else:
        ident, reward = data['id'], data['reward']
        delete_reward(ident)
        create_reward(reward)
    return jsonify({
        "success": True
    }), 201

@app.route('/links', methods=['GET'])
def get_link_route():
    links = get_all_links()
    links_json = [{"id": row[0], "name": row[1], "link": row[2]} for row in links]
    return jsonify({
        "success": True,
        "links" : links_json
    }), 201

@app.route('/rewards', methods=['GET'])
def get_reward_route():
    rewards = get_list_reward()
    rewards_json = [{"reward": row[0], "id": row[2]} for row in rewards]
    return jsonify({
        "success": True,
        "rewards" : rewards_json
    }), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    all_customers = list_customers()
    customers_with_orders = []
    for customer in all_customers:
        orders = get_nb_orders(customer[0])
        customers_with_orders.append(customer + (orders,))
    customers_json = [{"phone": row[0], "birthDate": row[9], "gender": row[3], "visits": row[-1]} for row in customers_with_orders]
    return jsonify({
        "success": True,
        "clients" : customers_json
    }), 201

@app.route('/customer/links/<phone>', methods=['GET'])
def get_link_customer_route(phone):
    all_links, links = get_links_customer(phone)
    return jsonify({
        "success": True,
        "links" : links
    }), 201

@app.route('/review/validate', methods=['POST'])
def review_validate():
    data = request.get_json()
    user, link_id = data['user'], data['link_id']
    validate_review(user, link_id)
    return jsonify({
        "success": True
    }), 201

@app.route('/click', methods=['POST'])
def click():
    data = request.get_json()
    click_link(data["phone"], data["link_id"])
    return jsonify({
        "success": True,
    }), 201

@app.route('/visit/add', methods=['POST'])
def add_visit():
    data = request.get_json()
    print("data : ", data)
    add_points_to_customer(data["phone"], 1)
    add_order(data["phone"])
    return jsonify({
        "success": True,
    }), 201

@app.route('/customer/delete', methods=['POST'])
def customer_delete():
    data = request.get_json()
    remove_customer(data["phone"])
    return jsonify({
        "success": True,
    }), 201





# Run the Flask app with debug mode on
if __name__ == "__main__":
    app.run(debug=True)
