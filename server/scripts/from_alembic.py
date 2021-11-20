import dotenv

dotenv.load_dotenv("server.env")

from db import metadata
from mails.models import Mail, Email, EmailFromMail
from domains.models import Domain
from users.models import User
