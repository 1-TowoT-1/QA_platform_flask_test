# PostgreSQL基本使用

### 一、数据库的结构
+ 服务器（Server）
├── 数据库（Database）
│   ├── 表空间（Tablespace）
│   │   └── 存储物理文件（Data Files）
│   ├── 模式/模式空间（Schema）
│   │   ├── 表（Table）
│   │   │   ├── 列（Column）
│   │   │   ├── 行（Row / Record）
│   │   │   └── 索引（Index）
│   │   ├── 视图（View）
│   │   ├── 函数（Function / Stored Procedure）
│   │   ├── 触发器（Trigger）
│   │   └── 序列（Sequence）
│   └── 用户 & 权限（User / Roles & Privileges）
└── 连接 & 监听（Connection & Listener）

| 层级 | 含义 |
|-------|-------|
服务器 (Server) | 一台PostgreSQL实例或服务器。
数据库 (Database) | 在服务器上，管理自己的一套数据集合。不同数据库之间隔离。
表空间 (Tablespace) | 物理存储位置，可以理解为磁盘上目录或文件夹。默认表空间通常是pg_default。
模式 (Schema) | 数据库内部的逻辑分类（命名空间），比如public就是默认schema。
表 (Table) | 具体存储数据的地方，每张表有若干列和行。
列 (Column) | 定义字段，比如id，name，age。
行 (Row) | 具体的数据记录。
索引 (Index) | 加速查询的数据结构，比如B树索引。
视图 (View) | 查询的结果快照（虚拟表）。
函数/存储过程 (Function/Procedure) | 封装的SQL逻辑。
触发器 (Trigger) | 在某些操作（插入、更新等）发生时自动触发执行的逻辑。
序列 (Sequence) | 生成自增ID的机制。
用户 (User/Roles) | 管理数据库权限的人或应用程序账号。


### 二、vscode接入、postgres新用户添加问题
1. 本地vscode使用conda安装了虚拟环境，开始用的是postgres自己的超级账户，需要切换到postgres的账户：`sudo su - postgres`
2. 创建新用户后，切换登录用户会遇到：
```sql
psql -U username
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  Peer authentication failed for user "username"
```
+ 这是由于postgreSQL默认的认证方式是本机peer认证，如果需要进行账户密码认证需要更改配置文件 `pg_hba.conf`，更改peer认证方式为密码认证；
+ 更改配置完成需要重启pgSQL服务，切换到本机账户，重启服务：`sudo service postgresql restart`；重进账户即可完成账户登录；
+ 新账户登录命令：`psql -U usrename -d database` 需要指定的数据库，\dt可以查看该数据库内的所有表信息。但是可能因为没有设置权限无法读取和操作，之后可以使用postgres默认管理账户进行权限赋予。

### 三、wsl连接本机pgadmin
1. psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432 （-h服务器、-U用户民、-d数据库、-p端口号）
2. psql (最开始连接数据库，默认用户和数据库都是postgres)
3. pgql进入默认数据库后，\password可以设置密码
4. wsl连接本地数据库需要注意填写IP支持:
    + 查看 wsl 的IP：ip addr show eth0
    + 使用 `psql -U postgres -c "SHOW config_file; SHOW hba_file; SHOW ident_file;"` 显示默认配置文件postgresql.conf（主配置文件）、pg_hba.conf（客户端认证配置文件） 、ident_file（用户名映射配置文件）；
    + 在 `postgresql.conf` 设置 listen_addresses = '*' 监听所有网络接口；
    + 在 `pg_hba.conf` 设置需要支持的主机IP；
    + 在本机使用 pgadmin 添加相应配置即可.
    + 由于pgadmin是postgreSQL官方的支持，特殊化强烈，这里使用`DBeavar`来控制postgresql的各种数据库，操作跟上述一样。

### 四、基本操作
1. `\l=\list`：显示数据库列表
2. `\c database`：切换到对应数据库
3. `\dt`：查看数据库中所有表
4. `\dt+`：查看数据库所有表以及额外信息
5. `\q`：退出
6. `\?`：查看psql命令列表
7. `\h`：查看SQL命令解释，例如\h select
8. `\du`：列出所有用户

### 五、Schema
1. Schema 基本概念
    + Schema 是 PostgreSQL 中的命名空间，用于组织数据库对象（如表、视图、函数等）。它类似于操作系统中的目录结构，允许你将数据库对象分组管理。
    + 主要特点：
        + 一个数据库可以包含多个 schema
        + 每个 schema 可以包含表、视图、函数等数据库对象
        + 不同 schema 中的对象可以同名而不会冲突
        + 提供逻辑分组和权限控制的能力

2. 默认 Schema
    + PostgreSQL 安装后会自动创建以下 schema：
    + public - 默认 schema，所有新建对象默认放在这里
    + pg_catalog - 包含系统表和所有内置数据类型、函数等
    + information_schema - 提供标准化方式访问数据库元数据

3. Schema 的作用
    + 主要优势：
        + 多用户环境管理：不同用户可以拥有各自的 schema，互不干扰
        + 第三方应用集成：不同应用可以有自己的 schema，避免表名冲突
        + 逻辑分组：将相关表组织在一起，提高可管理性
        + 权限控制：可以在 schema 级别设置权限


### 六、如何备份PostgreSQL数据库
1. 备份数据库：`pg_dump`
2. 备份所有数据库：`pg_dumpall`
3. 还原数据库：`pg_restore`


### 七、用户管理
+ 用户授权：
    1. 创建带密码的用户：`CREATE USER username WITH PASSWORD 'yourpassword';`
    2. 授予登录权限（默认已开启）：`ALTER USER username WITH SUPERUSER;`
    3. 授予超级用户权限（慎用）：`ALTER USER username WITH SUPERUSER;`
    4. 授予创建数据库权限：`ALTER USER username CREATEDB;`
    5. 授予特定数据库访问权限：`GRANT CONNECT ON DATABASE your_db TO username;`
    6. 授予某个 schema 使用权限：`GRANT USAGE ON SCHEMA public TO username;`
    7. 授予表的操作权限（查询、插入等）：`GRANT SELECT, INSERT ON table_name TO username;`
+ 删除用户：
    1. 移交拥有的对象（防止报错）：`REASSIGN OWNED BY username TO new_owner;`
    2. 删除该用户拥有的所有权限和对象：`DROP OWNED BY username;`
    3. 删除用户本身：`DROP USER username;`


### 八、服务管理
+ postgresql作为服务运行在后台，需要手动管理服务的开启关闭。
+ 使用命令重启/关闭postgresql服务：
    1. sudo service postgresql start
    2. sudo service postgresql stop
    3. sudo service postgresql status