from collections import defaultdict
from enum import Enum
from gzip import GzipFile
from pathlib import Path
from typing import Type, Dict, Any, Generator
# from xml import etree
from zipfile import ZipFile

from lxml import etree
from collections_extended import setlist

from progress.bar import Bar
from pydantic import BaseModel, Field
from rdflib import Graph, RDF, SKOS
from rdflib.resource import Resource

from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Term


class MeSHOptions(KnowledgeParserOptions):
    """
    Options for the RDF knowledge import
    """
    branches : str = Field(None, description="Comma-separated list of branches to import, for example 'B,C' to import only descriptors belonging to the Organisms & Diseases categories")


# The top-level categories in the MeSH descriptor hierarchy are:
MESH_CATEGORIES = {
    "A": "Anatomy",
    "B": "Organisms",
    "C": "Diseases",
    "D": "Chemicals and Drugs",
    "E": "Analytical, Diagnostic and Therapeutic Techniques and Equipment",
    "F": "Psychiatry and Psychology",
    "G": "Biological Sciences",
    "H": "Physical Sciences",
    "I": "Anthropology, Education, Sociology and Social Phenomena",
    "J": "Technology and Food and Beverages",
    "K": "Humanities",
    "L": "Information Science",
    "M": "Persons",
    "N": "Health Care",
    "V": "Publication Characteristics",
    "Z": "Geographic Locations",
}


class MeSHKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Dict[str, Any], bar: Bar) -> Generator[Term, None, None]:
        options = MeSHOptions(**options)
        allowed_branches = [b.strip() for b in options.branches.split(",") if b.strip() in MESH_CATEGORIES] if options.branches else list(MESH_CATEGORIES.keys())
        try:
            archive, file = file_from_archive(source)
            mesh = etree.parse(file)
            bar.max = int(mesh.xpath("count(//DescriptorRecord)"))
        finally:
            if file:
                file.close()
            if archive:
                archive.close()
        bar.start()
        try:
            archive, file = file_from_archive(source)
            mesh = etree.iterparse(file, events=("end",), tag=['DescriptorRecord'])
            for event, record in mesh:
                bar.next()
                dui = record.findtext("DescriptorUI")
                norm = record.findtext("./DescriptorName/String")
                labels = setlist()
                props = defaultdict(list)
                labels.add(norm)
                for concept in record.iterfind("./ConceptList/Concept"):
                    for term in concept.iterfind("./TermList/Term"):
                        tname = term.findtext("String")
                        labels.add(tname)
                labels.remove(norm)
                cats = setlist()
                branches = setlist()
                for tnumber in record.iterfind("./TreeNumberList/TreeNumber"):
                    number = tnumber.text
                    props['TreeNumber'].append(number)
                    branches.add(number[0])
                    cats.add(MESH_CATEGORIES[number[0]])
                props['Category'] = list(cats)
                props['Branch'] = list(branches)

                record.clear()
                if intersection(allowed_branches, props['Branch']):

                    # for qualifier in record.iterfind("./AllowableQualifiersList/AllowableQualifier/QualifierReferredTo"):
                    #     qid = qualifier.findtext("QualifierUI")
                    #     props['AllowableQualifier'].append(qid)
                    term: Term = Term(identifier=dui, prefLabel=norm, altLabel=list(labels), properties=props)
                    yield term
        finally:
            if file:
                file.close()
            if archive:
                archive.close()
            bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return MeSHOptions


def file_from_archive(source: Path):
    archive = None
    file = None
    if source.suffix == ".gz":
        file = GzipFile(str(source))
    elif source.suffix == ".zip":
        archive = ZipFile(str(source))
        file = archive.open(archive.filelist[0])
    else:
        file = source.open("r", encoding="utf-8")
    return archive, file


# Python program to illustrate the intersection
# of two lists using set() method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))