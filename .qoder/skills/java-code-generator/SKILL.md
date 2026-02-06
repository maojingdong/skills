---
name: java-code-generator
description: "Generate complete Java backend code from database DDL statements. Creates Entity, Mapper, Service, and Controller layers with MyBatis-Plus integration. Use when converting database table structures to Spring Boot backend code, generating CRUD APIs from table definitions, or creating standardized Java backend frameworks from SQL schemas."
---

# Java Code Generator from DDL

## Overview

This skill automatically generates complete Java backend code from database DDL statements, creating a full Spring Boot application structure with MyBatis-Plus integration.

## Quick Start

### Basic Usage

1. Provide your DDL statement:
```sql
CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) COMMENT '邮箱地址',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
);
```

2. Run the generator:
```bash
python scripts/main.py --ddl "your_ddl_statement" --package "com.example.project"
```

3. Get complete backend structure:
```
com.example.project/
├── entity/User.java
├── mapper/UserMapper.java
├── service/UserService.java
├── service/impl/UserServiceImpl.java
└── controller/UserController.java
```

## Generated Components

### Entity Class
- Automatic field mapping from database columns
- MyBatis-Plus annotations (@TableName, @TableId, @TableField)
- Lombok annotations (@Data, @Builder, @NoArgsConstructor, @AllArgsConstructor)
- Proper Java data type conversion

### Mapper Interface
- Extends MyBatis-Plus BaseMapper<T>
- Ready for immediate CRUD operations
- Supports custom query method declarations

### Service Layer
- Service interface with business method definitions
- ServiceImpl with MyBatis-Plus IService integration
- Built-in transaction management

### Controller Layer
- RESTful API endpoints (GET, POST, PUT, DELETE)
- Request validation and error handling
- Standard response format

## Command Line Options

```bash
python scripts/main.py [OPTIONS]

Options:
  --ddl TEXT          DDL statement or file path
  --package TEXT      Base package name (default: com.example.project)
  --output-dir TEXT   Output directory (default: ./generated)
  --table-prefix TEXT Table name prefix to remove
  --help             Show this message and exit
```

## Data Type Mapping

| Database Type | Java Type | Annotation |
|---------------|-----------|------------|
| VARCHAR/CHAR | String | @TableField |
| INT/INTEGER | Integer | @TableField |
| BIGINT | Long | @TableField |
| DECIMAL/NUMERIC | BigDecimal | @TableField |
| DATETIME/TIMESTAMP | LocalDateTime | @TableField |
| DATE | LocalDate | @TableField |
| TINYINT | Boolean/Integer | @TableField |

## Best Practices

### Package Structure
Follow standard Maven/Gradle structure:
```
src/main/java/com/example/project/
├── entity/          # Entity classes
├── mapper/          # Mapper interfaces
├── service/         # Service interfaces
│   └── impl/        # Service implementations
└── controller/      # REST controllers
```

### Naming Conventions
- Classes: UpperCamelCase (User, UserProfile)
- Fields: lowerCamelCase (userName, emailAddress)
- Tables: snake_case (user_profile, order_items)
- Packages: lowercase with dots (com.example.project)

### MyBatis-Plus Integration
- Use @TableName for table mapping
- Use @TableId for primary key identification
- Use @TableField for column mapping
- Extend BaseMapper for automatic CRUD operations

## Advanced Features

### Custom Configuration
See [references/mybatis-plus-guide.md](references/mybatis-plus-guide.md) for advanced MyBatis-Plus configurations.

### Naming Conventions
Refer to [references/naming-conventions.md](references/naming-conventions.md) for detailed naming standards.

## Troubleshooting

Common issues and solutions:

1. **Parsing errors**: Ensure DDL syntax is valid SQL
2. **Type mapping issues**: Check if data types are supported
3. **Annotation conflicts**: Verify MyBatis-Plus version compatibility
4. **Package structure**: Ensure proper Maven/Gradle project structure

## Examples

### Simple Table
```sql
CREATE TABLE product (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    status TINYINT DEFAULT 1
);
```

Generated files include complete CRUD operations with proper validation and error handling.

### Complex Table with Relationships
```sql
CREATE TABLE order (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

Generates relationship-aware code with appropriate annotations and methods.