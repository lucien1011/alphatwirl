from AlphaTwirl.EventReader import EventReaderPackageBundle
import unittest

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, name):
        self.name = name
        self._eventIds = [ ]

    def event(self, event):
        self._eventIds.append(event.id)

##__________________________________________________________________||
class MockReaderPackage(object):
    def __init__(self):
        self.reader = None
        self.collected = False

    def make(self, name):
        self.reader = MockReader(name)
        return self.reader

    def collect(self):
        self.collected = True

##__________________________________________________________________||
class TestEventReaderPackageBundle(unittest.TestCase):

    def test_packages_read_and_collected(self):

        bundle = EventReaderPackageBundle()

        package1 = MockReaderPackage()
        bundle.add(package1)

        package2 = MockReaderPackage()
        bundle.add(package2)

        actual = bundle.make("compName1") # need to evaluate actual before expected.
        expected = [package1.reader, package2.reader]
        self.assertEqual(expected, actual)

        actual = bundle.make("compName2")
        expected = [package1.reader, package2.reader]
        self.assertEqual(expected, actual)

        self.assertFalse(package1.collected)
        self.assertFalse(package2.collected)
        bundle.collect()
        self.assertTrue(package1.collected)
        self.assertTrue(package2.collected)

##__________________________________________________________________||