# 一个电商平台案例项目
    本项目所有的安装包都在项目目录下的docs文件夹requeriments.txt中，你可以一次性全部下载；其他的资源也一并放到该目录
    本项目用到的所有静态文件比如css、images、js 等等全部包含在同名项目子文件中的static中。
    项目的所有的静态资源加载路径已经正确配置。
    所有的前后端接口文档请查看docs文件夹中的XX文件
## 一、开发模式
### (一)前后端不分离
    前后端不分离的开发模式，是为了提高搜索引擎排名，即SEO。特别是首页，详情页和列表页。
### (二)前后段分离
    后台管理系统采用前后端分离模式
## 二、主要的技术：
### （一）前端采用vue.js框架
    页面需要整体刷新：我们会选择使用Jinja2模板引擎来实现。
    页面需要局部刷新：我们会选择使用Vue.js来实现。
### （二）后端采用djano框架
### （三）jinja2模板引擎
    页面需要整体刷新：我们会选择使用Jinja2模板引擎来实现。
    本项目中，在meiduo_mall.utils.jinja2_env文件中编写模板引擎环境配置代码，并在meiduo_mall.settings.dev配置文件里进行配置。
### （四）Nginx服务器
#### 1.代理服务
    运用Nginx进行反向代理
#### 2.静态服务
    提供静态首页、商品详情页等静态页面
### （五）uwsgi服务器
    提供动态服务
### （六）后端服务
#### 1.mysql
    请确保安装过mysql，并建立一个名为meiduo的数据库。
    数据库建立后请在配置文件中进行相关的配置。
    注意：Django中操作MySQL数据库需要驱动程序MySQLdb，
    在工程同名子目录的__init__.py文件中，添加如下代码：1,from pymysql import install_as_MySQLdb 
    2,install_as_MySQLdb()
    sql脚本导入商品数据，脚本在docs中
    mysql -h127.0.0.1 -uroot -pmysql meiduo_mall < 文件路径/goods_data.sql
    对于数据库的优化，我们选择使用MySQL读写分离实现。涉及内容包括：1,数据库的主从同步以及数据库的读写分离。
    mysql的主从同步操作步骤：
    1，请确保已经安装了docker
    2，获取MySQL镜像 sudo docker load -i 文件路径/mysql_docker_5722.tar，docker文件请从docs文件中获取。
    3,对从机进行配置，为了快速配置，我们直接把主机的配置文件拷贝到从机中。
        步骤：   $ cd ~
                $ mkdir mysql_slave
                $ cd mysql_slave
                $ mkdir data
                $ cp -r /etc/mysql/mysql.conf.d ./、
      复制完成后，对~/mysql_slave/mysql.conf.d/mysqld.cnf文件进行编辑。
                # 从机端口号
                port = 8306
                # 关闭日志
                general_log = 0
                # 从机唯一编号
                server-id = 2
    4,运用docker安装mysql从机 创建root用户，密码是mysql
    sudo docker run --name mysql-slave -e MYSQL_ROOT_PASSWORD=mysql -d --network=host -v /home/python/mysql_slave/data:/var/lib/mysql -v /home/python/mysql_slave/mysql.conf.d:/etc/mysql/mysql.conf.d mysql:5.7.22
    5,测试从机是否创建成功
    mysql -uroot -pmysql -h 127.0.0.1 --port=8306
    6,对主机进行配置
    # 开启日志
    general_log_file = /var/log/mysql/mysql.log
    general_log = 1
    # 主机唯一编号
    server-id = 1
    # 二进制日志文件
    log_bin = /var/log/mysql/mysql-bin.log
    #重启主机
    sudo service mysql restart
    7,从机备份主机原有数据
    # 1. 收集主机原有数据
    $ mysqldump -uroot -pmysql --all-databases --lock-all-tables > ~/master_db.sql
    
    # 2. 从机复制主机原有数据
    $ mysql -uroot -pmysql -h127.0.0.1 --port=8306 < ~/master_db.sql
    8,创建同步数据的帐号
    # 登录到主机
    $ mysql –uroot –pmysql
    # 创建从机账号
    $ GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';
    # 刷新权限
    $ FLUSH PRIVILEGES;
    9,展示MySQL主机的二进制日志信息
    SHOW MASTER STATUS;
    10,主从链接
    # 登录到从机
    $ mysql -uroot -pmysql -h 127.0.0.1 --port=8306
    # 从机连接到主机
    $ change master to master_host='127.0.0.1', master_user='slave', master_password='slave',master_log_file='mysql-bin.000250', master_log_pos=990250;
    # 开启从机服务
    $ start slave;
    # 展示从机服务状态（你可以从主机中建立一个数据库然后从从机中查看是否有新建的数据库来进行测试。）
    $ show slave status \G
    11,最后不要忘记在django的配置文件中进行数据库相关配置的更新。
    
