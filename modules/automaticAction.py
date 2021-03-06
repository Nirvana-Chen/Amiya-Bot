import os
import time
import json
import threading

from database.baseController import BaseController
from library.imageCreator import clean_temp
from modules.commonMethods import restart, insert_zero
from modules.gameData import GameData
from modules.network.httpRequests import HttpRequests

from functions.vblog.vblog import VBlog

database = BaseController()
gameData = GameData()
blog = VBlog()

with open('config.json') as config:
    config = json.load(config)
    admin_id = config['admin_id']


def run_automatic_action():
    threading.Thread(target=AutomaticAction().run_loop).start()


class AutomaticAction(HttpRequests):
    def __init__(self):
        super().__init__()

    def run_loop(self):
        try:
            first_loop = True
            while True:
                if first_loop:
                    first_loop = False
                    self.send_admin('启动完毕')
                stop = self.events()
                if stop:
                    print('loop stop')
                    break
                time.sleep(60)
        except KeyboardInterrupt:
            pass

    def send_admin(self, text):
        self.send_private_message({'user_id': admin_id}, text)

    def events(self):
        now = time.localtime(time.time())
        hour = now.tm_hour
        mint = now.tm_min

        if (hour == 4 or hour == 16) and mint == 0:

            # 判断是否可以重启
            record = 0
            now_time = int('%s%s%s%s' % (now.tm_year,
                                         insert_zero(now.tm_mon),
                                         insert_zero(now.tm_mday),
                                         0 if hour == 4 else 1))

            if os.path.exists('restart.txt') is False:
                with open('restart.txt', mode='w+') as rs:
                    rs.write(str(now_time))
            else:
                with open('restart.txt', mode='r+') as rs:
                    record = int(rs.read())
                    rs.seek(0)
                    rs.write(str(now_time))

            if record < now_time:

                # 重置签到和心情值
                if hour == 4:
                    database.user.reset_state()

                # 清空消息及图片记录
                database.message.del_message()
                database.resource.del_image_id()

                # 清除图片缓存
                clean_temp()

                # 更新干员和材料数据
                res = gameData.update()
                if res:
                    self.send_admin(res)

                # 执行重启
                restart()
                return True

        threading.Timer(0, self.intellect_full_alarm).start()
        threading.Timer(0.5, self.send_new_blog).start()
        return False

    def intellect_full_alarm(self):
        now = int(time.time())
        results = database.remind.check_intellect_full_alarm(now)
        if results:
            for item in results:
                text = '博士！博士！您的理智已经满%d了，快点上线查看吧～' % item['full_num']
                data = {
                    'user_id': item['user_id'],
                    'group_id': item['group_id'],
                    'type': item['message_type']
                }
                self.send_message(data, text, at=True)

    def send_new_blog(self):
        blog_file = 'resource/blog.txt'
        record_id = []
        if os.path.exists(blog_file):
            with open(blog_file, mode='r') as file:
                record_id = file.read().split('\n')

        new_id = blog.get_new_blog(only_id=True)

        if new_id and isinstance(new_id, str) and new_id not in record_id:
            new_blog = blog.get_new_blog()

            if new_blog is False:
                return False

            with open(blog_file, mode='a+') as file:
                file.write(new_id + '\n')

            group_list = self.get_group_list()
            time_record = time.time()
            total = 0

            self.send_admin('开始推送微博:\n%s\n共有 %d 个群' % (new_id, len(group_list)))

            for group in group_list:
                data = {'group_id': group['id']}
                for index, item in enumerate(new_blog):
                    at_all = 'all' if group['permission'] == 'ADMINISTRATOR' and index == 0 else False
                    if item.content:
                        self.send_group_message(data, message_chain=item.content, at=False)
                total += 1
            complete = '微博推送完毕。成功 %d / %d，耗时：%ds' % (total, len(group_list), time.time() - time_record)
            self.send_admin(complete)
