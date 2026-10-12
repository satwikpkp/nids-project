import logging
from typing import Optional, Dict, Any, List
from backend.app.config import settings

logger = logging.getLogger("nids.database")

# In-memory mock store to guarantee flawless operation even if MongoDB daemon is not running locally
class InMemoryStore:
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.telemetry_history: List[Dict[str, Any]] = []

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.users.get(email.lower())

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        for user in self.users.values():
            if user.get("username", "").lower() == username.lower():
                return user
        return None

    def insert_user(self, user_dict: Dict[str, Any]) -> Dict[str, Any]:
        email = user_dict["email"].lower()
        self.users[email] = user_dict
        return user_dict

    def insert_alert(self, alert_dict: Dict[str, Any]) -> Dict[str, Any]:
        self.alerts.append(alert_dict)
        # Cap in-memory alert history to latest 500
        if len(self.alerts) > 500:
            self.alerts.pop(0)
        return alert_dict

    def get_recent_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        return list(reversed(self.alerts[-limit:]))

memory_store = InMemoryStore()

class DatabaseManager:
    client: Optional[Any] = None
    db: Optional[Any] = None
    is_connected_to_mongo: bool = False

    async def connect_to_database(self):
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=2000
            )
            # Ping database to verify connection
            await self.client.admin.command('ping')
            self.db = self.client[settings.DATABASE_NAME]
            self.is_connected_to_mongo = True
            logger.info("Connected successfully to MongoDB at %s", settings.MONGODB_URI)
        except Exception as e:
            self.is_connected_to_mongo = False
            logger.warning(
                "MongoDB not reachable (%s). Gracefully falling back to high-performance in-memory persistence layer.",
                str(e)
            )

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

db_manager = DatabaseManager()
