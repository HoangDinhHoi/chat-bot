import json
import aiohttp
from os import environ
from aiohttp import web

# fanpage token
PAGE_ACCESS_TOKEN = 'EAACtUPHBoJMBAC4XfAUl7VTN8hZAZAzh9W5O6VgqdQDEbkMDflUmxjQwSQOrX9ADfZBVv6jCVt2NGRwH4pmY57X6fPzqt6WrNSGmCIEPcUfxZCpfs4ZARdIZApBKjngWDsCOJbcaSnEAgrN1L81urkIvJCbuhUoZCfq8CwS3ZCvMKBQ7YWhrVvqe'
# verify token
VERIFY_TOKEN = 'Vm>@d(y26Ek/Q]G<'

class BotControl(web.View):

    async def get(self):
        query = self.request.rel_url.query
        if(query.get('hub.mode') == "subscribe" and query.get("hub.challenge")):
            if not query.get("hub.verify_token") == VERIFY_TOKEN:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(text=query.get("hub.challenge"))
        return web.Response(text='Forbidden', status=403)

    async def post(self):
        data = await self.request.json()
        if data.get("object") == "page":
            await self.send_greeting("Chào bạn. Mình là bot demo của học python.")

            for entry in data.get("entry"):
                for messaging_event in entry.get("messaging"):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]

                        if any(["chào" in message_text.lower(), "hi " in message_text.lower(),
                                "hello" in message_text.lower(), "có ai" in message_text.lower(),
                                "có ở đó" in message_text.lower(), "hi" == message_text.lower()]):
                            await self.send_message(sender_id, "Chào đằng ấy ^^")
                        elif any(["thông tin" in message_text.lower(), "người viết" in message_text.lower(),
                                  "ở đâu" in message_text.lower(), "tuổi" in message_text.lower()]):
                            await self.send_message(sender_id, "Mình tên là Hợi handsome/n năm nay mình 24 tuổi/n mình đang học Bách Khoa nha/n Cảm ơn đã like page của mình")
                        elif any(["bạn tên" in message_text.lower(), "mày tên" in message_text.lower(),
                                "your name" in message_text.lower(), "cậu tên" in message_text.lower()]):
                            await self.send_message(sender_id, "mình tên là bot demo aiohttp nha")
                        elif any(["thực đơn" in message_text.lower(), "menu" in message_text.lower(),
                                  "danh sách" in message_text.lower(), "cho mình hỏi" in message_text.lower(),]):
                            await self.send_message(sender_id,"Bạn vào đây để mua trà giải rượu, cặp chống gù lưng cửa Nhật nhé: https://www.facebook.com/japanshop28895/")

                        elif any(["tác giả" in message_text.lower(), "người viết" in message_text.lower(),
                                "ai viết" in message_text.lower(), "ba mày" in message_text.lower(), "cha mày" in message_text.lower()
                                     , "bố mày" in message_text.lower(), "tía mày" in message_text.lower()]):
                            await self.send_message(sender_id, "ahihi. Đừng chửi bậy như vậy chứ :)). mình tạo ra cái này cho vui ấy mà ^^")
                        elif any(["cứu giúp" in message_text.lower(), "help" in message_text.lower(), "trợ giúp" in message_text.lower(),
                                  "giúp mình" in message_text.lower(), "hài" in message_text.lower(), "tài thật" in message_text.lower()],
                                 "giúp" in message_text.lower(), "nhờ" in message_text.lower(), "nhờ chút" in message_text.lower()):
                            await self.send_message(sender_id, "Bạn dễ thương gì ấy ơi. Vào đây để kết bạn với mình nha: https://www.facebook.com/hoihandsome ")
                        elif any(["wtf" in message_text.lower(), "dmm" in message_text.lower(), "đm" in message_text.lower(),
                                  "đmm" in message_text.lower(), "định mệnh" in message_text.lower(), "mẹ mày" in message_text.lower(),
                                  "fuck you" in message_text.lower()]):
                            await self.send_message(sender_id, "Bạn mà chửi mình nữa là mình chửi lại đó ^^ không đùa đâu")
                        else:
                            await self.send_message(sender_id, "Mình nghe ba mình nói nếu bạn like page này của mình thì bạn sẽ trở nên đẹp nhất thế giới đó.")

        return web.Response(text='ok', status=200)

    async def send_greeting(self, message_text):
        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "setting_type": "greeting",
            "greeting": {
                "text": message_text
            }
        })
        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/thread_settings", params=params, headers=headers, data=data)

    async def send_message(self, sender_id, message_text):

        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": sender_id
            },
            "message": {
                "text": message_text
            }
        })

        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)



routes = [
    web.get('/', BotControl, name='verify'),
    web.post('/', BotControl, name='webhook'),
]

app = web.Application()
app.add_routes(routes)

# if __name__ == '__main__':
#     web.run_app(app, host='0.0.0.0', port=environ.get("PORT", 9090))
