#!/usr/bin/env python3
"""
Java Code Generator Main Entry Point

This script serves as the main entry point for the Java code generation tool.
It parses command line arguments and orchestrates the DDL parsing and code generation process.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the scripts directory to Python path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from ddl_parser import DDLParser
from code_generator import CodeGenerator
from java_templates import JavaTemplates


def main():
    parser = argparse.ArgumentParser(
        description='Generate Java backend code from database DDL statements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --ddl "CREATE TABLE user (id BIGINT PRIMARY KEY, name VARCHAR(50))"
  %(prog)s --ddl schema.sql --package com.mycompany.project
  %(prog)s --ddl schema.sql --output-dir ./src/main/java
        """
    )
    
    parser.add_argument(
        '--ddl',
        required=True,
        help='DDL statement or path to SQL file containing DDL statements'
    )
    
    parser.add_argument(
        '--package',
        default='com.example.project',
        help='Base package name for generated Java classes (default: com.example.project)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='./generated',
        help='Output directory for generated Java files (default: ./generated)'
    )
    
    parser.add_argument(
        '--table-prefix',
        help='Table name prefix to remove when generating class names'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        # Read DDL content
        if os.path.isfile(args.ddl):
            with open(args.ddl, 'r', encoding='utf-8') as f:
                ddl_content = f.read()
            if args.verbose:
                print(f"Reading DDL from file: {args.ddl}")
        else:
            ddl_content = args.ddl
            if args.verbose:
                print("Using DDL from command line argument")
        
        # Parse DDL
        if args.verbose:
            print("Parsing DDL...")
        
        parser_instance = DDLParser()
        table_info = parser_instance.parse(ddl_content)
        
        if args.verbose:
            print(f"Parsed table: {table_info.name}")
            print(f"Fields: {len(table_info.fields)}")
        
        # Generate code
        if args.verbose:
            print("Generating Java code...")
        
        templates = JavaTemplates()
        generator = CodeGenerator(templates, args.package, args.table_prefix)
        generated_files = generator.generate(table_info, args.output_dir)
        
        # Print results
        print(f"\nSuccessfully generated {len(generated_files)} files:")
        for file_path in generated_files:
            print(f"  - {file_path}")
            
        print(f"\nOutput directory: {os.path.abspath(args.output_dir)}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()