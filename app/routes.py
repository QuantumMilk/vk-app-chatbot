from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
import logging
from .config import settings
from .schemas import VKCallbackEvent
from .vk_client import vk_client

router = APIRouter()
logger = logging.getLogger(__name__)

# Отслеженные пользователи, которым уже отправлено приветствие
greeted_users = set()

@router.post("/vk_callback", response_class=PlainTextResponse)
async def vk_callback(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Некорректный JSON payload")

    event_type = payload.get("type")
    group_id = payload.get("group_id")
    secret_key = payload.get("secret")

    # Проверка секретного ключа и идентификатора сообщества
    if secret_key != settings.secret_key:
        logger.warning("Неверный SECRET_KEY!")
        raise HTTPException(status_code=403, detail="Неверный SECRET_KEY")
    if group_id != int(settings.group_id):
        logger.warning("Неверный group_id!")
        raise HTTPException(status_code=403, detail="Неверный group_id")

    # Обработка события подтверждения Callback API
    if event_type == "confirmation":
        return settings.confirmation_token

    # 1. Обработка события разрешения на отправку сообщений (например, при нажатии кнопки "Начать")
    if event_type == "message_allow":
        user_id = payload.get("object", {}).get("user_id")
        if user_id and user_id not in greeted_users:
            greeting_text = "Привет! Добро пожаловать в чат-бот."
            await vk_client.send_message(peer_id=user_id, text=greeting_text)
            greeted_users.add(user_id)
        return "ok"

    # 2. Обработка события статуса набора текста (если пользователь начал печатать)
    if event_type == "message_typing_state":
        user_id = payload.get("object", {}).get("from_id")
        if user_id and user_id not in greeted_users:
            greeting_text = "Привет! Добро пожаловать в чат-бот."
            await vk_client.send_message(peer_id=user_id, text=greeting_text)
            greeted_users.add(user_id)
        return "ok"

    # 3. Обработка события нового сообщения
    if event_type == "message_new":
        try:
            event = VKCallbackEvent.parse_obj(payload)
        except Exception as e:
            logger.error("Ошибка валидации данных: %s", e)
            raise HTTPException(status_code=400, detail="Ошибка валидации payload")
        
        message = event.object.message
        peer_id = message.peer_id

        # Если это системное сообщение (например, приглашение в чат), отправляем приветствие.
        if message.action and message.action.type in ["chat_invite_user", "chat_invite_user_by_link"]:
            joined_user_id = message.action.member_id
            if joined_user_id and joined_user_id not in greeted_users:
                greeting_text = "Привет! Добро пожаловать в чат-бот."
                await vk_client.send_message(peer_id=joined_user_id, text=greeting_text)
                greeted_users.add(joined_user_id)
            return "ok"

        # Если это первое сообщение (conversation_message_id == 1) и пользователь не написал текст, отправляем приветствие.
        if message.conversation_message_id == 1 and not message.text.strip() and peer_id not in greeted_users:
            greeting_text = "Привет! Добро пожаловать в чат-бот."
            await vk_client.send_message(peer_id, text=greeting_text)
            greeted_users.add(peer_id)
            return "ok"
        
        # Если в сообщении присутствуют вложения с фотографиями, отправляем их обратно
        photo_attachments = []
        if message.attachments:
            for att in message.attachments:
                if att.type == "photo" and att.photo:
                    owner_id = att.photo.owner_id
                    photo_id = att.photo.id
                    attachment_str = f"photo{owner_id}_{photo_id}"
                    if att.photo.access_key:
                        attachment_str += f"_{att.photo.access_key}"
                    photo_attachments.append(attachment_str)
        if photo_attachments:
            attachments_str = ",".join(photo_attachments)
            await vk_client.send_message(peer_id, attachments=attachments_str)
    
    return "ok"
