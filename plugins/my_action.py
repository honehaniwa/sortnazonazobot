from slackbot.bot import respond_to
import slackbot_settings
import random
import csv

answer = ""
flag = True
M_flag = True

def readData():
    with open('./plugins/data.csv', 'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        str = []
        for row in reader:
            str.append(row)
        str = [flatten for inner in str for flatten in inner]
    return str

def writeData(str):
    with open('./plugins/data.csv', 'a',encoding="utf-8") as f:
        print(','+str+'\n',file=f)

@respond_to('hello')
def reply_hello(message):
    message.reply('hello')

@respond_to('add\s(.*)')
def add_str(message, words):
    writeData(words)
    message.reply('added "' + words + '" !!!!!')

@respond_to('sort')
def reply(message):
    global answer,flag,M_flag
    if flag and M_flag:
        str = readData()
        answer = random.choice(str)
        message.reply(''.join(sorted(answer)) + 'ってな～んだ')
        flag = False 
    else:
        message.reply('まだ答えが出てないよ!!!\n答えが知りたかったら `@sortnazonazobot reply (ans 又は merge)` って言ってね!')

@respond_to('ans\s(.*)')
def reply_ans(message,words):
    global answer,flag,M_flag
    if flag and M_flag:
        message.reply('この問題はすでに正解されてるよ!\n新しく問題を出してほしいなら `@sortnazonazobot sort` って言ってね!')
    else:
        if not M_flag:
            str = words.split(' ')
            ans = max(str) + ' ' + min(str)
            if ans == answer:
                message.reply('正解!!!!! すごい!!!!!')
                answer = ''
                M_flag = True
            else:
                message.reply(ans + ' じゃないなぁ～')
        else:
            if words == answer:
                message.reply('正解!!!!! すごい!!!!!')
                answer = ''
                flag = True
            else:
                message.reply(words + ': じゃないなぁ～')

@respond_to('reply\s(.*)')
def reply_word(message, word):
    global answer,flag,M_flag
    if word == 'ans':
        if answer == '':
            message.reply('新しく問題を出してほしいなら `@sortnazonazobot [sort or merge]` って言ってね!')
        else:
            message.reply('正解は->'+answer+' でした～')
            answer = ''
            flag = True
            M_flag = True
    else:
        message.reply(word)

@respond_to('merge')
def mergesort(message):
    global M_flag,answer,flag
    if M_flag and flag:
        str = readData()
        s1 = random.choice(str)
        s2 = random.choice(str)
        answer = max(s1,s2) + ' ' + min(s1,s2)
        message.reply(''.join(sorted(answer)) + 'ってな～んだ')
        M_flag = False 
    else:
        message.reply('まだ答えが出てないよ!!!\n答えが知りたかったら `@sortnazonazobot reply ans` って言ってね!')

@respond_to('debug')
def debug(message):
    global answer
    if message.body['user'] == 'UFY47JBFV':
        message.send('flag is '+str(flag)+'\nM_flag is '+str(M_flag)+'\nans is '+answer)
    else:
        print(message.body['user'])
        message.send('Only developer can use this command...')

@respond_to('usage')
def message_to(message):
    message.reply('\n・1単語ソートなぞなぞは `@sortnazonazobot sort` \n・2単語ソートなぞなぞは `@sortnazonazobot merge` \n・単語の追加は `@sortnazonazobot add hogehoge` \n・解答をする場合は `@sortnazonazobot ans hogehoge` (1単語), `@sortnazonazobot ans hoge fuga` (2単語) \n・答えを知る `@sortnazonazobot reply ans` ')
    message.reply('新機能として天気予報、雨雲レーダーを追加しました!:sunny: `@sortnazonazobot weather` , `@sortnazonazobot 雨雲レーダー`')


@respond_to('weather')
def weather(message):
    import urllib
    import json

    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='
    # '130010'とすると東京の情報を取得してくれる
    # ここを変えれば任意の地域の天気情報を取得できる
    city_id = '230010'
    html = urllib.request.urlopen(url + city_id)
    jsonfile = json.loads(html.read().decode('utf-8'))
    title = jsonfile['title'] 
    telop = jsonfile['forecasts'][0]['telop']
    #telopが晴れだったら晴れのスラックのアイコンとか場合分け
    telop_icon = ''
    if telop.find('雪') > -1:    
        telop_icon = ':showman:'
    elif telop.find('雷') > -1:
        telop_icon = ':thinder_cloud_and_rain:'
    elif telop.find('晴') > -1:
        if telop.find('曇') > -1:
            telop_icon = ':partly_sunny:'
        elif telop.find('雨') > -1:
            telop_icon = ':partly_sunny_rain:'
        else:
            telop_icon = ':sunny:'
    elif telop.find('雨') > -1:
        telop_icon = ':umbrella:'
    elif telop.find('曇') > -1:
        telop_icon = ':cloud:'
    else:
        telop_icon = ':fire:'
    text = title + '\n' + '今日の天気　' + telop + telop_icon
    message.send(text) 


@respond_to('雨雲レーダー')
def sendURL(message):
    message.send('https://tenki.jp/radar/5/26/rainmesh.html')