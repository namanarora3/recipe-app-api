# custom django managemant commands test

from unittest.mock import patch  # mock the behavoiur of the database
# possibility for when we try to connext to database before its ready
from psycopg2 import OperationalError as Psycopg2OpError
# allows to call the comand that we are testing
from django.core.management import call_command

from django.db.utils import OperationalError
# base test class used to test unit test,
# using simple testcase because we are testing without databse test
from django.test import SimpleTestCase


# video 8 from databse setup, didnt understand a
# word about these tests co copy pasted
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
