# Java命名规范参考

## 包命名规范

### 基本原则
- 全部小写字母
- 使用有意义的域名反向作为前缀
- 层次结构清晰

### 标准格式
```
com.company.project.module
org.organization.project.submodule
```

### 常见包结构
```
com.example.project
├── controller      # 控制器层
├── service         # 服务层
│   └── impl        # 服务实现
├── mapper          # 数据访问层
├── entity          # 实体类
├── dto             # 数据传输对象
├── vo              # 视图对象
├── config          # 配置类
├── exception       # 异常处理
├── util            # 工具类
└── constant        # 常量定义
```

## 类命名规范

### 实体类 (Entity)
- 使用名词，首字母大写
- 与数据库表名对应
- 示例：User, Product, OrderDetail

### 控制器类 (Controller)
- 名词 + Controller后缀
- 示例：UserController, ProductController

### 服务接口 (Service)
- 名词 + Service后缀
- 示例：UserService, ProductService

### 服务实现类 (ServiceImpl)
- 名词 + ServiceImpl后缀
- 示例：UserServiceImpl, ProductServiceImpl

### Mapper接口
- 名词 + Mapper后缀
- 示例：UserMapper, ProductMapper

### 配置类 (Config)
- 功能描述 + Config后缀
- 示例：SwaggerConfig, DatabaseConfig

## 方法命名规范

### CRUD操作
```java
// 查询单个
User getUserById(Long id);
User findById(Long id);

// 查询列表
List<User> getAllUsers();
List<User> listUsers();

// 分页查询
Page<User> getUserPage(int current, int size);

// 创建
void createUser(User user);
boolean save(User user);

// 更新
void updateUser(User user);
boolean updateById(User user);

// 删除
void deleteUser(Long id);
boolean removeById(Long id);
```

### 业务方法
- 使用动词开头
- 采用驼峰命名法
- 方法名应能清楚表达意图

```java
// 好的命名
boolean validateUserCredentials(String username, String password);
void sendWelcomeEmail(User user);
Order calculateOrderTotal(Order order);

// 避免的命名
void doSomething();  // 太模糊
void process();      // 不明确
```

## 变量命名规范

### 局部变量
- 使用驼峰命名法
- 名称应具有描述性

```java
// 好的例子
String userName = "john";
int userAge = 25;
List<User> userList = new ArrayList<>();

// 避免的例子
String s = "john";    // 不够描述性
int a = 25;           // 含义不明
List<User> list = new ArrayList<>(); // 太通用
```

### 成员变量
- 私有成员变量通常以下划线开头（可选）
- 或者直接使用驼峰命名

```java
public class User {
    private String userName;     // 推荐
    private int userAge;         // 推荐
    
    // 或者
    private String _userName;    // 可选风格
    private int _userAge;        // 可选风格
}
```

### 常量
- 全部大写字母
- 单词间用下划线分隔

```java
public static final String DEFAULT_USER_ROLE = "USER";
public static final int MAX_LOGIN_ATTEMPTS = 5;
public static final double TAX_RATE = 0.08;
```

## 数据库命名规范

### 表名
- 使用小写字母
- 单词间用下划线分隔
- 使用复数形式（可选，保持一致性）

```sql
-- 推荐
user_profiles
order_items
product_categories

-- 避免
UserProfiles  -- 驼峰命名不适合数据库
user-profile  -- 连字符可能引起问题
```

### 字段名
- 使用小写字母
- 单词间用下划线分隔
- 避免使用保留字

```sql
-- 推荐
user_id
created_time
is_active

-- 避免
userId      -- 驼峰命名
CreateTime  -- 大小写混合
order       -- SQL保留字
```

### 主键命名
```sql
-- 通用主键命名
id

-- 或者带表名前缀（适用于复合主键场景）
user_id
product_id
```

## 接口命名规范

### RESTful API路径
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    // GET /api/users - 获取用户列表
    @GetMapping
    public List<User> getUsers() { }
    
    // GET /api/users/{id} - 获取单个用户
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) { }
    
    // POST /api/users - 创建用户
    @PostMapping
    public User createUser(@RequestBody User user) { }
    
    // PUT /api/users/{id} - 更新用户
    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) { }
    
    // DELETE /api/users/{id} - 删除用户
    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) { }
}
```

## 枚举命名规范

```java
public enum UserRole {
    ADMIN("管理员"),
    USER("普通用户"),
    GUEST("访客");
    
    private final String description;
    
    UserRole(String description) {
        this.description = description;
    }
    
    public String getDescription() {
        return description;
    }
}
```

## 异常类命名

```java
// 业务异常
public class UserNotFoundException extends RuntimeException { }
public class InsufficientBalanceException extends BusinessException { }

// 系统异常
public class DatabaseConnectionException extends SystemException { }
public class NetworkTimeoutException extends SystemException { }
```

## 测试类命名

```java
// 测试类名 = 被测试类名 + Test
public class UserServiceTest { }

// 测试方法名 = test + 要测试的方法 + 场景描述
@Test
public void testFindUserById_withValidId_returnsUser() { }

@Test
public void testFindUserById_withInvalidId_throwsException() { }
```

## 配置文件命名

```
application.yml          # 主配置文件
application-dev.yml      # 开发环境配置
application-test.yml     # 测试环境配置
application-prod.yml     # 生产环境配置
```

## 日志命名规范

```java
// 在类中定义logger
private static final Logger logger = LoggerFactory.getLogger(UserService.class);

// 日志输出格式
logger.info("User {} logged in successfully", username);
logger.error("Failed to process order {}: {}", orderId, exception.getMessage());
```

## 最佳实践总结

### 1. 一致性原则
- 在整个项目中保持命名风格一致
- 团队内部制定并遵守统一的命名规范

### 2. 描述性原则
- 名称应该清楚表达其用途和含义
- 避免使用缩写，除非是广泛认知的缩写

### 3. 简洁性原则
- 在保证描述性的前提下尽量简洁
- 避免过长的名称影响可读性

### 4. 可搜索性原则
- 使用能够被IDE快速搜索的命名
- 避免使用过于通用的词汇

### 5. 避免匈牙利命名法
- 不要在变量名中包含类型信息
- 让IDE和现代开发工具来处理类型信息