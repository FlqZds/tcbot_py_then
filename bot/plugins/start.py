from email import message
from telebot import types
import os
import shutil
from bot.handler_type import PluginInterface
from pybt.system import System
from pybt.sites import Sites
from bot.config import URL, KEY, HELP, File_HTEML, DateFile, Template_HTML, Domain, IDFile
from bs4 import BeautifulSoup
import json
import re
import time


class StartPlugin(PluginInterface):
    """
        机器人命令入口
    """
    command = 'start'

    def handler_command(self, bot, message):
        markup = types.InlineKeyboardMarkup()
        # itembtn1 = types.InlineKeyboardButton('tcmiku的档案库', url='https://tcmiku.github.io')
        # 返回callback_data一个 1-64字节的数据
        itembtn2 = types.InlineKeyboardButton(text='帮助信息', callback_data="help")
        markup.add(itembtn2)  #内置键盘启动
        # 根据当前用户id创建家目录
        page = userpage(bot, message)
        page.create_dir()


        # 外置键盘设置
        show_button = button()
        show_button.open_admin(bot, message)
        bot.send_message(message.chat.id, f"启动成功欢迎用户: {message.chat.username}\n您的用户id为：{message.chat.id}",
                         reply_markup=markup)

    def handler_back(self, bot, call):
        bot.send_message(call.message.chat.id, HELP)

    # 权限判断机制
    def admin_start(self, bot, message):

        with open(file=DateFile, mode='r', encoding='utf-8') as date:
            admin_date = json.load(date)
        admin_date
        if message.from_user.id in admin_date["Admin"]:
            return "admin"
        elif message.from_user.id in admin_date['user']:
            return "user"
        else:
            return None

    def handle_message(self, bot, message):
        date = self.admin_start(bot, message)
        if date == 'admin':
            # 管理员可使用命令
            # 系统有关命令
            if message.text.startswith('!'):
                systeams = systeam(bot, message)
            elif message.text.startswith('#'):
                admin = authorityManagement(bot, message)   # 管理员就#
            elif message.text.startswith('*'):   # 做的事
                jumpurl = rehtml(bot, message)
                meatadd = meat(bot, message)
                copy_htmls = webModules(bot, message)
                copy_enghtml = html_copy(bot, message)
                chang = changeWeb(bot,message)
                var = PrintText(bot, message)
        elif date == 'user':                                # 用户就*
            # 用户可使用命令
            if message.text.startswith('*'):
                jumpurl = rehtml(bot, message)
                meatadd = meat(bot, message)
                copy_htmls = webModules(bot, message)
                copy_enghtml = html_copy(bot, message)
                chang = changeWeb(bot, message)
                var = PrintText(bot, message)
        else:
            bot.send_message(message.chat.id, "您没有该权限")


# 外置键盘控制
class button:
    """
    外置键盘控制
    """

    def __read_date(self):
        self.DateFile = DateFile
        with open(file=self.DateFile, mode='r', encoding='utf-8') as date:
            self.admin_date = json.load(date)
        self.admin_date

    def open_admin(self, bot, message):
        self.__read_date()
        markup = types.ReplyKeyboardMarkup(row_width=3)  # row_width可以控制外置键盘一排放几个
        itembtn1 = types.KeyboardButton("#管理员列表")
        itembtn2 = types.KeyboardButton("#用户列表")
        itembtn3 = types.KeyboardButton("#添加管理员")
        itembtn4 = types.KeyboardButton("#添加用户")
        itembtn5 = types.KeyboardButton("#删除管理员")
        itembtn6 = types.KeyboardButton("#删除用户")
        itembtn7 = types.KeyboardButton("*查看模板路径")
        itembtn8 = types.KeyboardButton("*复制网页模板")
        itembtn9 = types.KeyboardButton("*复制用户网页")
        itembtn10 = types.KeyboardButton("*删除网页")
        itembtn11 = types.KeyboardButton("*查看落地页网址")
        itembtn12 = types.KeyboardButton("*改跳转")
        itembtn13 = types.KeyboardButton("*加像素")
        itembtn14 = types.KeyboardButton("*像素列表")
        itembtn15 = types.KeyboardButton("*模板切换")
        itembtn16 = types.KeyboardButton("*输出")
        if message.chat.id in self.admin_date["Admin"]:
            print(f"管理员{message.chat.username}启动外置键盘     {time.ctime()}")
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9,
                       itembtn10, itembtn11, itembtn12, itembtn13, itembtn14,itembtn15,itembtn16)
        elif message.chat.id in self.admin_date["user"]:
            print(f"用户{message.chat.username}启动外置键盘     {time.ctime()}")
            markup.add(itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12, itembtn13, itembtn14,itembtn15,itembtn16)
        bot.send_message(message.chat.id, "外置键盘启动", reply_markup=markup)


