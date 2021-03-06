"""
随机色图生成器（未完成）
"""
import asyncio
import requests
from typing import Any, Dict, Union

from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart


class RandomPic:
    def __init__(self,
                 glo_setting: Dict[str, Any],
                 scheduler: AsyncIOScheduler,
                 app: Quart,
                 bot_api: Api,
                 *args, **kwargs):
        '''
        初始化，只在启动时执行一次

        参数：
            glo_setting 包含所有设置项，具体见default_config.json
            bot_api 是调用机器人API的接口，具体见<https://python-aiocqhttp.cqp.moe/>
            scheduler 是与机器人一同启动的AsyncIOScheduler实例
            app 是机器人后台Quart服务器实例
        '''
        # 注意：这个类加载时，asyncio事件循环尚未启动，且bot_api没有连接
        # 此时不要调用bot_api
        # 此时没有running_loop，不要直接使用await，请使用asyncio.ensure_future并指定loop=asyncio.get_event_loop()

        # 如果需要启用，请注释掉下面一行
        # return

        # 这是来自yobot_config.json的设置，如果需要增加设置项，请修改default_config.json文件
        self.setting = glo_setting

        # 这是cqhttp的api，详见cqhttp文档
        self.api = bot_api

        # # 注册定时任务，详见apscheduler文档
        # @scheduler.scheduled_job('cron', hour=8)
        # async def good_morning():
        #     await self.api.send_group_msg(group_id=123456, message='早上好')

        # # 注册web路由，详见flask与quart文档
        # @app.route('/is-bot-running', methods=['GET'])
        # async def check_bot():
        #     return 'yes, bot is running'

    @staticmethod
    def generate_random_pic():
        """
        随机生成色图CQ地址
        
        :return str
        """

        # 使用随机图片API接口: https://api.lolicon.app/#/setu
        # 仅限PCR，无R18要素
        API_URL = 'https://api.lolicon.app/setu/'
        API_PARAMS = { 'keyword': 'Re:Dive', 'size1200': True}

        result = requests.get(url = API_URL, params = API_PARAMS) 
        data = result.json()

        # 返回值
        if data['code'] != 0:
            quota = data['quota']
            quota_ttl = data['quota_min_ttl']
            print("当前余额：{}， 下次回复时间：{}秒".format(quota, quota_ttl))
            return "lsp别冲了，休息休息\n[CQ:image,file=6FAE123008DF352FE0EA054A79725E1F,url=http://c2cpicdw.qpic.cn/offpic_new/1819669596//1819669596-3842825114-6FAE123008DF352FE0EA054A79725E1F/0?term=2]"
        
        pic = data['data'][0]['url']

        # 生成CQ格式的图片
        cq_url = "[CQ:image,file={}]".format(pic)

        return cq_url


    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        '''
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        '''
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        # return

        cmd = ctx['raw_message']
        if cmd == '色图' or cmd == '来张色图':

            # 调用api发送消息，详见cqhttp文档
            # Note: 单独给某人发消息 uncomment
            # await self.api.send_private_msg(
            #     user_id=1819669596, message='没有色图')

            # 返回字符串：发送消息并阻止后续插件
            # Note: 从哪发return到哪
            reply = self.generate_random_pic()
            return reply

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False
