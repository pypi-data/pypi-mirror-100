from pathlib import Path

from progress.bar import Bar
from pyimporters_dummy.dummy import DummyOptions, DummyKnowledgeParser
from pyimporters_plugins.base import Term


def test_dummy():
    source = Path()
    parser = DummyKnowledgeParser()
    options = DummyOptions(foo="test")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0 : Term = concepts[0]
    assert c0.identifier == 'test'
    assert c0.prefLabel == 'test'
    assert c0.altLabel is None
