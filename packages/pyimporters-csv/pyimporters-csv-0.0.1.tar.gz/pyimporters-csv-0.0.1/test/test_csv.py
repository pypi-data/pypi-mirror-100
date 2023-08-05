from pathlib import Path

from progress.bar import Bar

from pyimporters_plugins.base import Term
from pyimporters_csv.csv import CSVKnowledgeParser, CSVOptions, TXTKnowledgeParser, TXTOptions


def test_csv():
    source = Path('data/Digestion.csv')
    parser = CSVKnowledgeParser()
    options = CSVOptions(encoding="utf-8", identifier_col="ID", prefLabel_col="prefLabel_en", altLabel_cols="altLabel_en", multivalue_separator="|")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 92
    c7 : Term = concepts[7]
    assert c7.identifier == 'https://opendata.inra.fr/EMTD/8'
    assert c7.prefLabel == 'specific pathogen-free animal'
    assert len(c7.altLabel) == 2
    assert set(c7.altLabel) == set(['SPF animal', 'specific pathogen free animal'])


def test_txt():
    source = Path('data/currencies.txt')
    parser = TXTKnowledgeParser()
    options = TXTOptions(encoding="utf-8")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 279
    c1 : Term = concepts[1]
    assert c1.identifier == 'Euro'
    assert c1.prefLabel == 'Euro'
    assert c1.altLabel is None
