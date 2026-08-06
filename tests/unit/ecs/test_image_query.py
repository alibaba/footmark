#!/usr/bin/env python

from footmark.ecs.connection import ECSConnection
from footmark.ecs.image import Image
from footmark.ecs.keypair import KeyPair
from footmark.market.connection import MARKETConnection
from tests.compat import mock, unittest


class TestDescribeImagesPagination(unittest.TestCase):

    def setUp(self):
        self.connection = ECSConnection.__new__(ECSConnection)
        self.connection.build_request_params = mock.Mock(side_effect=lambda params: params)

    def test_uses_describe_images_action_and_collects_all_pages(self):
        first_page = [Image(), Image()]
        last_page = [Image()]
        self.connection.get_list_new = mock.Mock(side_effect=[first_page, last_page])

        result = self.connection.describe_images(page_size=2)

        self.assertEqual(result, first_page + last_page)
        actions = [call[0][0]['Action'] for call in self.connection.build_request_params.call_args_list]
        self.assertEqual(actions, ['DescribeImages', 'DescribeImages'])
        page_numbers = [call[0][0]['page_number'] for call in self.connection.build_request_params.call_args_list]
        self.assertEqual(page_numbers, ['1', '2'])

    def test_empty_page_returns_immediately(self):
        self.connection.get_list_new = mock.Mock(return_value=[])

        result = self.connection.describe_images(page_size=100)

        self.assertEqual(result, [])
        self.assertEqual(self.connection.get_list_new.call_count, 1)

    def test_rejects_invalid_page_size(self):
        self.connection.get_list_new = mock.Mock()

        with self.assertRaises(ValueError):
            self.connection.describe_images(page_size=0)

        with self.assertRaises(ValueError):
            self.connection.describe_images(page_size=101)

        self.assertEqual(self.connection.get_list_new.call_count, 0)


class TestDescribeProductsPagination(unittest.TestCase):

    def setUp(self):
        self.connection = MARKETConnection.__new__(MARKETConnection)
        self.connection.build_request_params = mock.Mock(side_effect=lambda params: params)

    def test_uses_describe_products_action_and_collects_all_pages(self):
        first_page = [object(), object()]
        last_page = [object()]
        self.connection.get_list_new = mock.Mock(side_effect=[first_page, last_page])

        result = self.connection.describe_products(page_size=2)

        self.assertEqual(result, first_page + last_page)
        actions = [call[0][0]['Action'] for call in self.connection.build_request_params.call_args_list]
        self.assertEqual(actions, ['DescribeProducts', 'DescribeProducts'])


class TestTaggedObjects(unittest.TestCase):

    def test_image_accepts_normalized_tag_fields(self):
        image = Image()

        image.tags = {'tag': [{'tag_key': 'Environment', 'tag_value': 'production'}]}

        self.assertEqual(image.tags, {'Environment': 'production'})

    def test_key_pair_accepts_normalized_and_api_tag_fields(self):
        key_pair = KeyPair()

        key_pair.tags = {'tag': [
            {'tag_key': 'Environment', 'tag_value': 'production'},
            {'TagKey': 'Owner', 'TagValue': 'platform'},
        ]}

        self.assertEqual(key_pair.tags, {
            'Environment': 'production',
            'Owner': 'platform',
        })


if __name__ == '__main__':
    unittest.main()
