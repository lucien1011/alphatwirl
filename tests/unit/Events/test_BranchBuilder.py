from AlphaTwirl.Events import BranchBuilder
import sys
import unittest

##____________________________________________________________________________||
class MockFile(object):
    pass

##____________________________________________________________________________||
class MockTree(object):
    def __init__(self, Entries = 100):
        self.Entries = Entries
        self.iEvent = -1
        self.leafNames = ('run', 'evt', 'njet', 'jet_pt', 'met_pt')
        self.branchstatus = [ ]
        self.getEntryCalled = False
    def GetDirectory(self):
        return MockFile()
    def GetEntries(self):
        return self.Entries
    def GetEntry(self, ientry):
        self.getEntryCalled = True
        if ientry < self.Entries:
            nbytes = 10
            self.iEvent = ientry
        else:
            nbytes = 0
            self.iEvent = -1
        return nbytes

    def SetBranchStatus(self, bname, status):
        self.branchstatus.append((bname, status))

    def _isleafName(self, name): return name in self.leafNames


##____________________________________________________________________________||
class MockArray(object): pass

##____________________________________________________________________________||
class MockBranchAddressManager(object):
    def getArrays(self, tree, branchName):
        if tree._isleafName(branchName):
            return MockArray(), MockArray()
        return None, None

##____________________________________________________________________________||
class MockBranch(object):
    def __init__(self, name, array, countarray):
        pass

##____________________________________________________________________________||
class TestMockTree(unittest.TestCase):

    def test_mocktree(self):
        tree = MockTree(Entries = 3)
        self.assertIsInstance(tree.GetDirectory(), MockFile)
        self.assertEqual(3, tree.GetEntries())

        self.assertEqual(-1, tree.iEvent)

        nbytes = 10
        self.assertEqual(nbytes, tree.GetEntry(0))
        self.assertEqual(0, tree.iEvent)
        self.assertEqual(nbytes, tree.GetEntry(1))
        self.assertEqual(1, tree.iEvent)
        self.assertEqual(nbytes, tree.GetEntry(2))
        self.assertEqual(2, tree.iEvent)
        self.assertEqual(0, tree.GetEntry(3))
        self.assertEqual(-1, tree.iEvent)

##____________________________________________________________________________||
class TestBranchBuilder(unittest.TestCase):

    def setUp(self):
        self.moduleBranchBuilder = sys.modules['AlphaTwirl.Events.BranchBuilder']
        self.org_branchAddressManager = self.moduleBranchBuilder.branchAddressManager
        self.moduleBranchBuilder.branchAddressManager = MockBranchAddressManager()

        self.org_Branch = self.moduleBranchBuilder.Branch
        self.moduleBranchBuilder.Branch = MockBranch

    def tearDown(self):
        self.moduleBranchBuilder.branchAddressManager = self.org_branchAddressManager
        self.moduleBranchBuilder.Branch = self.org_Branch

    def test_init(self):
        builder = BranchBuilder()

    def test_getattr(self):
        builder = BranchBuilder()
        tree = MockTree()

        jet_pt = builder(tree, "jet_pt")
        met_pt = builder(tree, "met_pt")
        self.assertIsInstance(jet_pt, MockBranch)
        self.assertIsInstance(met_pt, MockBranch)

    def test_getattr_same_objects_different_calls(self):

        builder = BranchBuilder()

        tree = MockTree()
        jet_pt1 = builder(tree, "jet_pt")
        met_pt1 = builder(tree, "met_pt")

        jet_pt2 = builder(tree, "jet_pt")
        met_pt2 = builder(tree, "met_pt")

        self.assertIs(jet_pt1, jet_pt2)
        self.assertIs(met_pt1, met_pt2)

    def test_getattr_same_objects_different_builders(self):

        builder1 = BranchBuilder()
        builder2 = BranchBuilder()

        tree = MockTree()
        jet_pt1 = builder1(tree, "jet_pt")
        met_pt1 = builder1(tree, "met_pt")

        jet_pt2 = builder2(tree, "jet_pt")
        met_pt2 = builder2(tree, "met_pt")

        self.assertIs(jet_pt1, jet_pt2)
        self.assertIs(met_pt1, met_pt2)

    def test_getattr_exception(self):
        builder = BranchBuilder()

        tree = MockTree()

        self.assertRaises(AttributeError, builder.__call__, tree, 'no_such_branch')

##____________________________________________________________________________||
