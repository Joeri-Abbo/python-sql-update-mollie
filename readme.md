## Update Mollie Customers from MySQL Database

This Python script retrieves user information from a MySQL database and updates their corresponding Mollie customers
with their new name and email.

### Setup

- Install the necessary packages by running pip install -r requirements.txt.
- Create a new YAML configuration file called config.yaml in the same directory as the script.
- Update the config.yaml file with your MySQL database and Mollie API credentials.
- Make sure your MySQL database contains a table called users with columns first_name, last_name, email, and
  customer_id.

### Usage

To run the script, simply execute python update_customers.py in your terminal. The script will connect to the MySQL
database and Mollie API, retrieve the users from the users table, and update their corresponding Mollie customers with
their new name and email.

### Configuration

The config.yaml file should contain the following structure:

```yaml
mysql:
  host: localhost
  user: yourusername
  password: yourpassword
  database: yourdatabase

mollie:
  api_key: test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Replace the placeholders with your own credentials for your MySQL database and Mollie API. The api_key value for Mollie
should be a test API key for development purposes.

### Dependencies

This script uses the following Python packages:

- mysql-connector-python to connect to the MySQL database.
- mollie-api-python to connect to the Mollie API.
- pyyaml to parse the config.yaml file.
- You can install these packages by running pip install -r requirements.txt.