import os

from dotenv import load_dotenv

load_dotenv()

QIWI_TOKEN = os.getenv("qiwi")
WALLET_QIWI = os.getenv("wallet")
QIWI_PUBKEY = os.getenv("qiwi_pub_key")

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

token = str(os.getenv('token'))
vk_token_bot = str(os.getenv('vk_token_bot'))
version = str(os.getenv('version'))

ip = os.getenv("ip")
#
db_host = ip

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{DATABASE}"
