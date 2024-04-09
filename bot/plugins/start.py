from telebot import types
import os
import shutil
from bot.handler_type import PluginInterface
from pybt.system import System
from pybt.sites import Sites
from bot.config import URL,KEY,HELP,File_HTEML,DateFile,Template_HTML
from bs4 import BeautifulSoup
import json
import re
import time
class StartPlugin(PluginInterface):
    command = 'start'
    def handler_command(self,bot,message):
        markup = types.InlineKeyboardMarkup()
        # itembtn1 = types.InlineKeyboardButton('tcmiku的档案库', url='https://tcmiku.github.io')
        # 返回callback_data一个 1-64字节的数据
        itembtn2 = types.InlineKeyboardButton('帮助信息', callback_data="help")
        markup.add(itembtn2)
        #根据当前用户id创建家目录
        page = userpage(bot,message)
        page.create_dir()
        #外置键盘设置
        show_button = button()
        show_button.open_admin(bot,message)
        bot.send_message(message.chat.id, f"启动成功欢迎用户: {message.chat.username}\n您的用户id为：{message.chat.id}", reply_markup=markup)

    def handler_back(self,bot,call):
        bot.send_message(call.message.chat.id, HELP)



    #权限判断机制
    def admin_start(self,bot,message):

        with open(file=DateFile,mode='r',encoding='utf-8') as date:
            admin_date = json.load(date)
        admin_date
        if message.from_user.id in admin_date["Admin"]:
            return "admin"
        elif message.from_user.id in admin_date['user']:
            return "user"
        else:
            return None

    def handle_message(self,bot,message):
        date = self.admin_start(bot,message)
        if date == 'admin':
            #管理员可使用命令
            #系统有关命令
            if message.text.startswith('!'):
                systeams = systeam(bot,message)
            elif message.text.startswith('#'):
                admin = authorityManagement(bot,message)
            elif message.text.startswith('*'):
                jumpurl = rehtml(bot,message)
                meatadd = meat(bot,message)
                copy_html = webModules(bot, message)
        elif date == 'user':
            #用户可使用命令
            if message.text.startswith('*'):
                jumpurl = rehtml(bot, message)
                meatadd = meat(bot, message)
                copy_html = webModules(bot,message)
        else:
            bot.send_message(message.chat.id, "您没有该权限")

#外置键盘控制
class button:
    def __read_date(self):
        self.DateFile = DateFile
        with open(file=self.DateFile,mode='r',encoding='utf-8') as date:
            self.admin_date = json.load(date)
        self.admin_date
    def open_admin(self,bot,message):
        self.__read_date()
        markup = types.ReplyKeyboardMarkup(row_width=2)  # row_width可以控制外置键盘一排放几个
        itembtn1 = types.KeyboardButton("#管理员列表")
        itembtn2 = types.KeyboardButton("#用户列表")
        itembtn3 = types.KeyboardButton("#添加管理员")
        itembtn4 = types.KeyboardButton("#添加用户")
        itembtn5 = types.KeyboardButton("#删除管理员")
        itembtn6 = types.KeyboardButton("#删除用户")
        itembtn7 = types.KeyboardButton("*查看网页路径")
        itembtn8 = types.KeyboardButton("*复制网页模板")
        itembtn9 = types.KeyboardButton("*改跳转")
        itembtn10 = types.KeyboardButton("*加像素")
        itembtn11 = types.KeyboardButton("*像素列表")
        if message.chat.id in self.admin_date["Admin"]:
            print(f"管理员{message.chat.username}启动外置键盘     {time.ctime()}")
            markup.add(itembtn1, itembtn2,itembtn3,itembtn4,itembtn5,itembtn6,itembtn7,itembtn8,itembtn9,itembtn10,itembtn11)
        elif message.chat.id in self.admin_date["user"]:
            print(f"用户{message.chat.username}启动外置键盘     {time.ctime()}")
            markup.add(itembtn7,itembtn8,itembtn9,itembtn10,itembtn11)
        bot.send_message(message.chat.id, "外置键盘启动", reply_markup=markup)

