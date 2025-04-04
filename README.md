# Hackathon IAMD 


---

## Project Structure

### `app.py` 📄
The main entry point of the project. It initializes the Flask application and defines the API routes.

### `flask_resources/` 📂
Contains all resources required for the Flask application:

- **`static/`** 📂: Includes static assets such as CSS, JavaScript, and fonts.
- **`templates/`** 📂: Contains HTML templates for rendering the web interface.

### `db/` 📂
Handles the database schema, connections, and queries. Key files:

- **`db_init.py`** 📄: Initializes the database by executing all `.sql` files in this directory.
- **`creation_table.sql`** 📄: Defines the schema for the database tables.
- **`insert_data.sql`** 📄: Inserts test data into the tables for initial use.
- **`db_utils.py`** 📄: Implements a class for managing the database connection.
- **`db_requests_X.py`** 📄: Contains database queries specific to different components of the app.
- **`database.sqlite`** 📄: The SQLite database file, created when `db_init.py` is run for the first time.

### `data_generation/` 📂
Scripts for generating data to populate the database and train models. These were not used during the project as they were deemed unnecessary for the final implementation.

### `q_learning/` 📂
Scripts for implementing and using a deep Q-learning model:

- **`q_learning.py 📄`**: Handles training of the Q-learning model.
- **`customer_simulation.py 📄`**: Simulates customer behavior to provide input for the model.
- **`evaluate.py 📄`**: Evaluates the performance of the model.
- **`model.keras 📄`**: The trained Deep Q-learning model.

---

## How to Run the Project

### 1. Initialize the Database
Follow these steps to set up the database (this step is optional, it is done automatically when the app is run for the first time)

1. Navigate to the `db/` directory.
2. Run `db_init.py ` to create the database and populate it with initial test data:
   ```bash
   python db/db_init.py
    ```
3. Verify that the `database.sqlite` file has been created in the `db/` directory.

### 2. Run the Flask Application

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   
2. Run the Flask application:
   ```bash
    python app.py
    ```
   
3. Open a web browser and navigate to `http://127.0.0.1:5000` to access the web interface.
4. Use the web interface to interact with the application.
5. To stop the Flask application, press `Ctrl+C` in the terminal.

---

## Contributors

- [Jérémi Mentec]()
- [Arthur Cappellina]()
- [Paul Deveaux]()

