import mysql.connector
import yaml
from mollie.api.client import Client

# Load configuration from YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connect to MySQL database
db = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database'],
    port=config['mysql']['port']
)
cursor = db.cursor()

# Connect to Mollie API
mollie = Client()
mollie.set_api_key(config['mollie']['api_key'])

# Get users from MySQL database
query = "SELECT first_name, last_name, email, customer_id FROM users where customer_id IS NOT NULL"
cursor.execute(query)
users = cursor.fetchall()

# Update users in Mollie API
for user in users:
    customer_id = user[3]
    print(f"{user[0]} {user[1]}")
    mollie_customer = mollie.customers.update(customer_id, {
        "name": f"{user[0]} {user[1]}",
        "email": user[2]
    })

# Close database connection
db.close()
