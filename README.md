<<<<<<< HEAD
# TcBot(插件驱动的TelegrmBOT)
## 使用说明
使用`pip install -r ./requirements.txt`下载程序依赖
在```mian.py```中启动即可
## 功能列表
| 系统相关       |  |       |  2024/4/9  |
|------------|----------|-------|-------|
| 功能         | 完成情况     |功能描述| 使用权限  |
| 用户列表       | √        |输出已有用户列表| admin |
| 管理员列表      | √        |输出已有管理员列表| admin |
| 添加用户       | √        |添加用户| admin |
| 添加管理员      | √        |添加管理员| admin |
| 删除用户       | √        |删除用户| admin |
| 删除管理员      | √        |删除管理员| admin |
| 查看已有模板路径 | √        |输出已有模板网站的路径| user  |
| 查看落地页网址    | √        |输出当前用户已有的落地页路径| user  |
| 复制网页模板     | √        |为当前用户复制指定的模板网页| user  |
| 改跳转 | √        |将指定网站的跳转链接改为目标链接| user  |
| 加像素 | √        |为指定网页添加一个像素，像素id由用户指定| user  |
| 删除网页 | √        |删除当前用户落地页路径下的用户落地页| user  |
| 像素列表 | WIP     |输出当前用户落地页中所有的像素id| user  |

| BOT相关   | 2024/4/8     |
|---------|--------------|
| 当前可操作命令 | 已使用外置键盘的方式实现 |
| 命令提示    | 内置命令提示       |
| BOT外置键盘 | 根据需要添加       |
| BOT内置键盘 | 根据需要添加       |


|高防|2024/4/7(功能未构建)|
|---|---|
|不同国家访问限制|暂无|

|粉丝群|2024/4/7(功能未构建)|
|---|---|
|计数|未构建|
|监控|未构建|

| 落地页相关  | 2024/4/3 |
|--------|----------|
| 功能     | 完成情况     |
| 改跳转    | √        |
| 加像素    | √        |
| 删像素    | 功能未构建    |
| 查看像素列表 | 构建中      |

|数据库相关| 2024/4/3(功能未构建) |
|---|-----------------|
|用户存储|暂无|
|文件存储|暂无|

|linux运维相关|2024/4/7|
|---|---|
|错误提醒|暂无|
|高防设置|暂无|

## 插件编写说明
1. 插件必须位于`bot/plugins`文件夹中
2. 插件中必须有一个以插件名首字母大写加Plugin的类 (例如:插件名叫`dome`那么其中必须有一个名为`DomePlugin`的类)
3. 插件必须继承`bot.hander_tyoe`中的`PluginInterface`类
4. 插件可以通过`command`来设置命令```command = "插件命令"```
5. 插件中处理机器人命令时都需要重写```handler_type.py```中的函数
6. 插件需要的固定设置尽量在```config.py```中获取


## python编写说明
1. 每个函数都要加self
2. self在类中代表全局，未加的变量就是局部变量
3. 目录结构是以 plugins文件夹下的  .py  文件来 作为源目录的
4. 

=======
# tcbot_py_then
just tcbot
>>>>>>> 54cf55d533e9435b732c12d7de35202380331eaa
