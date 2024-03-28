from telebot import types
from bot.handler_type import PluginInterface
from pybt.system import System
from pybt.sites import Sites
from bot.config import URL,KEY,HELP,File_HTEML,Admin
from bs4 import BeautifulSoup
import json
import re
class StartPlugin(PluginInterface):
    command = 'start'
    def handler_command(self,bot,message):
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('tcmiku的档案库', url='https://tcmiku.github.io')
        # 返回callback_data一个 1-64字节的数据
        itembtn2 = types.InlineKeyboardButton('帮助信息', callback_data=HELP)
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, f"启动成功欢迎用户: {message.chat.username}\n您的用户id为：{message.chat.id}", reply_markup=markup)

    def handler_back(self,bot,call):
        bot.send_message(call.message.chat.id, call.data)

    #权限判断机制
    def admin_start(self,message):
        if message.from_user.id in Admin:
            return True
        else:
            return False

    def handle_message(self,bot,message):
        if self.admin_start(message):
            #系统有关命令
            if message.text.startswith('!'):
                systeams = systeam(bot,message)
            elif message.text.startswith('#'):
                admin = authorityManagement(bot,message)
            elif message.text.startswith('*'):
                jumpurl = rehtml(bot,message)
                meatadd = meat(bot,message)
        else:
            bot.send_message(message.chat.id, "您没有该权限")

#权限管理机制
class authorityManagement:
    def __init__(self,bot,message):
        self.bot = bot
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.__admin_show()
        self.__admin_add()

    def __admin_show(self):
        if self.command == '管理员列表':
            self.bot.send_message(self.message.chat.id,Admin)

    def __admin_add(self):
        if self.command == '添加管理员':
            self.bot.send_message(self.message.chat.id,"请输入要加入的管理员id")
            self.bot.register_next_step_handler(self.message,self.__admin_add_nextstep)

    def __admin_add_nextstep(self,message):
       self.bot.send_chat_action(message.chat.id, 'typing')
       if message.text.isdigit():
           Admin.append(int(message.text))
           self.bot.send_message(message.chat.id, "添加成功")
       else:
           self.bot.send_message(message.chat.id,"添加失败")

class systeam:
    def __init__(self,bot,message):
        self.bot = bot
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.__git_systeam_cpu()
    def __git_systeam_cpu(self):
        bt = bt_api()
        if self.command == '获取系统信息':
            systeam = bt.bt_systeam()
            sys_out = f"当前系统为:{systeam['system']}\nCPU核心数:{systeam['cpuNum']}\n"
            self.bot.send_message(self.message.chat.id, sys_out)


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
    def __init__(self,bot,message):
        self.message = message
        self.bot = bot
        self.command = message.text.split(' ', 1)[0][1:]
        self.command_user()

    def command_user(self):
        if self.command == "改跳转":
            self.bot.send_message(self.message.chat.id,"请输入要修改的网页地址: ")
            self.bot.register_next_step_handler(self.message,self.__file_html_in)

    def __file_html_in(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url_in = message.text
        self.bot.send_message(message.chat.id, "请输入要跳转的网页: ")
        self.bot.register_next_step_handler(message,self.__url_html_in)

    def __url_html_in(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url = message.text
        self.urladd()
        self.bot.send_message(message.chat.id,"修改成功")

    def urladd(self):
        self.file_html = f'{File_HTEML}/{self.url_in}.html'
        self.openhtml()
        self.db4()
        self.__server_html()

    def openhtml(self):
        with open(self.file_html,mode='r',encoding="utf-8") as f:
            self.html_content = f.read()

    def db4(self):
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
                new_url = self.url
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



class meat:
    def __init__(self,bot,message):
        self.bot = bot
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.command_user()

    def command_user(self):
        if self.command == "加像素":
            self.bot.send_message(self.message.chat.id, "请输入要修改的网页地址: ")
            self.bot.register_next_step_handler(self.message, self.__file_html_in)

    def __file_html_in(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url_in = message.text
        self.bot.send_message(message.chat.id, "请输入要添加的像素id: ")
        self.bot.register_next_step_handler(message,self.__url_html_in)

    def __url_html_in(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.meat = message.text
        self.urladd()
        self.bot.send_message(message.chat.id, "修改成功")

    def urladd(self):
        self.file_html = f'{File_HTEML}/{self.url_in}.html'
        self.openhtml()
        self.bs4()
        self.__server_html()

    def openhtml(self):
        with open(self.file_html,mode='r',encoding="utf-8") as f:
            self.html_content = f.read()

    def bs4(self):
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(self.html_content, 'html.parser')

        # 查找所有的<script>标签
        script_tags = soup.find_all('script')

        # 遍历每个<script>标签并修改fbq('init', '原像素ID')
        for script_tag in script_tags:
            # 获取<script>标签的文本内容
            script_content = script_tag.string
            if script_content:
                # 使用正则表达式替换fbq('init', '原像素ID')中的ID
                pattern = r"fbq\('init', '\d+'\);"
                new_content = re.sub(pattern, f"fbq('init', '{self.meat}');", script_content)
                # 将修改后的内容设置回<script>标签
                script_tag.string.replace_with(BeautifulSoup(new_content, 'html.parser').string)

                # 查找<noscript>标签并修改其中的src属性
        noscript_tags = soup.find_all('noscript')
        for noscript_tag in noscript_tags:
            img_tags = noscript_tag.find_all('img')
            for img_tag in img_tags:
                src_value = img_tag.get('src')
                if src_value:
                    # 使用字符串替换修改src属性中的ID
                    new_src_value = src_value.replace('921554562711093', self.meat)
                    img_tag['src'] = self.meat

                    # 将修改后的内容编码为字符串
        modified_html_content = str(soup)
        self.html_txt = modified_html_content


    def __server_html(self):
        html = self.html_txt
        with open(self.file_html,'w') as file:
            file.write(html)

if __name__ == '__main__':
    # rehtml操作示例
    # html = rehtml('en/eng',"https://www.baidu.com")
    # bt_api操作示例
    bt = bt_api()