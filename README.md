# TcBot(插件驱动的TelegrmBOT)
## 使用说明

## 插件编写说明
1. 插件必须位于`bot/plugins`文件夹中
2. 插件中必须有一个以插件名首字母大写加Plugin的类 (例如:插件名叫`dome`那么其中必须有一个名为`DomePlugin`的类)
3. 插件必须继承`bot.hander_tyoe`中的`PluginInterface`类
4. 插件可以通过`command`来设置命令```command = "插件命令"```
5. 插件中处理机器人命令时都需要重写```handler_type.py```中的函数
6. 插件需要的固定设置尽量在```config.py```中获取