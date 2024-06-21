# DB Infos
ID = "root"
PWD = "0000"
HOST = "localhost"
PORT = 3306
DB_NAME = "logos"

# PyJWT Secret Key
JWT_SECRET_KEY = "[YOUR KEY HERE]"

# SQLAlchemy Connection String(DB URL)
DB_URL = f"mysql+pymysql://{ID}:{PWD}@{HOST}:{PORT}/{DB_NAME}"