# 权限管理机制
class authorityManagement:
    """
    权限管理机制
    """

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.DateFile = DateFile
        self.__read_admin()
        self.__admin_del()
        self.__user_del()
        self.__user_show()
        self.__admin_show()
        self.__admin_add()
        self.__user_add()

    def __read_admin(self):
        with open(file=self.DateFile, mode='r', encoding='utf-8') as date:
            self.admin_date = json.load(date)


    def __admin_show(self):
        if self.command == '管理员列表':
            date = str(self.admin_date['Admin'])
            date = date.strip("[]").replace(",", "\n")
            self.bot.send_message(self.message.chat.id, f"现有管理员id:\n{date}")

    def __user_show(self):
        if self.command == '用户列表':
            date = str(self.admin_date['user'])
            date = date.strip("[]").replace(",", "\n")
            self.bot.send_message(self.message.chat.id, f"现有用户id:\n{date}")

    def __user_del(self):
        if self.command == '删除用户':
            self.bot.send_message(self.message.chat.id, "请输入要删除的用户id")
            self.bot.register_next_step_handler(self.message, self.__user_del_nextstep)

    def __user_del_nextstep(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        if message.text.isdigit() and int(message.text) in self.admin_date['user']:
            self.admin_date['user'].remove(int(message.text))
            self.__server_date()
            self.bot.send_message(message.chat.id, "删除成功")
            print(f"删除用户{message.text}成功      {time.ctime()}")
        else:
            self.bot.send_message(message.chat.id, "删除失败")
            print(f"删除用户{message.text}失败     {time.ctime()}")

    def __admin_del(self):
        if self.command == '删除管理员':
            self.bot.send_message(self.message.chat.id, "请输入要删除的管理员id")
            self.bot.register_next_step_handler(self.message, self.__admin_del_nextstep)

    def __admin_del_nextstep(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        if message.text.isdigit() and int(message.text) in self.admin_date['Admin']:
            self.admin_date['Admin'].remove(int(message.text))
            self.__server_date()
            self.bot.send_message(message.chat.id, "删除成功")
            print(f"删除管理员{message.text}成功     {time.ctime()}")
        else:
            self.bot.send_message(message.chat.id, "删除失败")
            print(f"删除管理员{message.text}失败     {time.ctime()}")

    def __admin_add(self):
        if self.command == '添加管理员':
            self.bot.send_message(self.message.chat.id, "请输入要加入的管理员id")
            self.bot.register_next_step_handler(self.message, self.__admin_add_nextstep)

    def __user_add(self):
        if self.command == '添加用户':
            self.bot.send_message(self.message.chat.id, "请输入要加入的用户id")
            self.bot.register_next_step_handler(self.message, self.__user_add_nextstep)

    def __user_add_nextstep(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        if message.text.isdigit():
            self.admin_date['user'].append(int(message.text))
            self.__server_date()
            self.bot.send_message(message.chat.id, "添加成功")
            print(f'添加用户{message.text}      {time.ctime()}')
        else:
            self.bot.send_message(message.chat.id, "添加失败,您输入的id不是纯数字")
            print(f'用户{message.text}添加失败      {time.ctime()}')

    def __admin_add_nextstep(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        if message.text.isdigit():
            self.admin_date['Admin'].append(int(message.text))
            self.__server_date()
            self.bot.send_message(message.chat.id, "添加成功")
            print(f'添加管理员{message.text}     {time.ctime()}')
        else:
            self.bot.send_message(message.chat.id, "添加失败,您输入的id不是纯数字")
            print(f'管理员{message.text}添加失败     {time.ctime()}')

    def __server_date(self):
        with open(self.DateFile, mode='w', encoding='utf-8') as f:
            json.dump(self.admin_date, f, ensure_ascii=False)

class PrintText:
    def __init__(self,bot,message):
        self.message = message
        self.bot = bot
        self.id = message.chat.id
        self.command = message.text.split()[0][1:]
        self.print_message()
    def print_message(self):
        if self.command=='输出':
            self.bot.send_message(self.message.chat.id,f"输出的信息为您的id:{self.message.chat.id}")
            self.bot.send_message(self.message.chat.id, f"操作结束，请选择您的下一个插件")

class rehtml():
    def __init__(self, bot, message):
        self.message = message
        self.bot = bot
        self.id = message.chat.id
        self.command = message.text.split(' ', 1)[0][1:]
        self.command_user()
        self.__file_html()
        self.server_web_html_command()

    def __file_html(self):
        if self.command == '查看模板路径':
            self.template_html_def()

    def template_html_def(self):
        file = template_html(self.message)
        lists = file.splicing()
        lists = str(lists)
        cleaned_string = lists.strip("[]").replace(",", "\n")
        self.bot.send_message(self.message.chat.id, f"现有模板路径:\n{cleaned_string}")

    def web_file(self):
        file = file_html(self.message)
        lists = file.splicing()
        lists = str(lists)
        cleaned_string = lists.strip("[]").replace(",", "\n")
        self.bot.send_message(self.message.chat.id, f"现有网站路径:\n{cleaned_string}")

    def server_web_html_command(self):
        if self.command == "查看落地页网址":

            try:
                self.server_web_html()
                str_html = str(self.server_web)
                str_html = str_html.strip("[]").replace(",", "\n")
                self.bot.send_message(self.message.chat.id, f"落地页网址:\n{str_html}")
            except:
                print(f"用户未初始化      {time.ctime()}")
                self.bot.send_message(self.message.chat.id, "请输入/start创建路径")

    def server_web_html(self):
        file = file_html(self.message)
        lists = file.splicing()
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.server_web = []
        for list in lists:
            web_file_html = f'{Domain}/{self.val}/{list}.html'
            self.server_web.append(web_file_html)

    def command_user(self):
        if self.command == "改跳转":
            self.web_file()
            self.bot.send_message(self.message.chat.id, "请输入要修改的网页路径: ")
            self.bot.register_next_step_handler(self.message, self.__file_html_in)

    def __file_html_in(self, message):
        file = file_html(message)
        lists = file.splicing()
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url_in = message.text
        if self.url_in in lists:
            self.bot.send_message(message.chat.id, "请输入要跳转的网页: ")
            self.bot.register_next_step_handler(message, self.__url_html_in)
        else:
            self.bot.send_message(message.chat.id, "没有该网页路径")

    def __url_html_in(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url = message.text
        self.urladd()
        self.bot.send_message(message.chat.id, "修改成功")

    def urladd(self):
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.file_html = f'{File_HTEML}/{self.val}/{self.url_in}.html'
        self.openhtml()
        self.db4()
        self.__server_html()

    def openhtml(self):
        with open(self.file_html, mode='r', encoding="utf-8") as f:
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

    # 保存
    def __server_html(self):
        html = self.html_txt
        with open(self.file_html, 'wb') as file:
            file.write(html)


class meat:
    def __init__(self, bot, message):
        self.bot = bot
        self.id = message.chat.id
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.command_user()
        self.mate_list()

    def command_user(self):
        if self.command == "加像素":
            web = rehtml(self.bot, self.message)
            web.web_file()
            self.bot.send_message(self.message.chat.id, "请输入要修改的网页路径: ")
            self.bot.register_next_step_handler(self.message, self.__file_html_in)

    def mate_list(self):
        if self.command == "像素列表":
            self.json_open()
            try:
                date = str(self.intjson['mate'][f'{self.id}'])
                # 不显示前七个字符
                if date is None:
                    self.bot.send_message(self.message.chat.id, '像素列表为空')
                else:
                    date = date.strip("{}").replace(",", "\n").replace("'", "").replace("{", "").replace("}", "").replace("0:","")
                    self.bot.send_message(self.message.chat.id,f"目前已有像素:\n{date}")
            except Exception as e:
                print(f'用户可能未添加过像素{e}           {time.ctime()}')
                self.bot.send_message(self.message.chat.id, '像素列表为空')
    def __file_html_in(self, message):
        file = file_html(message)
        lists = file.splicing()
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url_in = message.text
        if self.url_in in lists:
            self.bot.send_message(message.chat.id, "请输入要添加的像素id: ")
            self.bot.register_next_step_handler(message, self.__url_html_in)
        else:
            self.bot.send_message(message.chat.id, "没有该网页路径")

    def __url_html_in(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.meat = message.text
        # 初始化pixelsList类
        pixels_new = pixelsList()
        # 调用json_Judge_mate方法
        pixels_new.json_Judge_mate(self.id, self.meat, self.url_in)
        self.urladd()
        self.bot.send_message(message.chat.id, "添加成功")
        print(f"{self.id}添加像素成功     {time.ctime()}")

    def urladd(self):
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.file_html = f'{File_HTEML}/{self.val}/{self.url_in}.html'
        self.openhtml()
        self.bs4()
        self.__server_html()

    def openhtml(self):
        with open(self.file_html, mode='r', encoding="utf-8") as f:
            self.html_content = f.read()
    # 替换落地页的  --改跳转
    def bs4(self):
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(self.html_content, 'html.parser')
        # 创建一个新的script标签并设置内容
        script_tag = soup.new_tag('script')
        script_tag.string = f'fbq(\'init\', \'{self.meat}\');'
        # 创建<noscript>标签
        noscript_tag = soup.new_tag('noscript')
        # 创建<img>标签并设置属性和src
        img_tag = soup.new_tag('img', height="1", width="1", style="display:none",
                               src=f"https://www.facebook.com/tr?id={self.meat}&ev=PageView&noscript=1")
        # 将<img>标签添加到<noscript>标签中
        noscript_tag.append(img_tag)
        # 在<head>标签中添加<script>和<noscript>标签
        head = soup.find('head')
        if head:
            head.append(script_tag)
            head.append(noscript_tag)

        # 将修改后的HTML转换回字符串
        modified_html_content = str(soup)
        modified_html_content = soup.encode('utf-8')
        self.html_txt = modified_html_content

    def json_open(self):
        self.DateFile = DateFile
        with open(self.DateFile, mode='r', encoding='utf-8') as f:
            self.intjson = json.load(f)

    def json_save(self):
        self.json_open()
        self.intjson["mate"].append(self.meat)
        with open(self.DateFile, mode='w', encoding='utf-8') as f:
            json.dump(self.intjson, f, ensure_ascii=False)

    def __server_html(self):
        html = self.html_txt
        with open(self.file_html, 'wb') as file:
            file.write(html)


class file_html:
    """
    用于获取网页路径
    """

    def __init__(self, message):
        self.id = message.chat.id
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.path = f"{File_HTEML}/{self.val}"
        self.list_immediate_subdirectories()

    def list_immediate_subdirectories(sefl):
        immediate_subdirectories = []
        entries = os.listdir(sefl.path)  # 列出这个文件夹下的所有文件和文件夹
        for entry in entries:
            path = os.path.join(sefl.path, entry)
            if os.path.isdir(path):
                immediate_subdirectories.append(entry)
        sefl.file_lists = immediate_subdirectories

    def file_splicing(self, file_list):
        html_files = []
        file = f"{self.path}/{file_list}"
        entries = os.listdir(file)
        for entry in entries:
            full_path = os.path.join(file, entry)
            # 检查这个路径是否是一个文件
            if os.path.isfile(full_path) and full_path.endswith('.html'):
                html_files.append(full_path)
        self.html_file_names = [os.path.basename(path) for path in html_files]

    def splicing(self):
        i = 0
        file_list = []
        # 循环遍历家目录获取其中所有.html文件
        for list in self.file_lists:
            self.file_splicing(list)
            i = 0
            while i < len(self.html_file_names):
                html_name = str(self.html_file_names[i])[:-5]
                file_list.append(f"{list}/{html_name}")
                i += 1
        return file_list


class template_html:
    """
    用于获取网页模板路径
    """

    def __init__(self, message):
        self.id = message.chat.id
        self.path = f"{Template_HTML}"
        self.list_immediate_subdirectories()
        self.file_splicing()

    def list_immediate_subdirectories(sefl):
        immediate_subdirectories = []
        entries = os.listdir(sefl.path)
        for entry in entries:
            path = os.path.join(sefl.path, entry)
            if os.path.isdir(path):
                immediate_subdirectories.append(entry)
        sefl.file_lists = immediate_subdirectories

# 看你是否是一个html，是的话就返回
    def file_splicing(self):
        html_files = []
        for file_list in self.file_lists:
            file = f"{self.path}/{file_list}"
            entries = os.listdir(file)
            for entry in entries:
                full_path = os.path.join(file, entry)
                # 检查这个路径是否是一个文件
                if os.path.isfile(full_path) and full_path.endswith('.html'):
                    html_files.append(full_path)
        self.html_file_names = [os.path.basename(path) for path in html_files] #从html_files列表中的每个路径提取文件名，并将这些文件名存储在self.html_file_names属性中

    def splicing(self):
        i = 0
        file_list = []
        for list in self.file_lists:
            html_name = str(self.html_file_names[i])[:-5]
            file_list.append(f"{list}/{html_name}")
            i += 1
        return file_list


class userpage:
    """
    作者:yyl
    rq:2024.4.8
    功能描述：生产对应的userid文件夹
    """

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.id_file = IDFile
        self.file_list = File_HTEML
        self.DateFile = DateFile
        self.__read_admin()

    def __read_admin(self):
        with open(file=self.DateFile, mode='r', encoding='utf-8') as date:
            self.admin_date = json.load(date)
        self.admin_date

    # 生成以用户id命名的文件夹
    def create_dir(self):
        userid = str(self.message.chat.id)
        idn = userNumber_id(userid)
        dictionary = idn.id_date
        val = chr(dictionary[f'{userid}'])
        # 指定生成文件夹路径
        userdir = os.path.join(self.file_list, val)
        # 获取当前用户id并转为int
        id = int(userid)
        # 判断该id是否在user列表里
        if id in self.admin_date['user']:
            # 判断该文件夹是否存在
            if os.path.isdir(userdir):
                print(f'该目录已存在      {time.ctime()}')
            else:
                os.makedirs(userdir)
                print(f'已创建用户文件夹      {time.ctime()}')
        elif id in self.admin_date['Admin']:
            if os.path.isdir(userdir):
                print(f'该目录已存在      {time.ctime()}')
            else:
                os.makedirs(userdir)
                print(f"已创建管理员文件夹      {time.ctime()}")


class webModules:
    '''
    zds
    2024/4/8
    fun：
    # 网页模板：
    # 每一个普通用户都可以复制一个落地页模板到自己的路径下进行操作（用于保证落地页内容相同但其中的跳转和像素不同）
    '''

    def __init__(self, bot, message):
        self.bot = bot
        self.id = message.chat.id
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.path = Template_HTML
        self.File_HTEML = File_HTEML
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.command_user()
        self.command_del()

    def command_del(self):
        if self.command == '删除网页':
            destPath = self.File_HTEML
            destDirList = os.listdir(f'{File_HTEML}/{self.val}')  # 要复制路径的 文件夹·文件
            list = str(destDirList).strip('[]').replace("'", "").replace(",", "\n")
            self.bot.send_message(self.message.chat.id, f"已有模板名称:\n {list}")
            self.bot.send_message(self.message.chat.id, "请输入要删除的模板名称: ")
            self.bot.register_next_step_handler(self.message, self.del_template)

    def command_user(self):
        if self.command == '复制网页模板':
            destPath = self.File_HTEML
            destDirList = os.listdir(self.path)  # 要复制路径的 文件夹·文件
            list = str(destDirList).strip('[]').replace("'", "").replace(",", "\n")
            self.bot.send_message(self.message.chat.id, f"已有模板名称:\n {list}")
            self.bot.send_message(self.message.chat.id, "请输入要复制的模板名称: ")
            self.bot.register_next_step_handler(self.message, self.copy_template)

    def del_template(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.cmd = message.text
        self.deleteWebTemplate()

    def copy_template(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.cmd = message.text
        self.copyFiles()

    def copyFiles(self):
        try:
            destPath = self.File_HTEML
            destDirList = os.listdir(self.path)  # 要复制路径的 文件夹·文件
            if self.cmd in destDirList:
                copyResult = shutil.copytree(self.path, f"{destPath}/{self.val}/{self.cmd}")
                print(f'{copyResult}，文件已成功创建    {time.ctime()}')
                shutil.move(f"{destPath}/{self.val}/{self.cmd}/{self.cmd}", f"{destPath}/")
                shutil.rmtree(f"{destPath}/{self.val}/{self.cmd}")
                shutil.move(f"{destPath}/{self.cmd}", f"{destPath}/{self.val}")
                self.bot.send_message(self.message.chat.id, "模板创建成功")
            else:
                self.bot.send_message(self.message.chat.id, "没有该模板文件")
                print(f'没有该模板文件    {time.ctime()}')
        except Exception as e:
            print(f'创建文件夹 失败 ，{e} {time.ctime()}')
            self.bot.send_message(self.message.chat.id,
                                  "模板创建失败，请检查路径是否正确(当前版本下：若网页路径已存在，也会创建失败可以使用“*查看网页路径”查看)")

    def deleteWebTemplate(self):  # 删除网页模板
        try:
            destPath = f'{self.File_HTEML}/{self.val}'  # 工作目录
            webTamplate_list = os.listdir(f'{destPath}')  # 找到用户所有的模板 导出为列表
            if f'{self.cmd}' in webTamplate_list:  # 判断删除的目标是否在工作列表中
                shutil.rmtree(f'{destPath}/{self.cmd}')
                self.meat_del(self.id)
                self.bot.send_message(self.message.chat.id, "模板以及所带像素删除成功")
                print(f'删除网页和所属像素成功   {time.ctime()}')
            else:
                print(f'未找到相关模板目录，请确认删除command指令')
                self.bot.send_message(self.message.chat.id, "未找到相关模板，请确认删除command指令")
        except Exception as e:
            print(f'模板文件夹删除失败 ，{e} {time.ctime()}')

    def meat_del(self, id):
        self.json_open()
        id = str(self.id)
        if id in self.intjson['mate']:
            del self.intjson['mate'][f'{id}'][f'{self.cmd}/eng']
            self.server_id(self.intjson)
            print(f'用户已删除 {self.cmd}中的像素   {time.ctime()}')

    def json_open(self):  # 读取user中的id字典
        self.DateFile = DateFile
        with open(self.DateFile, mode='r', encoding='utf-8') as f:
            self.intjson = json.load(f)

    def server_id(self, writed_Data):  # 将内存数据写入json
        with open(file=self.DateFile, mode='w', encoding='utf-8') as date:
            date.write(json.dumps(writed_Data, ensure_ascii=False))

class userNumber_id:
    """
    用户id对应的字符
    """

    def __init__(self, userid):
        self.id_file = IDFile
        self.DateFile = DateFile
        self.userid = userid
        self.open_id()
        self.read_admin()
        self.index = list(self.id_date.values())
        self.id_max = max(self.index)
        self.is_ena_in_id()
        self.server_id()

    def read_admin(self):
        with open(file=self.DateFile, mode='r', encoding='utf-8') as date:
            self.admin_date = json.load(date)
        self.admin_date

    def open_id(self):
        with open(file=self.id_file, mode='r', encoding='utf-8') as date:
            self.id_date = json.load(date)

    def is_ena_in_id(self):
        if self.userid in str(self.admin_date['user']):
            self.update_id()
        elif self.userid in str(self.admin_date['Admin']):
            self.update_id()
        else:
            print(f"用户id:{self.userid}未添加 {time.ctime()}")

    def update_id(self):
        if self.userid in self.id_date.keys():
            print(f"用户id:{self.userid}存在     {time.ctime()}")
        else:
            self.id_date.update({self.userid: self.id_max + 1})
            print(f"用户对应id已更新    {time.ctime()}")

    def server_id(self):
        with open(file=self.id_file, mode='w', encoding='utf-8') as date:
            date.write(json.dumps(self.id_date, ensure_ascii=False))


class pixelsList:
    '''
    创建像素列表，每个用户只能输出自己的像素
    '''

    def __init__(self):
        self.id_file = IDFile
        self.DateFile = DateFile
        self.intjson = {}
        self.pixelID = '0'
        self.pixelContent = '0'

    def json_open(self):  # 读取user中的id字典
        self.DateFile = DateFile
        with open(self.DateFile, mode='r', encoding='utf-8') as f:
            self.intjson = json.load(f)
            # print(f'json打印：{self.intjson} \n    {time.ctime()}')

    def server_id(self, writed_Data):  # 将内存数据写入json
        with open(file=self.DateFile, mode='w', encoding='utf-8') as date:
            date.write(json.dumps(writed_Data, ensure_ascii=False))

    def json_Judge_mate(self, userId, pixelContent, page_url):
        # 判断是否在mate里，在就执行加载像素
        # userId在，就更新 该userId的值，否则建立新的userid字典
        self.json_open()
        user_id = str(userId)
        if user_id not in self.intjson['mate']:
            self.intjson['mate'][user_id] = {}
        page_urls = self.intjson['mate'][user_id].keys()
        user_ids = self.intjson['mate'].keys()
        if user_id in user_ids and page_url in page_urls:
            # 获取userid里的pixelid的最大值，然后+1
            self.pixelID = str(int(max(self.intjson['mate'][user_id][page_url].keys())) + 1)
            # 获取用户输入的像素id
            self.intjson['mate'][user_id][page_url].update({self.pixelID: pixelContent})
            # 写入数据
            self.server_id(self.intjson)
        # 如果判断username没在mate里，就建立新的“userid”字典，并添加当前所要添加的像素id
        else:
            print(f'用户id不存在，创建id表   {time.ctime()}')
            self.intjson['mate'][user_id].update({f"{page_url}": {}})
            self.intjson['mate'][user_id][page_url] = {"0": ""}
            self.pixelID = str(int(max(self.intjson['mate'][user_id][page_url].keys())) + 1)
            self.intjson['mate'][user_id][page_url].update({self.pixelID: pixelContent})
            self.server_id(self.intjson)
            # print(self.intjson)
            self.server_id(self.intjson)
            # print(self.intjson)

    # 用于删除用户指定网页中的像素
    def del_pix(self, userId, pixelID):
        self.json_open()
        if userId in self.intjson['mate']:
            del self.intjson['mate'][userId][pixelID]
            print(f'用户已删除 {pixelID}像素   {time.ctime()}')


class html_copy:
    '''
    复制同一个家目录下的网页文件
    '''

    def __init__(self, bot, message):
        self.File_HTEML = File_HTEML
        self.bot = bot
        self.id = message.chat.id
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.command_user()

    # 复制用户目录下的网址
    def command_user(self):
        if self.command == '复制用户网页':
            destPath = self.File_HTEML
            destDirList = os.listdir(f'{destPath}/{self.val}')  # 要复制路径的 文件夹·文件
            print("destDirList:", len(destDirList))
            if len(destDirList) == 0:
                self.bot.send_message(self.message.chat.id, "用户家目录不存在")
            else:
                list = str(destDirList).strip('[]').replace("'", "").replace(",", "\n")
                self.bot.send_message(self.message.chat.id, f"已有落地页路径名称 :\n {list}")
                self.bot.send_message(self.message.chat.id, "请输入要复制的落地页路径 :如us ")
                self.bot.register_next_step_handler(self.message, self.copy_template)

    def del_template(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.cmd = message.text
        self.deleteWebTemplate()

    def copy_template(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.cmd = message.text
        self.copyFiles()

    def copyFiles(self):
        destPath = self.File_HTEML
        # 将目标路径指定到当前用户文件夹内
        destDirList = os.listdir(f'{destPath}/{self.val}')
        if self.cmd in destDirList:
            # 拼接用户输入的路径，该路径指定的是需要被复制的文件本身
            source_file = f"{destPath}/{self.val}/{self.cmd}/eng.html"
            # 拼接用户输入的路径，该路径指定的是需要被复制的文件的文件夹
            source_filepath = f"{destPath}/{self.val}/{self.cmd}"
            # 终端输出目标文件夹，验证是否获取到用户指定路径
            print(f'source_filepath {source_filepath}')

            # 让用户输入新文件名称
            self.bot.send_message(self.message.chat.id, "请输入新的落地页名称 :如eng1 ")
            # 将target_directory目标文件路径与source_filepath传入新参数以便do——copy使用
            self.source_filepath1 = source_filepath
            self.source_file1 = source_file
            # 获取用户新输入的值，也就是获取新落地页的名称，然后执行do_copy
            self.bot.register_next_step_handler(self.message, self.do_copy)
        else:
            self.bot.send_message(self.message.chat.id, "没有该路径")
            print(f'没有该路径    {time.ctime()}')

    def do_copy(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        # 获取用户输入的新落地页名称
        self.cmd = message.text
        # 将用户输入的新名称指定到新文件
        target_file_name = f'{self.cmd}.html'
        # 拼接目标文件完整路径，即目标位置，以及文件名称
        target_file_path = os.path.join(self.source_filepath1, target_file_name)
        try:
            # 执行复制功能
            shutil.copy(self.source_file1, target_file_path)
            print(f"文件成功复制至{target_file_path}")
            self.bot.send_message(self.message.chat.id, "成功复制 ")
        except FileNotFoundError:
            print(f"目标路径{self.source_filepath1}不存在.")
            self.bot.send_message(self.message.chat.id, "文件创建失败，目标路径{self.source_filepath1}不存在.")
        except PermissionError:
            print(f"Error: 权限无法访问{target_file_path}.")
            self.bot.send_message(self.message.chat.id, "权限无法访问，请确认路径是否正确")
        except Exception as e:
            print(f"未知错误: {e}")
            self.bot.send_message(self.message.chat.id, "未知错误，请检查指令是否正确")
        except Exception as e:
            print(f'创建文件夹 失败 ，{e} {time.ctime()}')
            self.bot.send_message(self.message.chat.id,
                                  "文件创建失败，请检查路径是否正确(当前版本下：若网页路径已存在，也会创建失败可以使用“*查看网页路径”查看)")


#  域名/us/eng固定(在使用情况下落地页域名不变内容可切换)可随时将落地页内容切换成us2,us3
class changeWeb:
    def __init__(self,bot,message):
        self.bot = bot
        self.id = message.chat.id
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.path = Template_HTML
        self.file_html = File_HTEML
        self.userCommand()      #入口


    def userCommand(self):
        if self.command == '模板切换':
            self.area_list=self.list_user_html()
            output = str(self.area_list).strip('[]').replace("'",'').replace(',','\n')
            if output != "":
                self.bot.send_message(self.id, f'您现有域名:\n{output}')
                self.bot.send_message(self.id,'您要固定的域名:')
                self.bot.register_next_step_handler(self.message,self.next_step_clear)
            else:
                self.bot.send_message(self.id,f'您当前域名为空，请复制模板')

    def next_step_clear(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        command=message.text
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        self.userfile = f'{File_HTEML}/{self.val}/{command}'
        destDirList = os.listdir(Template_HTML)  # 要复制路径的 文件夹·文件
        self.list = str(destDirList).strip('[]').replace("'", "").replace(",", "\n")
        if command in self.area_list:
            self.clear_DirContent(self.userfile)
            self.bot.send_message(self.message.chat.id, f"已有模板名称:\n {self.list}")
            self.bot.send_message(self.id, '你想切换的网页模板:')
            self.bot.register_next_step_handler(message,self.next_copy_web)
        else:
            self.bot.send_message(self.id,'您要固定的域名不存在')


    def next_copy_web(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        command = message.text
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])       # 拿到userId对应的像素字母
        if  command in self.list:
            self.htmlFile=f'{Template_HTML}/{command}'
            self.copy_Module(self.htmlFile,self.userfile)
            self.bot.send_message(self.id,'切换成功')
        else:
            self.bot.send_message(self.id,'无您所需要的模板')


    def list_user_html(self):   # 列出当前用户模板的文件夹
        idn = userNumber_id(str(self.id))
        dictionary = idn.id_date
        self.val = chr(dictionary[f'{str(self.id)}'])
        basket=os.listdir(f'{File_HTEML}/{self.val}')
        return basket




    def clear_DirContent(self,destPath):    #清空目录中的内容
        shutil.rmtree(destPath)        #要删除的目标文件集

    def copy_Module(self,WebModule_in,WebModule_out):   #复制的网页模板
        try:
            # 复制模板
            shutil.copytree(WebModule_in, WebModule_out)
        except Exception as e:
            print(f'复制模板失败{e}      {os.times()}')


class systeam:
    def __init__(self, bot, message):
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

# 这个没啥用
class bt_api:
    def __init__(self):
        self.Url = URL
        self.Key = KEY

    def bt_systeam(self):
        systeam_api = System(self.Url, self.Key)
        sys = systeam_api.get_system_total()
        return sys

    def bt_web(self):
        websites = Sites(self.Url, self.Key)
        webname = websites.websites()
        print(webname)
        web_index = websites.web_get_index(webname['data'][0]['name'])
        print(web_index)


if __name__ == '__main__':
    pass
