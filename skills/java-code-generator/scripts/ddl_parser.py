"""
DDL Parser Module

This module provides functionality to parse SQL DDL statements and extract
table structure information including fields, data types, constraints, and annotations.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from enum import Enum


class DataType(Enum):
    """Database data types enumeration"""
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    TEXT = "TEXT"
    INT = "INT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    SMALLINT = "SMALLINT"
    TINYINT = "TINYINT"
    DECIMAL = "DECIMAL"
    NUMERIC = "NUMERIC"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"


@dataclass
class FieldInfo:
    """Information about a database field/column"""
    name: str
    data_type: DataType
    java_type: str
    is_primary_key: bool = False
    is_nullable: bool = True
    is_auto_increment: bool = False
    default_value: Optional[str] = None
    comment: Optional[str] = None
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None


@dataclass
class TableInfo:
    """Information about a database table"""
    name: str
    fields: List[FieldInfo] = field(default_factory=list)
    comment: Optional[str] = None
    primary_keys: List[str] = field(default_factory=list)
    foreign_keys: List[Dict] = field(default_factory=list)
    indexes: List[Dict] = field(default_factory=list)


class DDLParser:
    """Main DDL parser class"""
    
    def __init__(self):
        # Regular expressions for parsing
        self.create_table_pattern = re.compile(
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([^\s\(]+)\s*\((.*?)\)(?:\s*COMMENT\s*=[\'"](.+?)[\'"])?\s*;',
            re.IGNORECASE | re.DOTALL
        )
        
        self.field_pattern = re.compile(
            r'^\s*([^\s]+)\s+([^\s\(]+)(?:\(([^)]+)\))?\s*(.*)$',
            re.IGNORECASE
        )
        
        self.primary_key_pattern = re.compile(
            r'PRIMARY\s+KEY\s*\(\s*([^\)]+)\s*\)',
            re.IGNORECASE
        )
        
        self.comment_pattern = re.compile(
            r'COMMENT\s+[\'"]([^\'"]+)[\'"]',
            re.IGNORECASE
        )
        
        self.default_pattern = re.compile(
            r'DEFAULT\s+([^\s,]+)',
            re.IGNORECASE
        )
        
        self.auto_increment_pattern = re.compile(
            r'AUTO_INCREMENT|IDENTITY',
            re.IGNORECASE
        )
        
        self.null_pattern = re.compile(
            r'(NOT\s+NULL|NULL)',
            re.IGNORECASE
        )
        
        # Data type mapping to Java types
        self.type_mapping = {
            DataType.VARCHAR: "String",
            DataType.CHAR: "String",
            DataType.TEXT: "String",
            DataType.INT: "Integer",
            DataType.INTEGER: "Integer",
            DataType.BIGINT: "Long",
            DataType.SMALLINT: "Integer",
            DataType.TINYINT: "Boolean",  # Could also be Integer depending on context
            DataType.DECIMAL: "BigDecimal",
            DataType.NUMERIC: "BigDecimal",
            DataType.FLOAT: "Float",
            DataType.DOUBLE: "Double",
            DataType.BOOLEAN: "Boolean",
            DataType.DATE: "LocalDate",
            DataType.TIME: "LocalTime",
            DataType.DATETIME: "LocalDateTime",
            DataType.TIMESTAMP: "LocalDateTime",
        }

    def parse(self, ddl_content: str) -> TableInfo:
        """
        Parse DDL content and return TableInfo object
        
        Args:
            ddl_content (str): SQL DDL statement(s)
            
        Returns:
            TableInfo: Parsed table information
            
        Raises:
            ValueError: If DDL cannot be parsed
        """
        # Find CREATE TABLE statement
        match = self.create_table_pattern.search(ddl_content)
        if not match:
            raise ValueError("No valid CREATE TABLE statement found in DDL")
        
        table_name = match.group(1).strip().strip('`"')
        table_definition = match.group(2)
        table_comment = match.group(3) if match.group(3) else None
        
        # Create table info object
        table_info = TableInfo(
            name=table_name,
            comment=table_comment
        )
        
        # Parse fields
        self._parse_fields(table_info, table_definition)
        
        # Parse primary keys
        self._parse_primary_keys(table_info, table_definition)
        
        # Parse foreign keys and indexes (basic support)
        self._parse_constraints(table_info, table_definition)
        
        return table_info
    
    def _parse_fields(self, table_info: TableInfo, table_definition: str):
        """Parse field definitions from table definition"""
        # Simple approach: split by comma outside of parentheses
        lines = []
        current_line = ""
        paren_count = 0
        
        for char in table_definition:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                lines.append(current_line.strip())
                current_line = ""
                continue
            current_line += char
        
        # Add the last line
        if current_line.strip():
            lines.append(current_line.strip())
        
        # Process each field line
        for line in lines:
            field_info = self._parse_field_line(line)
            if field_info:
                table_info.fields.append(field_info)
    
    def _parse_field_line(self, line: str) -> Optional[FieldInfo]:
        """Parse a single field definition line"""
        line = line.strip()
        if not line or line.upper().startswith(('PRIMARY', 'FOREIGN', 'UNIQUE', 'INDEX', 'CONSTRAINT')):
            return None
        
        match = self.field_pattern.match(line)
        if not match:
            return None
        
        field_name = match.group(1).strip().strip('`"')
        data_type_str = match.group(2).upper()
        type_params = match.group(3)
        modifiers = match.group(4) if match.group(4) else ""
        
        # Parse data type
        data_type = self._parse_data_type(data_type_str, type_params)
        if not data_type:
            return None
        
        java_type = self.type_mapping.get(data_type, "Object")
        
        # Parse modifiers
        is_nullable = 'NOT NULL' not in modifiers.upper()
        is_auto_increment = bool(self.auto_increment_pattern.search(modifiers))
        default_value = self._extract_default_value(modifiers)
        comment = self._extract_comment(modifiers)
        
        # Check for PRIMARY KEY in field definition
        is_primary_key = 'PRIMARY KEY' in modifiers.upper()
        
        # Handle TINYINT special case
        if data_type == DataType.TINYINT and java_type == "Boolean":
            # Check if it's used as boolean or integer
            if comment and ('true' in comment.lower() or 'false' in comment.lower()):
                java_type = "Boolean"
            else:
                java_type = "Integer"
        
        return FieldInfo(
            name=field_name,
            data_type=data_type,
            java_type=java_type,
            is_primary_key=is_primary_key,
            is_nullable=is_nullable,
            is_auto_increment=is_auto_increment,
            default_value=default_value,
            comment=comment,
            length=self._extract_length(type_params),
            precision=self._extract_precision(type_params),
            scale=self._extract_scale(type_params)
        )
    
    def _parse_data_type(self, type_str: str, params: Optional[str]) -> Optional[DataType]:
        """Parse SQL data type string to DataType enum"""
        type_str = type_str.upper()
        
        # Handle parameterized types
        if '(' in type_str:
            type_str = type_str.split('(')[0]
        
        try:
            return DataType(type_str)
        except ValueError:
            # Handle aliases
            type_aliases = {
                'INT': DataType.INTEGER,
                'INTEGER': DataType.INTEGER,
                'BOOL': DataType.TINYINT,
                'BOOLEAN': DataType.TINYINT,
                'DATETIME': DataType.TIMESTAMP,
            }
            return type_aliases.get(type_str)
    
    def _parse_primary_keys(self, table_info: TableInfo, table_definition: str):
        """Parse primary key definitions"""
        # Look for PRIMARY KEY constraint
        pk_match = self.primary_key_pattern.search(table_definition)
        if pk_match:
            pk_columns = pk_match.group(1)
            # Handle multiple columns
            columns = [col.strip().strip('`"') for col in pk_columns.split(',')]
            table_info.primary_keys.extend(columns)
            
            # Mark fields as primary key
            for field in table_info.fields:
                if field.name in columns:
                    field.is_primary_key = True
    
    def _parse_constraints(self, table_info: TableInfo, table_definition: str):
        """Parse foreign keys and other constraints (basic support)"""
        # This is a simplified implementation
        # In a production version, you'd want more robust constraint parsing
        pass
    
    def _extract_comment(self, modifiers: str) -> Optional[str]:
        """Extract comment from field modifiers"""
        match = self.comment_pattern.search(modifiers)
        return match.group(1).strip() if match else None
    
    def _extract_default_value(self, modifiers: str) -> Optional[str]:
        """Extract default value from field modifiers"""
        match = self.default_pattern.search(modifiers)
        return match.group(1).strip() if match else None
    
    def _extract_length(self, params: Optional[str]) -> Optional[int]:
        """Extract length parameter"""
        if not params or ',' in params:
            return None
        try:
            return int(params)
        except ValueError:
            return None
    
    def _extract_precision(self, params: Optional[str]) -> Optional[int]:
        """Extract precision from decimal/numeric parameters"""
        if not params or ',' not in params:
            return None
        try:
            return int(params.split(',')[0])
        except ValueError:
            return None
    
    def _extract_scale(self, params: Optional[str]) -> Optional[int]:
        """Extract scale from decimal/numeric parameters"""
        if not params or ',' not in params:
            return None
        try:
            return int(params.split(',')[1])
        except ValueError:
            return None