# Java Code Generator Skill

这是一个Qoder技能，可以根据数据库DDL语句自动生成完整的Java后端代码框架。

## 功能特性

- ✅ 解析标准SQL DDL语句
- ✅ 自动生成MyBatis-Plus集成的Java代码
- ✅ 创建完整的三层架构（Entity/Mapper/Service/Controller）
- ✅ 智能数据类型映射
- ✅ 支持主键自动识别
- ✅ 符合Java命名规范
- ✅ 可配置包名和表前缀

## 使用方法

### 基本用法

```bash
# 从DDL语句生成代码
python scripts/main.py --ddl "CREATE TABLE user (id BIGINT PRIMARY KEY, name VARCHAR(50))" --package "com.example.project"

# 从SQL文件生成代码
python scripts/main.py --ddl "schema.sql" --package "com.example.project" --output-dir "./src/main/java"
```

### 命令行参数

```
--ddl TEXT          DDL语句或SQL文件路径（必需）
--package TEXT      基础包名（默认：com.example.project）
--output-dir TEXT   输出目录（默认：./generated）
--table-prefix TEXT 表名前缀（用于生成类名时自动移除）
--verbose          显示详细输出
```

## 生成的代码结构

```
com.example.project/
├── entity/          # 实体类（带MyBatis-Plus注解）
├── mapper/          # Mapper接口（继承BaseMapper）
├── service/         # Service接口
│   └── impl/        # Service实现类
└── controller/      # REST控制器
```

## 支持的数据类型

| 数据库类型 | Java类型 | MyBatis注解 |
|-----------|----------|-------------|
| VARCHAR/CHAR | String | @TableField |
| INT/INTEGER | Integer | @TableField |
| BIGINT | Long | @TableId/@TableField |
| DECIMAL/NUMERIC | BigDecimal | @TableField |
| DATETIME/TIMESTAMP | LocalDateTime | @TableField |
| DATE | LocalDate | @TableField |
| TINYINT | Boolean/Integer | @TableField |

## 依赖要求

- Python 3.6+
- Jinja2 模板引擎

```bash
pip install jinja2
```

## 示例

### 输入DDL
```sql
CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) COMMENT '邮箱地址',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) COMMENT='用户表';
```

### 生成的实体类
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ApiModel(value = "User对象", description = "User实体类")
@TableName("user")
public class User implements Serializable {
    
    @ApiModelProperty(value = "用户ID")
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    @ApiModelProperty(value = "用户名", required = true)
    @TableField("username")
    private String username;
    
    @ApiModelProperty(value = "邮箱地址")
    @TableField("email")
    private String email;
    
    @ApiModelProperty(value = "创建时间")
    @TableField("created_time")
    private LocalDateTime createdTime;
}
```

## 参考文档

- [MyBatis-Plus最佳实践](references/mybatis-plus-guide.md)
- [Java命名规范](references/naming-conventions.md)