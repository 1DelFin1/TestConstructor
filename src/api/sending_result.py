import aiosmtplib
from email.message import EmailMessage

from src.core.config import settings


async def send_result_on_email(
    to_email: str,
    test_name: str,
    test_result: float,
    test_score: float,
):
    subject = f"Результат теста '{test_name}'"
    body = f"""
    Здравствуйте!
    Вы {"успешно" if test_score <= test_result else "не"} прошли тестирование.
        
    Ваш результат: {test_result}, порог прохождения: {test_score}.
    Спасибо за участие!
    """
    message = EmailMessage()
    message["From"] = settings.SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)
    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False
