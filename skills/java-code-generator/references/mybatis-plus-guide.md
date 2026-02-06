# MyBatis-Plus 最佳实践指南

## 概述

MyBatis-Plus是一个强大的MyBatis增强工具，在MyBatis的基础上只做增强不做改变，为简化开发、提高效率而生。

## 核心注解

### @TableName
用于指定实体类对应的数据库表名
```java
@TableName("user_info")
public class User {
    // 字段定义
}
```

### @TableId
用于标识主键字段
```java
@TableId(value = "id", type = IdType.AUTO)
private Long id;
```

**IdType枚举值：**
- AUTO: 数据库自增
- NONE: 无状态
- INPUT: 用户输入
- ASSIGN_ID: 分配ID（雪花算法）
- ASSIGN_UUID: 分配UUID

### @TableField
用于标识普通字段
```java
@TableField("user_name")
private String userName;
```

## 通用CRUD操作

### BaseMapper接口
继承BaseMapper<T>即可获得以下方法：

```java
public interface UserMapper extends BaseMapper<User> {
    // 自动获得以下方法：
    // insert(T entity)
    // deleteById(Serializable id)
    // deleteByMap(Map<String, Object> columnMap)
    // delete(Wrapper<T> wrapper)
    // updateById(T entity)
    // update(T entity, Wrapper<T> updateWrapper)
    // selectById(Serializable id)
    // selectBatchIds(Collection<? extends Serializable> idList)
    // selectByMap(Map<String, Object> columnMap)
    // selectOne(Wrapper<T> queryWrapper)
    // selectCount(Wrapper<T> queryWrapper)
    // selectList(Wrapper<T> queryWrapper)
    // selectMaps(Wrapper<T> queryWrapper)
    // selectObjs(Wrapper<T> queryWrapper)
    // selectPage(IPage<T> page, Wrapper<T> queryWrapper)
    // selectMapsPage(IPage<Map<String, Object>> page, Wrapper<T> queryWrapper)
}
```

### IService接口
Service层继承IService<T>和ServiceImpl<M, T>

```java
// 接口
public interface UserService extends IService<User> {
    // 业务方法定义
}

// 实现类
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    // 业务逻辑实现
}
```

## 分页插件配置

### 配置类
```java
@Configuration
public class MybatisPlusConfig {
    
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }
}
```

### 使用分页
```java
@GetMapping("/page")
public IPage<User> getUserPage(@RequestParam(defaultValue = "1") int current,
                               @RequestParam(defaultValue = "10") int size) {
    Page<User> page = new Page<>(current, size);
    return userService.page(page);
}
```

## 条件构造器

### QueryWrapper
用于构建查询条件
```java
QueryWrapper<User> queryWrapper = new QueryWrapper<>();
queryWrapper.eq("status", 1)
           .like("name", "张")
           .between("age", 18, 30)
           .orderByDesc("create_time");

List<User> users = userMapper.selectList(queryWrapper);
```

### LambdaQueryWrapper
类型安全的条件构造器
```java
LambdaQueryWrapper<User> lambdaQuery = new LambdaQueryWrapper<>();
lambdaQuery.eq(User::getStatus, 1)
          .like(User::getName, "张")
          .between(User::getAge, 18, 30);

List<User> users = userService.list(lambdaQuery);
```

## 自动填充功能

### 配置自动填充
```java
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {
    
    @Override
    public void insertFill(MetaObject metaObject) {
        this.strictInsertFill(metaObject, "createTime", LocalDateTime.class, LocalDateTime.now());
        this.strictInsertFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
    }
    
    @Override
    public void updateFill(MetaObject metaObject) {
        this.strictUpdateFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
    }
}
```

### 实体类使用
```java
@TableName("user")
public class User {
    
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;
    
    private String name;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

## 乐观锁插件

### 配置乐观锁
```java
@Bean
public OptimisticLockerInnerInterceptor optimisticLockerInnerInterceptor() {
    return new OptimisticLockerInnerInterceptor();
}
```

### 实体类添加版本字段
```java
@Version
private Integer version;
```

## 逻辑删除

### 全局配置
```yaml
mybatis-plus:
  global-config:
    db-config:
      logic-delete-field: deleted  # 全局逻辑删除字段名
      logic-delete-value: 1        # 逻辑已删除值
      logic-not-delete-value: 0    # 逻辑未删除值
```

### 实体类字段
```java
@TableLogic
private Integer deleted;
```

## 性能分析插件（开发环境）

```java
@Bean
@Profile({"dev","test"}) // 开发环境和测试环境生效
public PerformanceInterceptor performanceInterceptor() {
    return new PerformanceInterceptor()
            .setMaxTime(1000) // SQL最大执行时间(ms)
            .setFormat(true); // 格式化SQL
}
```

## 代码生成器

虽然我们的技能可以生成基础代码，但MyBatis-Plus官方也提供了代码生成器：

```xml
<!-- Maven依赖 -->
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-generator</artifactId>
    <version>3.5.3.1</version>
</dependency>
```

## 常见问题解决

### 1. 字段名与数据库不匹配
使用@TableField注解明确指定列名

### 2. 主键生成策略选择
- 单体应用：IdType.AUTO（数据库自增）
- 分布式应用：IdType.ASSIGN_ID（雪花算法）

### 3. 分页查询不生效
确保已配置PaginationInnerInterceptor分页插件

### 4. 逻辑删除不工作
检查全局配置和@TableLogic注解是否正确设置

## 最佳实践建议

1. **统一返回格式**：封装统一的API响应类
2. **异常处理**：使用@ControllerAdvice统一处理异常
3. **参数校验**：结合Hibernate Validator进行参数校验
4. **事务管理**：合理使用@Transactional注解
5. **缓存策略**：对于频繁查询的数据考虑使用Redis缓存
6. **日志记录**：记录重要操作日志便于追踪
7. **安全性**：注意SQL注入防护和敏感数据脱敏

## 版本兼容性

确保MyBatis-Plus版本与Spring Boot版本兼容：

| Spring Boot | MyBatis-Plus |
|-------------|--------------|
| 2.7.x       | 3.5.3        |
| 2.6.x       | 3.5.2        |
| 2.5.x       | 3.5.1        |