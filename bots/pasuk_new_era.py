
# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback

bot_id = 726564409
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
GLOBALADMINS = [512006137, 850666493]
phrases = {'permission_error':'Сука блять у тебя прав нет для этого ты кто такой блять', 
           'admin_error':'Сука я Дурова в ачько ебал дай админа'}
triggers = {'хс': 'Игра для пидоров'}
pasuki = ['Ебло', 'Кто ебло я ебло?', 'Сука', 'Никак', 'От какого Пасюка', 'От меня или от долбоеба цифрового?', 'Ебло', 'А, нет', 'Я ебло', 'bot.forward_message кажется', 'Чат оригинального сообщения, айди оригинального сообщения, чат, куда форвардить', 'Ты от моего лица форвард не сделаешь далбаеб', 'Ты можешь сделать форвард моего сообщения', 'message.forward_from_user.id', 'Я не пидарас', 'я пидарас', 'Здохнуть охота', 'Рассказывай', 'На самом деле я хотел бы сделать dragonwars типо копии чв с некоторыми изменениями и нововведениями, чтобы просто с вами и ещё некоторыми людьми почилить', 'То есть чтобы все выбрали себе сторону и касались', 'Но это я в соло сделаю если лень не будет', 'Ладна', 'Она похожа на рп игру какую то', 'А', 'Ну да', 'Мастер ведёт, ресурсы сохраняет тебе', 'События там', 'Короче да', 'Ебать сложно я их просто называю одноклассники', 'Да ясен писюн ты шо ебать', '@BastionSiegeBot', 'Зачекайте игру', '⚡️Пасюк Лошадкин\nОслиное логово\n\nСтатус       Деревня🏡\nТерритория      2659🗺\n\nСезон           Зима❄️\nПогода      Солнечно☀️\nВремя       10:44:34🕓\n\nЖители           260👥\nАрмия            440⚔️\nКристаллы          0💎\nЗолото         40552💰\nДерево          5420🌲\nКамень          4420⛏\nЕда            27488🍖', 'я сладенькая писечка', 'Далбаеб?', 'Сайт студии', 'Ебу дали?', 'А, ну ладно', 'Мне не сказали даже', 'Далбаебы', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'моя сиська больше, чем осла пиписька', 'Тут было что то интересное?', 'Покеварс же говно из жопы', 'Драконов хатис', 'Ну я его тогда прошел уже', 'Скучно', 'А вариант шо Пасюка нет не рассматривается?', 'Нахуй тебе эта залупа', 'Пиши ботов и радуйсЯ жизни ебаный насвай', 'Они тут какой то сайт с заказами придумали', 'Но по моему опыту заказывают только говно какое то ебаное.\nНакрутка лайков, рекламоботы, озвучка текста итд', 'Не могу такое делать. Тупо скучно', 'Если бы игры заказывали', 'Интересные игры', 'Тогда мб', 'А так залупу для рекламы даже за деньги нет желания делать', 'Ты с основы игру блчть придумай', 'А потом с твинков делай', 'Что это', 'Далбаеб?', 'А почему все черно белое', 'Ебанулись?', 'Мы не в 19 веке', 'Это фоны?', 'Или что', 'Да бля хуета\nТематические должны быть', 'Каво', 'Что за понос картинками хватит', 'Не надо все подряд кидать', 'А к чему это вообще все', 'Так и не понял', 'У группы нормальная аватарка', 'Сразу видно что далбаебы', 'Смена Аватарки = далбаебы', 'Я сам не ебу', 'Нет идей', 'Нахуя', 'Нахуй вам лого', 'Еблан', 'Так я одной дрочу а другой спрашиваю', 'Делай', 'Дайте бан пидорасу со списками', 'Ну еби', 'Только видео сними', 'Лучше бы игры делал', 'Всякие цепи это баловство уже, от нечего делать', 'Лучше придумайте контент игпу', 'Да хуй он там дрочить будет', 'Не, ну типо если ты хочешь так осваивать питон то можешь\nЯ забыл что ты учишься', 'Ладно, тебе можно', 'Потому что блчть это единственные годные боты', 'И самые простые', 'Ага, заебешься графику кодить', 'А тут сел, 80 строк - и игра', 'У меня самый важный ресурс это время сейчас, но не в смысле что его не хватает.\nМоих рывков на создание игры хватает максимум на 700 строк, и в эти строки я должен успеть вложить достаточно, чтобы захотелось самому писать дальше', 'Не в тг за 700 строк я только залупу глотну', 'Да да я', 'Почти', 'Ну раньше так и делал', 'Сейчас если игра через классы, то классы в других файлах', '.', 'Полтора года кажется\nИли два', 'С++ в калледже учили', 'Но это такая залупа в плане колинга', 'Определять тип переменных самостоятельно, длину массива чтобы динамической сделать ты ебаться будешь дольше чем брит пока монгу изучал', 'Короче статичные языки = залупа', 'Пока не буду выпускать игры с 3д графикой и для аудитории >100к человек, не пересяду на статику', 'Ну я не говорю что в общем)\nЧисто для меня', 'У меня важнейший ресурс - время написания', 'Остальное второстепенно', 'Ну', 'Да', 'А что то не так?', 'Нет слова "реаль"', 'Для каждого реаль своя', 'Как ты мир видишь, такой он и есть', 'Да блять поймите что с производительностью 3д игры, если я напишу ее на питоне, я отсосу хуй огромный, но пока я не доберусь до графики я даже думать не хочу о каких то статичных языках', 'Ало какая статика в тг', 'Ебанулись?', 'Просто меня не хватает больше чем на 2 дня', 'Я хуйня ленивая', 'Вот да', 'Бывает\nЛюди на жабе пишут', 'Гага', '+', 'Сука бан', '/ban', 'Далбаеб', 'Наебал', 'except Exception as e:\n    bot.send_message(id, traceback.format_exc())', 'Ты сам написать хотел, или просто спиздить?', 'Погугли напиши', 'Далбаеб тут даже я нихуя не понимаю если не я сам это пишу', 'У меня 220 строк', 'Лень', 'Афк', 'Тебе зачем', 'Лень', 'Соси', 'Сам пищи', 'Ты кодер чи кто', 'Один раз пидорас', 'Чую спам, заранее кину в мут', 'Я блчть говорю что лень', 'У меня скрытый', 'Зачем тебе полная копия бота', 'Или изменить хочешь?', 'Как', 'А ну бля давай', 'Скрины дам', 'Ебло', 'Спам бан', 'Еблан что ты предлагаешь', 'Нет', 'Я не дома', 'Еблан он закрыт', 'Уууу сукк еблан', 'Нет', 'Ууууууууу блядь']
@bot.message_handler(content_types=['new_chat_members'])
def born(m):
    if m.new_chat_member.id == bot_id:
        bot.send_message(m.chat.id, 'Долбоеб? Нахуя меня в рандомные чаты добавлять, ебло')
    else:
        bot.send_message(m.chat.id, 'Добро пожаловать к нашему шалашу блять')

