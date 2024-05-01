import vkbottle
import config
import json
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard
from vkbottle.tools import DocMessagesUploader

bot = Bot(config.vk_token_bot)

@bot.on.message(text="СЧС")
async def hi_handler(message: Message):
    
'url': 'https://vk.com/doc557331518_597827316?hash=01922e9bc569ecf3ac&dl=GU2TOMZTGE2TCOA:1620754718:e0a6f85b3ce15302a4&api=1&no_preview=1', 'access_key': 'e5f549bbea55ef59d7'

vk_session = vk_api.VkApi(token = config.vk_token_bot, api_version = config.version)
vk_session._auth_token()
vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 204477517)

def send_message(id, text, keyboard=None, template=None):
    random_id = vk_api.utils.get_random_id()
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': get_random_id(),
                                        'keyboard': keyboard, 'template': template})


while True:
    for event in longpoll.listen():
        if event.object.message["text"] == 'СЧС':
                if event.from_user:
                    # Если клиент пользователя не поддерживает callback-кнопки, нажатие на них будет отправлять текстовые
                    # сообщения. Т.е. они будут работать как обычные inline кнопки.
                    if "callback" not in event.object.client_info["button_actions"]:
                        print(
                            f'Клиент user_id{event.obj.message["from_id"]} не поддерживает callback-кнопки.'
                        )
                    payment = Payment(980)
                    payment.create()

                    keyboard_1 = VkKeyboard(one_time=False, inline=True)
                    keyboard_1.add_openlink_button("Оплатить 💰", payment.invoice)
                    keyboard_1.add_line()
                    keyboard_1.add_callback_button(
                            label="Появились проблемы? 🤔",
                            color=VkKeyboardColor.PRIMARY,
                            payload={"type": "problem", "text": "По всем экстренным вопросам обращайтесь к <a href='t.me/georgiisidorov10'>@georgiisidorov10</a>"},
                    )
                    keyboard_1.add_line()
                    keyboard_1.add_callback_button(
                            label="Готово ✅",
                            color=VkKeyboardColor.POSITIVE,
                            payload={"type": "ready"},
                    )
                    send_message(
                        event.object.message["from_id"],
                        "Чтобы получить файлы, произведите оплату на сумму 1000",
                        keyboard=keyboard_1.get_keyboard()
                    )

        else:
            if event.object.payload.get("type") == "ready":
                try:
                    payment.check_payment()
                except NoPaymentFound:
                    vk.messages.send(
                        user_id=event.obj.message["from_id"],
                        random_id=get_random_id(),
                        peer_id=event.obj.message["from_id"],
                        message="Транзакция не найдена",
                    )
                except NotEnoughMoney:
                    vk.messages.send(
                        user_id=event.obj.message["from_id"],
                        random_id=get_random_id(),
                        peer_id=event.obj.message["from_id"],
                        message="Оплаченная сумма меньше необходимой",
                    )
                else:
                    vk.messages.send(
                        user_id=event.obj.message["from_id"],
                        random_id=get_random_id(),
                        peer_id=event.obj.peer_id,
                        message="Вот СЧС-списки, мы рады были Вам угодить!",
                        attachment='doc557331518_597827316'
                    )
