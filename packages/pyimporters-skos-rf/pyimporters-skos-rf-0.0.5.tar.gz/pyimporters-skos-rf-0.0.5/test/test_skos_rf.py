from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_skos.skos import SKOSOptions, RDFFormat

from pyimporters_skos_rf.skos_rf import SKOSRFKnowledgeParser


def test_xml():
    source = Path('data/RF-Terminologie-paye.rdf')
    parser = SKOSRFKnowledgeParser()
    options = SKOSOptions(lang="fr", rdf_format=RDFFormat.xml)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 100
    homme = next(c for c in concepts if c.identifier == 'https://revuefiduciaire.grouperf.com/terminology/termino-paye#homme')
    assert homme.identifier == 'https://revuefiduciaire.grouperf.com/terminology/termino-paye#homme'
    assert homme.prefLabel == 'Homme'
    assert len(homme.altLabel) == 1
    assert set(homme.altLabel) == set(['hommes'])


