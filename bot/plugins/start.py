from telebot import types
from bot.handler_type import PluginInterface
from pybt.system import System
from pybt.sites import Sites
from bot.config import URL,KEY,HELP
class StartPlugin(PluginInterface):
    command = 'start'
    def handler_command(self,bot,message):
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('tcmiku的档案库', url='https://tcmiku.github.io')
        # 返回callback_data一个 1-64字节的数据
        itembtn2 = types.InlineKeyboardButton('帮助信息', callback_data=HELP)
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
                sys_out=f"当前系统为:{systeam['system']}\nCPU核心数:{systeam['cpuNum']}\n"
                bot.send_message(message.chat.id,sys_out)
        elif message.text.startswith('#'):
            command = message.text.split(' ',1)[0][1:]

class bt_api:
    def __init__(self):
       self.Url = URL
       self.Key = KEY

    def bt_systeam(self):
        systeam_api = System(self.Url,self.Key)
        sys = systeam_api.get_system_total()
        return sys

    def bt_web(self):
        websites = Sites(self.Url,self.Key)
        webname = websites.websites()
        print(webname)
        web_index = websites.web_get_index(webname['data'][0]['name'])
        print(web_index)

if __name__ == '__main__':
    bt = bt_api()
    bt.bt_web()