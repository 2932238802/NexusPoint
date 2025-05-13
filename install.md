### 项目计划书

## 项目运行

```shell
cd NexApp
py manage.py runserver
```


## 项目功能
- 登录和注册功能
- 网址搜索 输入的时候 自动爬取
- 

## 大致框图
![alt text](install.png)

## 大致项目结构
myproject/                  # 项目根目录
├── manage.py               # Django 命令行工具
├── myproject/              # 内层项目配置目录 (通常与项目根目录同名)
│   ├── __init__.py         # 标识这是一个 Python 包
│   ├── asgi.py             # ASGI 入口文件 (异步 web server)
│   ├── settings.py         # 项目全局配置
│   ├── urls.py             # 项目主 URL 配置
│   └── wsgi.py             # WSGI 入口文件 (同步 web server)
├── myapp/                  # 一个 Django 应用目录 (可以有多个应用)
│   ├── migrations/         # 数据库迁移文件目录
│   │   ├── __init__.py
│   │   └── 0001_initial.py # 示例迁移文件
│   ├── __init__.py
│   ├── admin.py            # 管理后台配置
│   ├── apps.py             # 应用配置
│   ├── models.py           # 数据库模型定义
│   ├── tests.py            # 应用测试文件
│   └── views.py            # 视图函数/类定义
├── templates/              # (可选) 项目级模板目录
│   └── base.html           # 基础模板示例
├── static/                 # (可选) 项目级静态文件目录
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── script.js
├── .venv/                  # (可选) 虚拟环境目录
├── requirements.txt        # (可选) 项目依赖列表
└── .gitignore              # (可选) Git 版本控制忽略文件