#### 2.redis
    本项目已经在dev的配置文件中进行了redis的相关配置。
#### 3.celery
#### 4.rabbitmq
#### 5.docker
    请自行百度安装docker
#### 6.fastDFS
    请先进行docker的安装
    1,解压本地资源镜像，文件在docs文件夹中
    sudo docker load -i 文件路径/fastdfs_docker.tar
    2,开启tracker容器，我们将 tracker 运行目录映射到宿主机的 /var/fdfs/tracker目录中
    sudo docker run -dit --name tracker --network=host -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker
    3,开启storage容器
    sudo docker run -dti --name storage --network=host -e TRACKER_SERVER=192.168.103.158:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
    TRACKER_SERVER=Tracker的ip地址:22122（Tracker的ip地址不要使用127.0.0.1）
    我们将 storage 运行目录映射到宿主机的 /var/fdfs/storage目录中。
    4,FastDFS客户端扩展在requriements中已经安装
    5,配置相关文件 meiduo_mall.utils.fastdfs.client.conf
    base_path=FastDFS客户端存放日志文件的目录
    tracker_server=运行Tracker服务的机器ip:22122
    6,将storage中的data删除（/var/fdfs/storage），用docs中的data替换(解压命令sudo tar -zxvf data.tar.gz)
    7,配置文件进行配置FDFS_BASE_URL
#### 7.elasticsearch
    1,解压教docs中本地镜像
    sudo docker load -i elasticsearch-ik-2.4.6_docker.tar
    2,将docs资料中的elasticsearc-2.4.6目录拷贝到home目录下。
    3,修改/home/python/elasticsearc-2.4.6/config/elasticsearch.yml第54行。更改ip地址为本机真实ip地址。
    4,sudo docker run -dti --name=elasticsearch --network=host -v /home/python/elasticsearch-2.4.6/config:/usr/share/elasticsearch/config delron/elasticsearch-ik:2.4.6-1.0
    5,在配置文件中配置Haystack为搜索引擎后端
    6,手动生成索引 python manage.py rebuild_index
#### 8.crontab
    对于首页进行定时静态化更新。
    在contents模块下的crons中封装了首页静态话的过程。
    django-crontab的相关配置工作已经完成。
### （七）外部接口
#### 1.容联云通讯
#### 2.qq互联
#### 3.支付宝
    支付宝的开放平台：https://open.alipay.com/platform/home.html
    Python支付宝SDK：https://github.com/fzlee/alipay/blob/master/README.zh-hans.md
    点击链接登录，阅读相关文档后即可。
## 三、项目主要模块
### （一）首页广告
### （二）用户模块
#### 1.注册
#### 2.登录
#### 3.个人信息
#### 4.收获地址
    将省市区三级联动数据导入数据库
    mysql -h数据库ip地址 -u数据库用户名 -p数据库密码 数据库 < areas.sql
    mysql -uroot -p meiduo_mall < areas.sql
    areas.sql在docs中
#### 5.我的订单
#### 6.修改密码
### （三）商品
    商品相关的模型类定义相对复杂，可以多花一些时间学习。
#### 1.商品列表
#### 2.商品搜索
#### 3.商品详情
### （四）购物
#### 1.购物车
#### 2.结算订单
#### 3.提交订单
#### 4.支付结果处理
#### 5.订单商品评价
### （五）后台管理（暂无）
#### 1.数据统计
#### 2.用户管理
#### 3.权限管理
#### 4.商品管理
#### 5.订单管理
### （六）第三方模块
#### 1.qq登录
#### 2.支付宝支付
#### 3.短信验证
## 注意技术点
### （一）配置Jinja2模板引擎
### （二）配置工程日志
### （三）自定义用户模型
###  (四）配置容联云通讯
### （五）celery
### （六）判断用户登录
### （七）添加验证邮箱
### （八）多帐号登录
### （九）图片的自定义存储方法
### （十）Haystack扩展
### （十一）面包屑导航
### （十二）IP的配置

