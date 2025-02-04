from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
import logging
from .config import settings
from .schemas import VKCallbackEvent
from .vk_client import vk_client

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/vk_callback", response_class=PlainTextResponse)
async def vk_callback(request: Request):
    """
    Основной endpoint для обработки Callback API от ВКонтакте.
    """
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Некорректный JSON payload")

    event_type = payload.get("type")
    group_id = payload.get("group_id")
    secret_key = payload.get("secret")
    
    # Проверяем, что запрос пришёл от ВКонтакте и содержит правильный секретный ключ
    if secret_key != settings.secret_key:
        logger.warning("Попытка запроса с неверным SECRET_KEY!")
        raise HTTPException(status_code=403, detail="Неверный SECRET_KEY")

    # Проверяем, что запрос пришел от нужного сообщества
    if group_id != int(settings.group_id):
        logger.warning(f"Попытка запроса с неверным group_id: {group_id}")
        raise HTTPException(status_code=403, detail="Неверный group_id")

    # Обработка подтверждения Callback API
    if event_type == "confirmation":
        return settings.confirmation_token

    # Обработка нового сообщения
    if event_type == "message_new":
        try:
            event = VKCallbackEvent.parse_obj(payload)
        except Exception as e:
            logger.error("Ошибка валидации данных: %s", e)
            raise HTTPException(status_code=400, detail="Ошибка валидации payload")
        
        message = event.object.message
        peer_id = message.peer_id

        # Если это первое сообщение в диалоге, отправляем приветствие
        if message.conversation_message_id == 1:
            greeting_text = "Привет! Добро пожаловать в наш чат-бот."
            await vk_client.send_message(peer_id, text=greeting_text)
        
        # Обработка вложений: отправляем обратно фотографии, если они есть
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