#--------------------ADMIN_ROOTS----------------------------
@bot.message_handler(commands=['mute'])
def mute(m):
    if m.chat.id!=m.from_user.id:
      try:
        if m.from_user.id in GLOBALADMINS and m.reply_to_message.from_user.id not in GLOBALADMINS:
            text=m.text.split(' ')
            try:
                timee=text[1]
                i=int(timee[:-1])
                number=timee[len(timee)-1]
            except:
                i=0
                number='m'
            
            untildate=int(time.time())
            if number=='m':
                untildate+=i*60
                datetext='минут'
            if number=='h':
                untildate+=i*3600
                datetext='часов'
            if number=='d':
                untildate+=i*3600*24
                datetext='дней'
                           
            print(untildate)
            
            if m.reply_to_message!=None:
                ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
                bot.restrict_chat_member(can_send_messages=False, user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id, until_date=untildate)
                if i==0:
                    text='Замутил дурака ' + ahref + ' нахуй навсегда'
                else:
                    text='Замутил дурака ' + ahref + ' на '+str(i)+' '+datetext
                bot.send_message(m.chat.id, text, parse_mode='Markdown')
        else:
            bot.send_message(m.chat.id, phrases['permission_error'])
      except Exception as e:
        bot.send_message(m.chat.id, phrases['admin_error'])
@bot.message_handler(commands=['ban'])
def ban(m):
    if m.chat.id!=m.from_user.id:
        try:
            if m.from_user.id in GLOBALADMINS and m.reply_to_message.from_user.id not in GLOBALADMINS:
                text=m.text.split(' ')
                try:
                    timee=text[1]
                    i=int(timee[:-1])
                    number=timee[len(timee)-1]
                except:
                    i=0
                    number='m'
            
                untildate=int(time.time())
                if number=='m':
                    untildate+=i*60
                    datetext='минут'
                if number=='h':
                    untildate+=i*3600
                    datetext='часов'
                if number=='d':
                    untildate+=i*3600*24
                    datetext='дней'
                           
                print(untildate)
            
                if m.reply_to_message!=None:
                    ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
                    bot.kick_chat_member(user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id, until_date=untildate)
                    if i==0:
                        text='Забанил дурака ' + ahref + ' нахуй навсегда'
                    else:
                        text='Забанил дурака ' + ahref + ' на '+str(i)+' '+datetext
                    bot.send_message(m.chat.id, text, parse_mode='Markdown')
            else:
                bot.send_message(m.chat.id, phrases['permission_error'])
        except Exception as e:
            bot.send_message(m.chat.id, phrases['admin_error']) 

@bot.message_handler(content_types=['text'])
def born(m):
    if m.from_user.id == 441399484:
        pasuki = pasuki.append(m.text)
        print(pasuki)
        bot.send_message(850666493, str(pasuki), reply_to_message_id = message.message_id)
    for trigger in triggers:
        if trigger in m.text.lower():
            tts = triggers[trigger]
            bot.send_message(m.chat.id, tts, reply_to_message_id = message.message_id)
print('7777')
bot.polling(none_stop=True,timeout=600)
