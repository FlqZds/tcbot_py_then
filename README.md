# TcBot(插件驱动的TelegrmBOT)
## 使用说明
使用`pip install -r ./requirements.txt`下载程序依赖
在```mian.py```中启动即可
## 功能列表
| 系统相关       | 2024/4/9 |       |
|------------|----------|-------|
| 功能         | 完成情况     | 使用权限  |
| 用户列表       | √        | admin |
| 管理员列表      | √        | admin |
| 添加用户       | √        | admin |
| 添加管理员      | √        | admin |
| 删除用户       | √        | admin |
| 删除管理员      | √        | admin |
| 查看已有HTML目录 | √        | user  |
| 查看落地页网址    | √        | user  |
| 复制网页模板     | √        | user  |
| 查看落地页网址    | √        | user  |

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