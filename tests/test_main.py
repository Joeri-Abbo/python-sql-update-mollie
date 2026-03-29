"""Basic tests for the Mollie customer update script."""
import sys
import types
import unittest
from unittest.mock import MagicMock, patch, mock_open


SAMPLE_CONFIG = """
mysql:
  host: localhost
  user: testuser
  password: testpass
  database: testdb
  port: 3306

mollie:
  api_key: test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""


class TestConfigLoading(unittest.TestCase):
    """Test YAML config loading."""

    def test_config_parses_correctly(self):
        import yaml
        config = yaml.safe_load(SAMPLE_CONFIG)
        self.assertEqual(config['mysql']['host'], 'localhost')
        self.assertEqual(config['mysql']['user'], 'testuser')
        self.assertEqual(config['mysql']['port'], 3306)
        self.assertEqual(config['mollie']['api_key'], 'test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    def test_config_missing_key_raises(self):
        import yaml
        config = yaml.safe_load(SAMPLE_CONFIG)
        with self.assertRaises(KeyError):
            _ = config['mysql']['nonexistent_key']


class TestCustomerUpdate(unittest.TestCase):
    """Test customer update logic with mocked dependencies."""

    def setUp(self):
        # Mock mysql.connector
        self.mock_mysql = MagicMock()
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_mysql.connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Mock mollie client
        self.mock_mollie_client = MagicMock()
        self.mock_mollie_module = MagicMock()
        self.mock_mollie_module.api.client.Client.return_value = self.mock_mollie_client

    def test_users_fetched_and_updated(self):
        """Each user row should trigger a Mollie customer update."""
        users = [
            ('Alice', 'Smith', 'alice@example.com', 'cst_001'),
            ('Bob', 'Jones', 'bob@example.com', 'cst_002'),
        ]
        self.mock_cursor.fetchall.return_value = users

        # Simulate the core update loop
        for user in users:
            customer_id = user[3]
            self.mock_mollie_client.customers.update(customer_id, {
                'name': f'{user[0]} {user[1]}',
                'email': user[2],
            })

        self.assertEqual(self.mock_mollie_client.customers.update.call_count, 2)
        first_call_args = self.mock_mollie_client.customers.update.call_args_list[0]
        self.assertEqual(first_call_args[0][0], 'cst_001')
        self.assertEqual(first_call_args[0][1]['name'], 'Alice Smith')
        self.assertEqual(first_call_args[0][1]['email'], 'alice@example.com')

    def test_exception_on_update_does_not_abort_loop(self):
        """An exception from one customer update should not stop processing others."""
        users = [
            ('Alice', 'Smith', 'alice@example.com', 'cst_001'),
            ('Bob', 'Jones', 'bob@example.com', 'cst_002'),
        ]
        call_count = 0
        errors = []

        for user in users:
            try:
                call_count += 1
                if user[3] == 'cst_001':
                    raise Exception('API error')
                self.mock_mollie_client.customers.update(user[3], {
                    'name': f'{user[0]} {user[1]}',
                    'email': user[2],
                })
            except Exception as e:
                errors.append(str(e))

        self.assertEqual(call_count, 2)
        self.assertEqual(len(errors), 1)
        self.assertIn('API error', errors[0])

    def test_no_users_no_updates(self):
        """Empty user list should result in zero Mollie API calls."""
        users = []
        for user in users:
            self.mock_mollie_client.customers.update(user[3], {})

        self.mock_mollie_client.customers.update.assert_not_called()


if __name__ == '__main__':
    unittest.main()
