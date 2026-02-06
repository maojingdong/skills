"""
Code Generator Module

This module handles the generation of Java code files from parsed table information
using predefined templates and proper file organization.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from jinja2 import Template

from ddl_parser import TableInfo, FieldInfo
from java_templates import JavaTemplates


class CodeGenerator:
    """Main code generator class"""
    
    def __init__(self, templates: JavaTemplates, base_package: str = "com.example.project", 
                 table_prefix: str = None):
        self.templates = templates
        self.base_package = base_package
        self.table_prefix = table_prefix or ""
        
    def generate(self, table_info: TableInfo, output_dir: str) -> List[str]:
        """
        Generate all Java code files for the given table
        
        Args:
            table_info: Parsed table information
            output_dir: Output directory for generated files
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        # Prepare template context
        context = self._prepare_context(table_info)
        
        # Create output directory structure
        self._create_directory_structure(output_dir)
        
        # Generate each component
        components = [
            ('entity', 'entity'),
            ('mapper', 'mapper'), 
            ('service', 'service'),
            ('service_impl', 'service/impl'),
            ('controller', 'controller')
        ]
        
        for template_type, sub_dir in components:
            file_path = self._generate_component(
                template_type, context, output_dir, sub_dir
            )
            if file_path:
                generated_files.append(file_path)
        
        return generated_files
    
    def _prepare_context(self, table_info: TableInfo) -> Dict[str, Any]:
        """Prepare context data for template rendering"""
        class_name = self._to_camel_case(
            self._remove_prefix(table_info.name, self.table_prefix)
        )
        
        # Process fields
        processed_fields = []
        has_bigdecimal = False
        primary_key_field = None
        
        for field in table_info.fields:
            property_name = self._to_camel_case(field.name, capitalize_first=False)
            field_dict = {
                'name': field.name,
                'property_name': property_name,
                'java_type': field.java_type,
                'is_primary_key': field.is_primary_key,
                'is_nullable': field.is_nullable,
                'is_auto_increment': field.is_auto_increment,
                'comment': field.comment
            }
            processed_fields.append(field_dict)
            
            if field.java_type == 'BigDecimal':
                has_bigdecimal = True
                
            if field.is_primary_key:
                primary_key_field = field_dict
        
        # Determine primary key type and property name
        primary_key_type = "Long"  # default
        primary_key_property = "Id"  # default
        
        if primary_key_field:
            primary_key_type = primary_key_field['java_type']
            primary_key_property = self._to_camel_case(primary_key_field['name'], capitalize_first=True)
        
        return {
            'package': self.base_package,
            'table_name': table_info.name,
            'class_name': class_name,
            'class_name_lower': self._to_camel_case(
                self._remove_prefix(table_info.name, self.table_prefix), 
                capitalize_first=False
            ),
            'service_name': self._to_camel_case(
                self._remove_prefix(table_info.name, self.table_prefix), 
                capitalize_first=False
            ) + "Service",
            'table_comment': table_info.comment,
            'fields': processed_fields,
            'has_bigdecimal': has_bigdecimal,
            'primary_key_type': primary_key_type,
            'primary_key_property': primary_key_property
        }
    
    def _generate_component(self, template_type: str, context: Dict[str, Any], 
                          output_dir: str, sub_dir: str) -> str:
        """Generate a single component file"""
        template_content = self.templates.get_template(template_type)
        if not template_content:
            return ""
        
        # Render template
        template = Template(template_content)
        rendered_content = template.render(context)
        
        # Determine file path
        class_name = context['class_name']
        file_name = f"{class_name}"
        
        if template_type == 'service_impl':
            file_name += "ServiceImpl"
        elif template_type == 'mapper':
            file_name += "Mapper"
        elif template_type == 'service':
            file_name += "Service"
        elif template_type == 'controller':
            file_name += "Controller"
        elif template_type == 'entity':
            pass  # Entity class name is already correct
        
        file_name += ".java"
        
        # Create full file path
        full_path = os.path.join(output_dir, self._package_to_path(), sub_dir, file_name)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        
        return full_path
    
    def _create_directory_structure(self, output_dir: str):
        """Create the required directory structure"""
        base_path = Path(output_dir) / self._package_to_path()
        
        directories = [
            'entity',
            'mapper',
            'service',
            'service/impl',
            'controller'
        ]
        
        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
    
    def _package_to_path(self) -> str:
        """Convert package name to directory path"""
        return self.base_package.replace('.', '/')
    
    def _to_camel_case(self, snake_str: str, capitalize_first: bool = True) -> str:
        """Convert snake_case to CamelCase or camelCase"""
        components = snake_str.split('_')
        if capitalize_first:
            return ''.join(x.capitalize() for x in components)
        else:
            return components[0].lower() + ''.join(x.capitalize() for x in components[1:])
    
    def _remove_prefix(self, table_name: str, prefix: str) -> str:
        """Remove prefix from table name"""
        if prefix and table_name.startswith(prefix):
            return table_name[len(prefix):]
        return table_name