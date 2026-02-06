"""
Java Code Templates

This module defines the templates for generating Java code files.
Each template is a string with placeholders that will be filled during code generation.
"""

from typing import Dict, Any


class JavaTemplates:
    """Container for Java code templates"""
    
    def __init__(self):
        self.templates = {
            'entity': self._get_entity_template(),
            'mapper': self._get_mapper_template(),
            'service': self._get_service_template(),
            'service_impl': self._get_service_impl_template(),
            'controller': self._get_controller_template()
        }
    
    def get_template(self, template_type: str) -> str:
        """Get template by type"""
        return self.templates.get(template_type, "")
    
    def _get_entity_template(self) -> str:
        """Template for Entity class"""
        return '''package {{package}}.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.io.Serializable;
import java.time.LocalDateTime;
{% if has_bigdecimal %}
import java.math.BigDecimal;
{% endif %}

/**
 * {{class_name}}实体类
{% if table_comment %}
 * {{table_comment}}
{% endif %}
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ApiModel(value = "{{class_name}}对象", description = "{{class_name}}实体类")
@TableName("{{table_name}}")
public class {{class_name}} implements Serializable {

    private static final long serialVersionUID = 1L;
    
{% for field in fields %}
    {% if field.is_primary_key %}
    @ApiModelProperty(value = "{{field.comment or field.name}}")
    @TableId(value = "{{field.name}}", type = IdType.{{'AUTO' if field.is_auto_increment else 'NONE'}})
    private {{field.java_type}} {{field.property_name}};
    {% else %}
    @ApiModelProperty(value = "{{field.comment or field.name}}"{% if not field.is_nullable %}, required = true{% endif %})
    @TableField("{{field.name}}")
    private {{field.java_type}} {{field.property_name}};
    {% endif %}
{% endfor %}

}'''
    
    def _get_mapper_template(self) -> str:
        """Template for Mapper interface"""
        return '''package {{package}}.mapper;

import {{package}}.entity.{{class_name}};
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/**
 * {{class_name}}Mapper接口
 */
@Mapper
public interface {{class_name}}Mapper extends BaseMapper<{{class_name}}> {

    // 可在此处添加自定义查询方法
    
}'''
    
    def _get_service_template(self) -> str:
        """Template for Service interface"""
        return '''package {{package}}.service;

import {{package}}.entity.{{class_name}};
import com.baomidou.mybatisplus.extension.service.IService;

/**
 * {{class_name}}Service接口
 */
public interface {{class_name}}Service extends IService<{{class_name}}> {

    // 可在此处添加自定义业务方法
    
}'''
    
    def _get_service_impl_template(self) -> str:
        """Template for Service implementation"""
        return '''package {{package}}.service.impl;

import {{package}}.entity.{{class_name}};
import {{package}}.mapper.{{class_name}}Mapper;
import {{package}}.service.{{class_name}}Service;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * {{class_name}}Service实现类
 */
@Service
public class {{class_name}}ServiceImpl extends ServiceImpl<{{class_name}}Mapper, {{class_name}}> implements {{class_name}}Service {

    // 可在此处添加自定义业务逻辑实现
    
}'''
    
    def _get_controller_template(self) -> str:
        """Template for Controller class"""
        return '''package {{package}}.controller;

import {{package}}.entity.{{class_name}};
import {{package}}.service.{{class_name}}Service;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * {{class_name}}控制器
 */
@RestController
@RequestMapping("/api/{{class_name_lower}}")
@Api(tags = "{{class_name}}管理")
public class {{class_name}}Controller {

    @Autowired
    private {{class_name}}Service {{service_name}};

    @PostMapping
    @ApiOperation("创建{{class_name}}")
    public {{class_name}} create(@RequestBody {{class_name}} {{class_name_lower}}) {
        {{service_name}}.save({{class_name_lower}});
        return {{class_name_lower}};
    }

    @GetMapping("/{id}")
    @ApiOperation("根据ID获取{{class_name}}")
    public {{class_name}} getById(
            @ApiParam("{{class_name}}ID") @PathVariable {{primary_key_type}} id) {
        return {{service_name}}.getById(id);
    }

    @GetMapping
    @ApiOperation("分页查询{{class_name}}列表")
    public Page<{{class_name}}> getPage(
            @ApiParam("页码") @RequestParam(defaultValue = "1") Integer current,
            @ApiParam("每页大小") @RequestParam(defaultValue = "10") Integer size) {
        Page<{{class_name}}> page = new Page<>(current, size);
        return {{service_name}}.page(page);
    }

    @PutMapping("/{id}")
    @ApiOperation("更新{{class_name}}")
    public boolean update(
            @ApiParam("{{class_name}}ID") @PathVariable {{primary_key_type}} id,
            @RequestBody {{class_name}} {{class_name_lower}}) {
        {{class_name_lower}}.set{{primary_key_property}}(id);
        return {{service_name}}.updateById({{class_name_lower}});
    }

    @DeleteMapping("/{id}")
    @ApiOperation("删除{{class_name}}")
    public boolean delete(
            @ApiParam("{{class_name}}ID") @PathVariable {{primary_key_type}} id) {
        return {{service_name}}.removeById(id);
    }

    @GetMapping("/list")
    @ApiOperation("查询所有{{class_name}}")
    public List<{{class_name}}> listAll() {
        return {{service_name}}.list();
    }
}'''