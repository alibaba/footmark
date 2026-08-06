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

    def test_caps_market_page_size_to_endpoint_limit(self):
        first_page = [object()] * 50
        second_page = [object()] * 50
        last_page = [object()] * 5
        self.connection.get_list_new = mock.Mock(side_effect=[first_page, second_page, last_page])

        result = self.connection.describe_products(page_size=100)

        self.assertEqual(result, first_page + second_page + last_page)
        page_sizes = [call[0][0]['page_size'] for call in self.connection.build_request_params.call_args_list]
        self.assertEqual(page_sizes, ['50', '50', '50'])


class TestTaggedObjects(unittest.TestCase):

    def test_builds_dotted_ecs_tag_query_parameters(self):
        connection = ECSConnection.__new__(ECSConnection)
        params = {}

        connection.build_tags_params(params, {'ManagedBy': 'Ansible'}, 20)

        self.assertEqual(params, {
            'set_Tag.1.Key': 'ManagedBy',
            'set_Tag.1.Value': 'Ansible',
        })

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


class TestKeyPairDeletion(unittest.TestCase):

    def setUp(self):
        self.connection = ECSConnection.__new__(ECSConnection)
        self.connection.build_request_params = mock.Mock(side_effect=lambda params: params)
        self.connection.get_status_new = mock.Mock(return_value=True)
        self.connection.describe_key_pairs = mock.Mock(return_value=[])

    def test_uses_plural_ecs_delete_action_and_checks_each_name(self):
        result = self.connection.delete_key_pair(key_pair_names=['test-key'])

        self.assertTrue(result)
        self.assertEqual(
            self.connection.build_request_params.call_args[0][0]['Action'],
            'DeleteKeyPairs'
        )
        self.connection.describe_key_pairs.assert_called_once_with(key_pair_name='test-key')


class TestKeyPairTags(unittest.TestCase):

    def setUp(self):
        self.connection = mock.Mock()
        self.key_pair = KeyPair(connection=self.connection)
        self.key_pair.name = 'test-key'

    def test_uses_key_pair_name_as_tag_resource_id(self):
        self.key_pair.add_tags({'Environment': 'test'})
        self.key_pair.remove_tags({'Environment': 'test'})

        self.connection.tag_resources.assert_called_once_with(
            resource_ids=['test-key'], resource_type='keypair', tags={'Environment': 'test'}
        )
        self.connection.untag_resources.assert_called_once_with(
            resource_ids=['test-key'], resource_type='keypair', tags={'Environment': 'test'}
        )


class TestRunInstancesRequestFormatting(unittest.TestCase):

    def test_keeps_data_disks_as_sdk_repeat_list(self):
        connection = ECSConnection.__new__(ECSConnection)
        data_disks = [{'Category': 'cloud_essd', 'Size': 40, 'Encrypted': True}]

        formatted = connection.format_request_kwargs(data_disks=data_disks)

        self.assertEqual(formatted['data_disks'], data_disks)

    def test_maps_system_disk_encryption_struct_to_sdk_setter(self):
        connection = ECSConnection.__new__(ECSConnection)
        connection.product = 'aliyunsdkecs.request.v20140526'

        params = connection.build_request_params({
            'Action': 'RunInstances',
            'system_disk': {
                'Encrypted': True,
                'KMSKeyId': 'kms-test',
            },
        })

        self.assertEqual(params['set_SystemDisk'], {
            'Encrypted': True,
            'KMSKeyId': 'kms-test',
        })


class TestImageWait(unittest.TestCase):

    def test_returns_as_soon_as_image_is_available(self):
        connection = ECSConnection.__new__(ECSConnection)
        image = Image()
        image.status = 'Available'
        connection.describe_images = mock.Mock(return_value=[image])

        with mock.patch('footmark.ecs.connection.time.sleep') as sleep:
            self.assertTrue(connection.wait_for_image_status('m-test', 'Available'))

        connection.describe_images.assert_called_once_with(image_id='m-test', status='ALL')
        sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()
