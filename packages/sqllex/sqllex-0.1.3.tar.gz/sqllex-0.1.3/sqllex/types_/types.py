from pathlib import Path
from typing import Literal, Mapping, Union, List, AnyStr, Any, MutableMapping, Tuple
from numbers import Number


class SQLRequest:
    """
    SQL request contains script and values (if necessary)
    """
    def __init__(self, script: str, values: tuple = None):
        self.script = script
        self.values = values

    def __str__(self):
        return f"""{{SQLiteScript: script={self.script}, values={self.values}}}"""


class SQLStatement:
    """
    SQL request contains SQLRequest
    """
    def __init__(self, request: SQLRequest, path: Union[Path, AnyStr]):
        self.request = request
        self.path = path


# FOREIGN_KEY const type
ForeignKey = Literal["FOREIGN KEY"]

# Types of data for data types of column
DataType = Literal["TEXT", "NUMERIC", "INTEGER", "REAL", "NONE"]

# Types of constants used as keywords for column settings
ConstrainType = Union[
    Literal["NOT NULL", "DEFAULT", "UNIQUE", "CHECK", "AUTOINCREMENT", "PRIMARY KEY", "REFERENCES", "WITH", "OR"],
    ForeignKey
]

# Subtypes for DBTemplateType
ListDataType = List[Union[DataType, ConstrainType, Number]]
ColumnType = Union[ListDataType, DataType, AnyStr]
TableType = Mapping[AnyStr, ColumnType]

# Type for databases template
DBTemplateType = Mapping[AnyStr, TableType]

# Universal Path type
PathType = Union[Path, AnyStr]

# Type for string or numeric data
NumStr = Union[Number, AnyStr]

# Type of data INSERT awaiting
InsertData = Union[NumStr, tuple, List, Mapping]

# Type for parameter of OR argument in INSERT method (?)
OrOptionsType = Literal["ABORT", "FAIL", "IGNORE", "REPLACE", "ROLLBACK"]

# Type for parameter of WITH argument
WithType = Mapping[str, Union[SQLRequest, str]]


if __name__ == "__main__":
    __all__ = [
        ForeignKey,
        DataType,
        ConstrainType,

        ListDataType,
        ColumnType,
        TableType,
        DBTemplateType,

        PathType,
        NumStr,
        SQLRequest,
        OrOptionsType,
        WithType
    ]
