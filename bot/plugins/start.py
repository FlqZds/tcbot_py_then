from telebot import types
from bot.handler_type import PluginInterface
from pybt.system import System
from bot.config import URL,KEY
class StartPlugin(PluginInterface):
    command = 'start'
    def handler_command(self,bot,message):
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('tcmiku的档案库', url='https://tcmiku.github.io')
        # 返回callback_data一个 1-64字节的数据
        itembtn2 = types.InlineKeyboardButton('帮助信息', callback_data="各种帮助信息")
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, f"启动成功欢迎用户: {message.chat.username}", reply_markup=markup)

    def handler_back(self,bot,call):
        bot.send_message(call.message.chat.id, call.data)


    def handle_message(self,bot,message):
        if message.text.startswith('!'):
            command = message.text.split(' ', 1)[0][1:]
            bt = bt_api()
            if command == '获取系统信息':
                systeam = bt.bt_systeam()
                sys_out=f"当前系统为 {systeam['system']}\nCPU核心数 {systeam['cpuNum']}\n"
                bot.send_message(message.chat.id,sys_out)

class bt_api:
    def __init__(self):
       self.Url = URL
       self.Key = KEY

    def bt_systeam(self):
        systeam = System(self.Url,self.Key)
        sys = systeam.get_system_total()
        return sys