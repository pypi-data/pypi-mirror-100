import codecs
from pathlib import Path
from typing import Type, Dict, Any, Generator
import pandas as pd
from progress.bar import Bar
from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Term

class TXTOptions(KnowledgeParserOptions):
    """
    Options for the TXT knowledge import
    """
    encoding : str = Field('utf-8', description="Encoding of the file")

class TXTKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any], bar : Bar) -> Generator[Term, None, None]:
        options = TXTOptions(**options)
        bar.max = file_len(source)
        bar.start()
        with source.open("r", encoding=options.encoding) as fin:
            for line in fin:
                bar.next()
                term = line.strip()
                if term:
                    yield Term(identifier=term, prefLabel=term)
        bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return TXTOptions

def file_len(input_file:Path):
  """ Count number of lines in a file."""
  with open(input_file) as f:
      nr_of_lines = sum(1 for line in f)
  return nr_of_lines