#权限管理机制
class authorityManagement:
    def __init__(self,bot,message):
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
        with open(file=self.DateFile,mode='r',encoding='utf-8') as date:
            self.admin_date = json.load(date)
        self.admin_date

    def __admin_show(self):
        if self.command == '管理员列表':
            date  = str(self.admin_date['Admin'])
            date = date.strip("[]").replace(",","\n")
            self.bot.send_message(self.message.chat.id,f"现有管理员id:\n{date}")

    def __user_show(self):
        if self.command == '用户列表':
            date  = str(self.admin_date['user'])
            date = date.strip("[]").replace(",","\n")
            self.bot.send_message(self.message.chat.id,f"现有用户id:\n{date}")

    def __user_del(self):
        if self.command == '删除用户':
            self.bot.send_message(self.message.chat.id,"请输入要删除的用户id")
            self.bot.register_next_step_handler(self.message,self.__user_del_nextstep)

    def __user_del_nextstep(self,message):
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
            self.bot.send_message(self.message.chat.id,"请输入要删除的管理员id")
            self.bot.register_next_step_handler(self.message,self.__admin_del_nextstep)

    def __admin_del_nextstep(self,message):
       self.bot.send_chat_action(message.chat.id, 'typing')
       if message.text.isdigit() and int(message.text) in self.admin_date['Admin']:
           self.admin_date['Admin'].remove(int(message.text))
           self.__server_date()
           self.bot.send_message(message.chat.id, "删除成功")
           print(f"删除管理员{message.text}成功     {time.ctime()}")
       else:
           self.bot.send_message(message.chat.id,"删除失败")
           print(f"删除管理员{message.text}失败     {time.ctime()}")

    def __admin_add(self):
        if self.command == '添加管理员':
            self.bot.send_message(self.message.chat.id,"请输入要加入的管理员id")
            self.bot.register_next_step_handler(self.message,self.__admin_add_nextstep)

    def __user_add(self):
        if self.command == '添加用户':
            self.bot.send_message(self.message.chat.id,"请输入要加入的用户id")
            self.bot.register_next_step_handler(self.message,self.__user_add_nextstep)

    def __user_add_nextstep(self,message):
        self.bot.send_chat_action(message.chat.id,'typing')
        if message.text.isdigit():
            self.admin_date['user'].append(int(message.text))
            self.__server_date()
            self.bot.send_message(message.chat.id,"添加成功")
            print(f'添加用户{message.text}      {time.ctime()}')
        else:
            self.bot.send_message(message.chat.id,"添加失败,您输入的id不是纯数字")
            print(f'用户{message.text}添加失败      {time.ctime()}')

    def __admin_add_nextstep(self,message):
       self.bot.send_chat_action(message.chat.id, 'typing')
       if message.text.isdigit():
           self.admin_date['Admin'].append(int(message.text))
           self.__server_date()
           self.bot.send_message(message.chat.id, "添加成功")
           print(f'添加管理员{message.text}     {time.ctime()}')
       else:
           self.bot.send_message(message.chat.id,"添加失败,您输入的id不是纯数字")
           print(f'管理员{message.text}添加失败     {time.ctime()}')

    def __server_date(self):
        with open(self.DateFile,mode='w',encoding='utf-8') as f:
            json.dump(self.admin_date,f,ensure_ascii=False)


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
        self.id = message.chat.id
        self.command = message.text.split(' ', 1)[0][1:]
        self.command_user()
        self.__file_html()

    def __file_html(self):
        if self.command == '查看网页路径':
            file = file_html(self.message)
            lists = file.splicing()
            lists = str(lists)
            cleaned_string = lists.strip("[]").replace(",", "\n")
            self.bot.send_message(self.message.chat.id,f"现有网页路径:\n{cleaned_string}")

    def command_user(self):
        if self.command == "改跳转":
            self.bot.send_message(self.message.chat.id,"请输入要修改的网页地址: ")
            self.bot.register_next_step_handler(self.message,self.__file_html_in)

    def __file_html_in(self,message):
        file = file_html(message)
        lists = file.splicing()
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url_in = message.text
        if self.url_in in lists:
            self.bot.send_message(message.chat.id, "请输入要跳转的网页: ")
            self.bot.register_next_step_handler(message, self.__url_html_in)
        else:
            self.bot.send_message(message.chat.id, "没有该网页路径")

    def __url_html_in(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url = message.text
        self.urladd()
        self.bot.send_message(message.chat.id,"修改成功")

    def urladd(self):
        self.file_html = f'{File_HTEML}/{self.id}/{self.url_in}.html'
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
        self.id = message.chat.id
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.command_user()
        self.mate_list()

    def command_user(self):
        if self.command == "加像素":
            self.bot.send_message(self.message.chat.id, "请输入要修改的网页地址: ")
            self.bot.register_next_step_handler(self.message, self.__file_html_in)

    def mate_list(self):
        if self.command == "像素列表":
            self.json_open()
            date = str(self.intjson['mate'])
            date = date.replace(",","\n")
            self.bot.send_message(self.message.chat.id,date)

    def __file_html_in(self,message):
        file = file_html(message)
        lists = file.splicing()
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.url_in = message.text
        if self.url_in in lists:
            self.bot.send_message(message.chat.id, "请输入要添加的像素id: ")
            self.bot.register_next_step_handler(message,self.__url_html_in)
        else:
            self.bot.send_message(message.chat.id, "没有该网页路径")

    def __url_html_in(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.meat = message.text
        self.urladd()
        self.bot.send_message(message.chat.id, "修改成功")

    def urladd(self):
        self.file_html = f'{File_HTEML}/{self.id}/{self.url_in}.html'
        self.openhtml()
        self.bs4()
        self.__server_html()

    def openhtml(self):
        with open(self.file_html,mode='r',encoding="utf-8") as f:
            self.html_content = f.read()

    def bs4(self):
        # # 使用BeautifulSoup解析HTML内容
        # soup = BeautifulSoup(self.html_content, 'html.parser')
        #
        # # 查找所有的<script>标签
        # script_tags = soup.find_all('script')
        #
        # # 遍历每个<script>标签并修改fbq('init', '原像素ID')
        # for script_tag in script_tags:
        #     # 获取<script>标签的文本内容
        #     script_content = script_tag.string
        #     if script_content:
        #         # 使用正则表达式替换fbq('init', '原像素ID')中的ID
        #         pattern = r"fbq\('init', '\d+'\);"
        #         new_content = re.sub(pattern, f"fbq('init', '{self.meat}');", script_content)
        #         # 将修改后的内容设置回<script>标签
        #         script_tag.string.replace_with(BeautifulSoup(new_content, 'html.parser').string)
        #
        #         # 查找<noscript>标签并修改其中的src属性
        # # 查找<noscript>标签内的<img>标签
        # noscript_tags = soup.find_all('noscript')
        # for noscript in noscript_tags:
        #     img_tags = noscript.find_all('img')
        #     for img in img_tags:
        #         # 提取src属性的值
        #         src_value = img['src']
        #         # 使用正则表达式找到id参数的值
        #         match = re.search(r'id=(\d+)', src_value)
        #         if match:
        #             # 提取id参数中的数字
        #             old_id = match.group(1)
        #             # 假设我们有一个新的id值
        #             new_id = self.meat  # 替换为你想要的新id值
        #             # 替换src中的旧id为新id，同时保持其他部分不变
        #             new_src_value = src_value.replace(f'id={old_id}', f'id={new_id}')
        #             # 更新<img>标签的src属性值
        #             img['src'] = new_src_value
        # # 将修改后的内容编码为字符串

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
        with open(self.DateFile,mode='r',encoding='utf-8') as f:
            self.intjson = json.load(f)

    def json_save(self):
        self.json_open()
        self.intjson["mate"].append(self.meat)
        with open(self.DateFile,mode='w',encoding='utf-8') as f:
            json.dump(self.intjson,f,ensure_ascii=False)

    def __server_html(self):
        html = self.html_txt
        with open(self.file_html,'wb') as file:
            file.write(html)

class file_html:
    def __init__(self,message):
        self.id = message.chat.id
        self.path = f"{File_HTEML}/{self.id}"
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
        self.html_file_names = [os.path.basename(path) for path in html_files]

    def splicing(self):
        i = 0
        file_list = []
        for list in self.file_lists:
            html_name = str(self.html_file_names[i])[:-5]
            file_list.append(f"{list}/{html_name}")
            i+=1
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
        # 指定生成文件夹路径
        userdir = os.path.join(self.file_list, userid)
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
    def __init__(self,bot,message):
        self.bot = bot
        self.id = message.chat.id
        self.message = message
        self.command = message.text.split(' ', 1)[0][1:]
        self.path = Template_HTML
        self.File_HTEML = File_HTEML
        self.command_user()

    def command_user(self):
        if self.command == '复制网页模板':
            self.bot.send_message(self.message.chat.id, "请输入要复制的模板名称: ")
            self.bot.register_next_step_handler(self.message,self.copy_template)

    def copy_template(self,message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.cmd = message.text
        self.copyFiles()
    def copyFiles(self):
        try:
            destPath = self.File_HTEML
            destDirList = os.listdir(self.path)  # 要复制路径的 文件夹·文件
            if self.cmd in destDirList:
                copyResult = shutil.copytree(self.path, f"{destPath}/{self.id}/{self.cmd}")
                print(f'{copyResult}，文件已成功创建    {time.ctime()}')
                shutil.move(f"{destPath}/{self.id}/{self.cmd}/{self.cmd}",f"{destPath}/")
                shutil.rmtree(f"{destPath}/{self.id}/{self.cmd}")
                shutil.move(f"{destPath}/{self.cmd}", f"{destPath}/{self.id}")
            else:
                self.bot.send_message(self.message.chat.id, "没有该模板文件")
                print(f'没有该模板文件    {time.ctime()}')
        except Exception as e:
            print(f'创建文件夹 失败 ，{e} {time.ctime()}')


if __name__ == '__main__':
    dome = file_html()
    print(dome.splicing())