from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://astroshoppingdigital_db_user:grbWr4hMXImw2Q8j@crypto.huibgar.mongodb.net/?retryWrites=true&w=majority&appName=crypto"
DATABASE_NAME = "crypto"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]