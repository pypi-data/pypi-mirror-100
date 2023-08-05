import abc
from typing import Optional, List, Dict, Any, Type, Generator
from pathlib import Path

from progress.bar import Bar
from pydantic import BaseModel, Field

class Term(BaseModel):
    identifier: str = Field(..., description="Unique identifier of the term", example="http://www.example.com/rocks")
    prefLabel: str = Field(..., description="The preferred label of the term", example="rocks")
    altLabel: Optional[List[str]] = Field(None, description="The alternative labels of the term", example=["basalt", "granite", "slate"])
    properties: Optional[Dict[str,Any]] = Field(None, description="Additional properties of the term", example={"wikidataId" : "Q8063"})

class KnowledgeParserOptions(BaseModel):
    """
    Options for the knowledge import
    """
    format: str = Field(None, description="Format of the import")
    lang: str = Field('en', description="Language of the project", extra="internal")
    limit: int = Field(0, description="Number of concepts to import. O means all", extra="advanced", ge=0)
    class Config:
        orm_mode = True

class KnowledgeParserBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, source : Path, options: Dict[str,Any], bar : Bar) -> Generator[Term, None, None]:
        """Parse the input source file and return a stream of concepts.

        :param source: A file object containing the knowledge.
        :param options: options of the parser.
        :returns: Iterable producing the concepts.
        """

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return KnowledgeParserOptions