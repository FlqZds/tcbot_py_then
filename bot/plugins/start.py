from telebot import types
from bot.handler_type import PluginInterface
from pybt.system import System
from pybt.sites import Sites
from bot.config import URL,KEY,HELP,File_HTEML
from bs4 import BeautifulSoup
import re
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

class rehtml():
    def __init__(self,refile,url):
        self.file_html = f'{File_HTEML}/{refile}.html'
        self.openhtml()
        self.db4(url= url)
        self.__server_html()


    def openhtml(self):
        with open(self.file_html,mode='r',encoding="utf-8") as f:
            self.html_content = f.read()

    def db4(self,url):
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(self.html_content, 'html.parser')

        # 找到所有的<script>标签
        script_tags = soup.find_all('script')

        # 遍历每个<script>标签并修改其内容
        for script_tag in script_tags:
            # 获取<script>标签的文本内容
            script_content = script_tag.string
            # 如果script_content存在，则尝试替换其中的window.open调用
            if script_content:
                # 定义你想要替换的新URL
                new_url = url

                # 使用正则表达式替换window.open中的URL
                # 注意：这只是一个简单的示例，对于复杂的JavaScript代码可能需要更精细的处理
                pattern = r"window\.open\('([^']*)'\);"
                modified_content = re.sub(pattern, f"window.open('{new_url}');", script_content)
                # 将修改后的内容设置回<script>标签
                script_tag.string.replace_with(modified_content)
        # 将修改后的内容编码为字符串
        modified_html_content = soup.encode('utf-8')
        self.html_txt = modified_html_content


    #保存
    def __server_html(self):
        html = self.html_txt
        with open(self.file_html,'wb') as file:
            file.write(html)



if __name__ == '__main__':
    html = rehtml('en/eng',"https://www.baidu.com")