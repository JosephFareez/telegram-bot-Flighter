import unittest
from unittest.mock import patch, MagicMock, Mock
from telebot.types import Message
from handlers.custom_handlers import (
    search_low_price,
    search_month,
    search_non_stop_tickets,
)

class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.message = Mock()
        self.message.from_user.id = 123

    @patch('loader.bot.send_message')
    @patch('database.city_finder.find_country_code')
    @patch('database.history_db.db_create')
    def test_search_low_price_handler(self, mock_db_create, mock_find_country_code, mock_send_message):
        # Set up mocks
        mock_find_country_code.return_value = 'mocked_country_code'
        message = MagicMock(spec=Message)

        # Call the handler
        search_low_price._search_low_price(message)

        # Assert the expected calls to mocked functions
        mock_send_message.assert_called_once_with(
            message.chat.id,
            "*Введите город вылета: *",
            parse_mode="Markdown"
        )
        mock_find_country_code.assert_called_once_with(message)
        mock_db_create.assert_called_once_with(
            message.chat.id, message.text
        )

    @patch('loader.bot.send_message')
    @patch('database.city_finder.find_country_code')
    @patch('database.history_db.db_create')
    def test_search_month_handler(self, mock_db_create, mock_find_country_code, mock_send_message):
        # Set up mocks
        mock_find_country_code.return_value = 'mocked_country_code'
        message = MagicMock(spec=Message)

        # Call the handler
        search_month._search_month(message)

        # Assert the expected calls to mocked functions
        mock_send_message.assert_called_once_with(
            message.chat.id,
            "*Введите город вылета: *",
            parse_mode="Markdown"
        )
        mock_find_country_code.assert_called_once_with(message)
        mock_db_create.assert_called_once_with(
            message.chat.id, message.text
        )

    @patch('loader.bot.send_message')
    @patch('database.city_finder.find_country_code')
    @patch('database.history_db.db_create')
    def test_search_non_stop_tickets_handler(self, mock_db_create, mock_find_country_code, mock_send_message):
        # Set up mocks
        mock_find_country_code.return_value = 'mocked_country_code'
        message = MagicMock(spec=Message)

        # Call the handler
        search_non_stop_tickets._search_non_stop_ticket(message)

        # Assert the expected calls to mocked functions
        mock_send_message.assert_called_once_with(
            message.chat.id,
            "*Введите город вылета: *",
            parse_mode="Markdown"
        )
        mock_find_country_code.assert_called_once_with(message)
        mock_db_create.assert_called_once_with(
            message.chat.id, message.text
        )

if __name__ == '__main__':
    unittest.main()
