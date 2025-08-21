import requests
import json
import os
import time
from datetime import datetime


def send_serverchan_message(title, desp=''):
    """
    通过 Server 酱发送消息
    参数：
    - send_key: 方糖服务的 SendKey（在官网获取）
    - title: 消息标题（必填）
    - desp: 消息内容（支持 Markdown，可选）
    返回：
    - 成功返回 Server 酱响应，失败返回错误信息
    """
    send_key = "SCT267560TNyjjRYal9CG8M6Pc1cmvhKos"
    url = f"https://sctapi.ftqq.com/{send_key}.send"

    try:
        response = requests.post(
            url,
            data={
                "title": title,
                "desp": desp
            },
            timeout=10
        )
        result = response.json()

        if result.get("code") == 0:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": result.get("message")}

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
def checkin():
    # glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("COOKIES", [
        "koa:sess=eyJ1c2VySWQiOjMyNDQ3NywiX2V4cGlyZSI6MTc4MDg4NzcwNTg5NywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=6urjvuyMBWg089ZenAKM6e9ZyFA; __stripe_mid=0d14b152-0810-4160-a956-2bce7d7d44218f58fc"])

    if cookies[0] != "":
        check_in_url = "https://glados.space/api/user/checkin"  # 签到地址
        status_url = "https://glados.space/api/user/status"  # 查看账户状态

        referer = 'https://glados.space/console/checkin'
        origin = "https://glados.space"
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        payload = {
            'token': 'glados.one'
        }

        for cookie in cookies:
            checkin = requests.post(check_in_url, headers={'cookie': cookie, 'referer': referer, 'origin': origin,
                                                           'user-agent': useragent,
                                                           'content-type': 'application/json;charset=UTF-8'},
                                    data=json.dumps(payload))
            state = requests.get(status_url, headers={
                'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})

            points = 0
            message_days = ""
            print("开始连接glados")
            if checkin.status_code == 200:
                print("连接成功")
                # 解析返回的json数据
                result = checkin.json()
                # 获取签到结果
                check_result = result.get('message')
                balance = int(float(result['list'][0]['balance']))
                # 获取账号当前状态
                result = state.json()
                # 获取剩余时间
                leftdays = int(float(result['data']['leftDays']))

                # print(leftdays)
                # 获取账号email
                email = result['data']['email']
                # print(email)
                # print(check_result)
                txt = "账号:{0} \n\n剩余天数:{1} \n\n 剩余积分:{2} \n\n签到内容:{3}".format(email, str(leftdays),
                                                                                            str(balance), check_result)
                send_serverchan_message("glados签到", txt)
                print(txt)
            else:
                print("连接失败")
                email = ""
                message_status = "签到请求URL失败, 请检查..."
                message_days = "error"


    else:
        # 推送内容
        title = f'# 未找到 cookies!'


if __name__ == '__main__':
    # 获取当前时间
    checkin()
