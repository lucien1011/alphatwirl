# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class EventReaderPackage(object):

    """This class relates event readers and a result collector.

    An instance of this class is initialized with a reader class and a
    collector.

    When the method ``make()`` is called with a data set name, this
    class creates a reader, provide the collector with the pair of
    the data set name and the reader, and returns the reader.

    After the readers read events, the mothod ``collect`` is called.
    This method, in turn, calls the method ``collect`` of the
    collector.

    """

    def __init__(self, ReaderClass, resultCollector = None):
        self._ReaderClass = ReaderClass
        self._resultCollector = resultCollector if resultCollector is not None else NullCollector()

    def make(self, datasetName):
        reader = self._ReaderClass()
        self._resultCollector.addReader(datasetName, reader)
        return reader

    def collect(self):
        self._resultCollector.collect()

##____________________________________________________________________________||
class NullCollector(object):
    def collect(self): pass
    def addReader(self, datasetName, reader): pass

##____________________________________________________________________________||
