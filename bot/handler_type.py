class PluginInterface:
    command = ''

    #用于处理普通文本消息
    def handle_message(self,bot,message):
        pass

    #用于处理命令
    def handler_command(self,bot,message):
        pass

    def handler_back(self,bot,call):
        pass