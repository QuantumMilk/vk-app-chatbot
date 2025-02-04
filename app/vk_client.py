import random
import logging 
from typing import Optional
import httpx
from .config import settings

logger = logging.getLogger(__name__)

class VKClient:
    """
    Класс для работы с VK API
    """
    base_url = "https://api.vk.com/method"

    def __init__(self):
        self.token = settings.vk_token
        self.api_version = settings.api_version

    async def send_message(self, peer_id: int, text: str = "", attachments: Optional[str] = None) -> dict:
        """
        Отправка сообщения пользователю через VK API.

        :param peer_id: ID пользователя/чата
        :param text: Текст сообщения
        :param attachments: Строка с вложениями (например, "photo12345_67890")
        :return: JSON-ответ от VK API
        """
        params = {
            "peer_id": peer_id,
            "message": text,
            "attachment": attachments or "",
            "random_id": random.randint(1, 10**9),
            "access_token": self.token,
            "v": self.api_version,
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.base_url}/messages.send",
                                             params=params,
                                             timeout=10)
                response.raise_for_status()
                data = response.json()
                logger.info(f"VK API response: {data}")
                return data
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения: {e}")
                raise e
    
vk_client = VKClient()