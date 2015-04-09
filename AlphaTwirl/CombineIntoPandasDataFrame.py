# Tai Sakuma <tai.sakuma@cern.ch>
import pandas

##____________________________________________________________________________||
def countsToDataFrame(counts, keyNames, valNames = ('n', 'nvar')):
    if not counts:
        columns = tuple(keyNames) + tuple(valNames)
        return pandas.DataFrame(columns = columns)
        return
    valNames = counts.values()[0].keys()
    d = [k + tuple([v[n] for n in valNames]) for k, v in counts.iteritems()]
    d.sort()
    columns = tuple(keyNames) + tuple(valNames)
    return pandas.DataFrame(d, columns = columns)

##____________________________________________________________________________||
class CombineIntoPandasDataFrame(object):
    def __init__(self):
        self.datasetColumnName = 'component'

    def combine(self, datasetReaderPairs):
        df = None
        for datasetName, reader in datasetReaderPairs:
            if not reader.results(): continue
            tbl_c = countsToDataFrame(reader.results(), reader.keynames(), reader.valNames())
            tbl_c.insert(0, self.datasetColumnName, datasetName)
            if df is None:
                df = tbl_c
            else:
                df = df.append(tbl_c, ignore_index = True)
        if df is None:
            reader = datasetReaderPairs[0][1]
            columns = (self.datasetColumnName, ) + tuple(reader.keynames()) + tuple(reader.valNames())
            df = pandas.DataFrame(columns = columns)
        return df

##____________________________________________________________________________||
