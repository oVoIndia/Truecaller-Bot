import json
from pyrogram import Client, filters
from firebase import firebase
from process import check, searches, truecaller_search, fb_search, logreturn, log, eyecon_search
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from creds import cred

firebase = firebase.FirebaseApplication(cred.DB_URL)
app = Client(
    "Truecaller-Bot",
    api_id=cred.API_ID,
    api_hash=cred.API_HASH,
    bot_token=cred.BOT_TOKEN
)


@app.on_message(filters.command(["start"]))
def start(client, message):
    client.send_message(chat_id=message.chat.id,
                        text=f"`Hi` **{message.from_user.first_name}**\n Enter the number to search...\n**  __Join My Channel For Updates @HxBots__**",reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("About", callback_data="about"),
             InlineKeyboardButton("Buy Me A Coffee ☕", url="https://upayme.vercel.app/kkirodewal@ybl")]]))
    check_status = check(message.chat.id)

@app.on_callback_query()
def newbt(client,callback_query):
    txt=callback_query.data
    if txt=="about":
        callback_query.message.edit(text=f"**🔹 Bot Name 🔹      :**  __[Truecaller-Bot](t.me/truecalerbot)__\n\n**🔹 Channel 🔹         :**  __[HxBots](t.me/hxbots)__\n\n**🔹 Creator 🔹          :**  __[oVoIndia](https://github.com/oVoIndia)__\n\n**🔹 Owner 🔹            :**  __[Kirodewal](t.me/Kirodewal)__\n\n**🔹 Server 🔹            :**  __[Heroku](https://herokuapp.com/)__",
                        disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Any Feedback 🙋‍♂️", url="t.me/hxsupport")]]))
    elif txt=="src":
        callback_query.message.edit(text="Enjoy...😁:-D\nhttps://github.com/oVoIndia/Truecaller-Bot", disable_web_page_preview=True)



@app.on_message(filters.command(["about"]))
def about(client, message):
    client.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                        text=f"**🔸 Bot Name 🔸      :**  __[Truecaller-Bot](t.me/truecalerbot)__\n\n**🔸 Channel 🔸         :**  __[HxBots](t.me/hxbots)__\n\n**🔸 Creator 🔸          :**  __[oVoIndia](https://github.com/oVoIndia)__\n\n**🔸 Owner 🔸            :**  __[Kirodewal](t.me/Kirodewal)__\n\n**🔸 Server 🔸            :**  __[Heroku](https://herokuapp.com/)__",
                        disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Any Feedback 🙋‍♀️", url="t.me/hxsupport")]]))


@app.on_message(filters.command(["log"]))
def stats(client, message):
    stat = client.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                               text="`Fetching details`")
    txt = logreturn()
    stat.edit(txt)


@app.on_message(filters.text)
def echo(client, message):
    actvt = ""
    actvt = firebase.get('/stats', 'total_searches')
    data = {"total_searches": 1}
    if not actvt:
        firebase.put('/stats', 'total_searches', data)
    global pq
    pq = ""
    pro = client.send_message(chat_id=message.chat.id, text="Searching...", reply_to_message_id=message.message_id)
    r_num = message.text
    num = r_num.replace("+91", "").replace(" ", "")
    frbseyename = ""
    frbsefb = ""
    frbsetrname = ""
    frbsetrmail = ""
    if num.isnumeric and len(num) == 10:
        pq = "\n\n**----••Truecaller says----**\n\nLimit exceeded ,try again tomorrow 🤦🏻‍♂️"
        tresponse = ""
        try:
            tresponse = truecaller_search(cred.T_AUTH, num)
            if tresponse:
                restj = tresponse.json()
                trslt = json.dumps(restj)
                tjsonload = json.loads(trslt)
                if "name" in tjsonload['data'][0]:
                    if tjsonload['data'][0]['internetAddresses']:
                        pq = f"\n\n**----••Truecaller says----**\n\nName : `{tjsonload['data'][0]['name']}`\nCarrier : `{tjsonload['data'][0]['phones'][0]['carrier']}` \nE-mail : {tjsonload['data'][0]['internetAddresses'][0]['id']}"
                        frbsetrname = tjsonload['data'][0]['name']
                        frbsetrmail = tjsonload['data'][0]['internetAddresses'][0]['id']
                    elif not tjsonload['data'][0]['internetAddresses']:
                        pq = f"\n\n**----••Truecaller says----**\n\nName : `{tjsonload['data'][0]['name']}`\nCarrier : `{tjsonload['data'][0]['phones'][0]['carrier']}`"
                        frbsetrname = tjsonload['data'][0]['name']
                else:
                    pq = "\n\n**----••Truecaller says----**\n\nNo results found 🤦🏻‍♂️"
            if tresponse.status_code == 429:
                pq = "\n\n**----••Truecaller says----**\n\nLimit exceeded ,try again tomorrow 🤦🏻‍♂️"
        except:
            pass
        response = eyecon_search(num)
        fbres = fb_search(num)
        fbrslt = fbres.url.replace('https://graph.', '').replace('picture?width=600', '')
        if response:

            rslt = response.json()

            if rslt:
                temp = json.dumps(rslt).replace('[', '').replace(']', '')
                jsonload = json.loads(temp)

                yk = f"\n\n**----••Eyecon says----**\n\nName :`{jsonload['name']}`"
                frbseyename = jsonload["name"]
                if "facebook.com" in fbrslt:
                    yk = f"\n\n**----••Eyecon says----**\n\nName : `{jsonload['name']}`\nFacebook : {fbrslt}"
                    frbseyename = jsonload["name"]
                    frbsefb = fbrslt
            else:
                yk = "**----••Eyecon says----**\n\nNo results found 🤦🏻‍♂️"
        else:
            yk = "**----••Eyecon says----**\n\nNo results found 🤦🏻‍♂️"

        yk += pq
        pro.edit(text=yk, disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Source", callback_data="src")]]))
        searches()
        log()
        if frbseyename and frbsefb and frbsetrname and frbsetrmail:
            data = {
                "Eyecon Name": frbseyename,
                "Mob": num,
                "Truecaller name": frbsetrname,
                "Facebook": frbsefb,
                "Mail": frbsetrmail
            }
            firebase.put('/knowho-log', num, data)
        elif frbseyename and frbsefb and frbsetrname:
            data = {
                "Eyecon Name": frbseyename,
                "Mob": num,
                "Truecaller name": frbsetrname,
                "Facebook": frbsefb
            }
            firebase.put('/knowho-log', num, data)
        elif frbseyename and frbsefb:
            data = {
                "Eyecon Name": frbseyename,
                "Mob": num,
                "Facebook": frbsefb
            }
            firebase.put('/knowho-log', num, data)
        elif frbseyename and frbsetrname and frbsetrmail:
            data = {
                "Eyecon Name": frbseyename,
                "Mob": num,
                "Truecaller name": frbsetrname,
                "Mail": frbsetrmail
            }
            firebase.put('/knowho-log', num, data)
        elif frbseyename and frbsetrname:
            data = {
                "Eyecon Name": frbseyename,
                "Mob": num,
                "Truecaller name": frbsetrname
            }
            firebase.put('/knowho-log', num, data)
        elif frbsetrname and frbsetrmail:
            data = {
                "Truecaller name": frbsetrname,
                "Mob": num,
                "Mail": frbsetrmail
            }
            firebase.put('/knowho-log', num, data)
        elif frbsetrname:
            data = {
                "Truecaller name": frbsetrname
            }
            firebase.put('/knowho-log', num, data)

    else:
        pro.edit("`Only` **10** `digit numbers allowed` 🤦🏻‍♂️")


app.run()
