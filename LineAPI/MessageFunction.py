from linebot.models import (FlexSendMessage, TextSendMessage, ImageSendMessage)
from linebot import LineBotApi
import LineAPI.Bot as CPS_MessageAPI
import re , json
import requests

def MessageFunctionDetaction(message):
    try:
        text = message.message.text
        message_type = message.message.type

        source_type = message.source.type
        replytoken = message.reply_token
    except KeyError:
        return ""

    # メッセージ発信がグループからだった場合
    if(source_type == "group" and message_type == "text"):

        if("Slack チャネル 連携" in text):
            groupId = message.source.group_id
            text = text.replace("Slack チャネル 連携", "")
            secrete = re.findall('-S (.*)', text)
            try:
                secrete[0]
            except IndexError:
                return ""
            requests.post(CPS_MessageAPI.SlackOutCommingURL, data=json.dumps({
                'text': u'LINE GROUP REGIST:{0}:{1}'.format(groupId, secrete[0]),  # 通知内容
                'username': u'Line登録の情報通知(グループ)',  # ユーザー名
                'icon_emoji': u':line:',  # アイコン
                'link_names': 1,  # 名前をリンク化
            }))

    # メッセージ送信がユーザからであり、メッセージタイプがテキストだった場合
    if (source_type == "user" and message_type == "text"):
        if (text == "Line連携"):
            LineLogin(replytoken)
        else:
            ReplyMessage(replytoken)

def LineLogin(replytoken,state="Line11107b"):
    url = 'https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={1}&redirect_uri={2}/LineBot-API/callbackLogin&state={0}&scope=profile'.format(state,CPS_MessageAPI.cilent_id,CPS_MessageAPI.myselfURL)
    print(url)
    payload = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Login認証リンク",
                        "margin": "none",
                        "size": "xxl",
                        "align": "center",
                        "weight": "bold",
                        "color": "#000000"
                    },
                    {
                        "type": "separator"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "action": {
                    "type": "uri",
                    "label": "test",
                    "uri": url
                },
                "contents": [
                    {
                        "type": "image",
                        "url": "https://raw.githubusercontent.com/NOGU626/OriginalBots/master/btn_login_base.png",
                        "margin": "none",
                        "align": "center",
                        "gravity": "top",
                        "size": "3xl",
                        "aspectRatio": "3:1"
                    }
                ]
            }
        }
    }
    line_bot_api = CPS_MessageAPI.line_bot_api
    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.reply_message(replytoken,messages=container_obj)

# デフォルトの送信メッセージ
def ReplyMessage(replytoken):
    message = "メッセージありがとうございます。\n" + "申し訳ありませんが個別のご返信をすることができません。"
    line_bot_api = CPS_MessageAPI.line_bot_api
    line_bot_api.reply_message(replytoken,TextSendMessage(text=message))
