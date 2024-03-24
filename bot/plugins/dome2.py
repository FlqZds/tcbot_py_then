from bot.handler_type import PluginInterface
class Dome2Plugin(PluginInterface):
    command = 'help'
    def handle_message(self,bot,message):
        bot.send_message(message.chat.id,'正常文本处理')