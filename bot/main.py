import telebot
import os
import config
import importlib
from config import TOKEN,Banner
from telebot import types
import time
import logging
import sys
import platform

#玄学加载
print(Banner)
# 获取操作系统名称
os_name = platform.system()
if platform.system() == "Windows":
    print(f"\033[34mWindows系统启动     {time.ctime()}\033[m")
elif platform.system() == 'Linux':
    print(f"\033[34mlinux系统启动       {time.ctime()}\33[m")
    sys.path.append('/www/wwwroot/TcBot')  #linux加载软件包的路径

#插件目录
PLUGIN_DIR = 'plugins'
#初始化机器人
if config.TOKEN != "":
    bot = telebot.TeleBot(TOKEN)
else:
    print("错误!!")
plugins = []
# 加载插件目录
for filename in os.listdir(os.path.join(os.path.dirname(__file__), PLUGIN_DIR)):
    if filename.endswith('.py'):
        #切断.py后缀获得文件名
        module_name = filename[:-3]
        #动态导入plugins中插件
        module = importlib.import_module(f'.{PLUGIN_DIR}.{module_name}', 'bot')
        try:
            #获取插件中以文件首字母大写加Plugin的类
            plugin_class = getattr(module, f'{module_name.capitalize()}Plugin')
            #将获取到的类放到插件列表里
            plugins.append(plugin_class())
            print(f'\033[32m加载 plugin: {module_name} 成功  {time.ctime()} \033[m')
        except Exception as e:
            print(f'\033[31m加载 plugin: {module_name} 失败  {time.ctime()}\033[m')

print(f"\033[32m模块加载完成   {time.ctime()}\033[m")

#获取机器人所有可执行的命令
commands = []
for plugin in plugins:
    commands.append(plugin.command)

#处理机器人所有命令
@bot.message_handler(func=lambda m: True)
def handler_all_mod(message):
    if message.text.startswith('/'):
        #去掉开头的/留下命令本身
        command  = message.text.split(' ',1)[0][1:]
        for plugin in plugins:
            if plugin.command == command:
                plugin.handler_command(bot,message)
    else:
        for plugin in plugins:
            plugin.handle_message(bot, message)


#内嵌键盘中callback_data的处理
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    for plugin in plugins:
        if hasattr(plugin,'handler_back'):
            plugin.handler_back(bot,call)


#运行机器人
try:
    print(f"\033[34m机器人运行成功  {time.ctime()} \033[m")
    print(f"目前可使用命令{commands}")
    bot.polling()
except Exception as e:
     print(f"\033[31m出现致命错误 {e}            {time.ctime()}\033[m")
     bot.polling()