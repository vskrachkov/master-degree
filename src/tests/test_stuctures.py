from unittest import TestCase

from core import (
    structures as structs,
    exceptions as exc
)


class FlatNodeTestCase(TestCase):
    def test_load_and_dump(self):
        # check that dumped node loads well
        dumped_flat_node = 'some string'
        node = structs.FlatNode.load(dumped_flat_node)
        self.assertEqual(node.name, dumped_flat_node)
        self.assertEqual(node.dump(), dumped_flat_node)

        # check that error will be raised if taken invalid type
        with self.assertRaises(exc.InvalidType):
            invalid_flat_node = object()
            structs.FlatNode.load(invalid_flat_node)


class ListNodeTestCase(TestCase):
    def test_load_and_dump_and_items(self):
        dumped_list_node = ['some sting', {'some nested node': ['nest']}]
        node = structs.ListNode.load(dumped_list_node)
        self.assertEqual(node.items(), dumped_list_node)
        self.assertEqual(node.dump(), dumped_list_node)

        # check that error will be raised if invalid type was taken
        with self.assertRaises(exc.InvalidType):
            invalid = object()
            structs.ListNode.load(invalid)


class NestedNodeTestCase(TestCase):
    def test_load(self):
        self.fail('Not implemented')

    def test_dump(self):
        self.fail('Not implemented')

    def test_items(self):
        self.fail('Not implemented')

    def test_root(self):
        self.fail('Not implemented')
