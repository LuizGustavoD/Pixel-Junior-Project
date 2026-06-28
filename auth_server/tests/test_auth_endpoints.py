import os
import sys
import unittest

# Set SQLite in-memory database URL before importing the app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Add app path
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
sys.path.insert(0, APP_DIR)

from main import app
from infra.config.db import engine, SessionLocal
from infra.models.user_model import Base, UserModel
from infra.security.password_hasher import PasswordHasher

class TestAuthEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure tables are created in the in-memory SQLite DB
        Base.metadata.create_all(bind=engine)
        cls.client = app.test_client()
        cls.hasher = PasswordHasher()

    def setUp(self):
        # Clear users table before each test
        db = SessionLocal()
        try:
            db.query(UserModel).delete()
            db.commit()
        finally:
            db.close()

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "healthy")

    def test_status_check(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["data"]["service"], "auth_server")

    def test_register_user_success(self):
        payload = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123!"
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["data"]["email"], "test@example.com")
        self.assertEqual(data["data"]["username"], "testuser")
        self.assertIn("id", data["data"])

    def test_register_user_validation_error(self):
        # Missing fields
        payload = {
            "email": "test@example.com"
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data["error"]["code"], "VALIDATION_ERROR")

    def test_register_user_duplicate_email(self):
        # Register user first
        db = SessionLocal()
        try:
            hashed = self.hasher.hash("Password123!")
            user = UserModel(email="duplicate@example.com", username="user1", password=hashed)
            db.add(user)
            db.commit()
        finally:
            db.close()

        payload = {
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "Password123!"
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data["error"]["code"], "USER_ALREADY_EXISTS")

    def test_login_success(self):
        db = SessionLocal()
        try:
            hashed = self.hasher.hash("Password123!")
            user = UserModel(email="login@example.com", username="loginuser", password=hashed)
            db.add(user)
            db.commit()
        finally:
            db.close()

        payload = {
            "email": "login@example.com",
            "password": "Password123!"
        }
        response = self.client.post("/auth/login", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("access_token", data["data"])

    def test_login_invalid_password(self):
        # Register a user manually
        db = SessionLocal()
        try:
            hashed = self.hasher.hash("Password123!")
            user = UserModel(email="login_fail@example.com", username="loginfail", password=hashed)
            db.add(user)
            db.commit()
        finally:
            db.close()

        payload = {
            "email": "login_fail@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post("/auth/login", json=payload)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data["error"]["code"], "INVALID_CREDENTIALS")

    def test_get_public_key(self):
        response = self.client.get("/token/public-key")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("public_key", data["data"])
        self.assertTrue(data["data"]["public_key"].startswith("-----BEGIN PUBLIC KEY-----"))

    def test_verify_token_success(self):
        # Register and login to get a real token
        db = SessionLocal()
        try:
            hashed = self.hasher.hash("Password123!")
            user = UserModel(email="verify@example.com", username="verifyuser", password=hashed)
            db.add(user)
            db.commit()
            user_id = user.id
        finally:
            db.close()

        login_response = self.client.post("/auth/login", json={
            "email": "verify@example.com",
            "password": "Password123!"
        })
        token = login_response.get_json()["data"]["access_token"]

        # Verify via JSON payload
        response = self.client.post("/token/verify", json={"token": token})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["data"]["user_id"], user_id)

        # Verify via Header
        response_header = self.client.post("/token/verify", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_header.status_code, 200)
        data_header = response_header.get_json()
        self.assertTrue(data_header.get("success"))
        self.assertEqual(data_header["data"]["user_id"], user_id)

    def test_verify_token_failure(self):
        response = self.client.post("/token/verify", json={"token": "invalid.token.string"})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data["error"]["code"], "INVALID_CREDENTIALS")

if __name__ == "__main__":
    unittest.main()
