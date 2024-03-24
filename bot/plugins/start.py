from telebot import types
from bot.handler_type import PluginInterface
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