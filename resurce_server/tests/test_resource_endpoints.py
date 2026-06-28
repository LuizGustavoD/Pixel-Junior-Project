import os
import sys
import unittest
import io
import shutil
import tempfile
from unittest.mock import patch

# Configure SQLite in-memory database URL and a temporary storage directory
TEST_DIR = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["UPLOAD_DIR"] = TEST_DIR

# Add app path to sys.path
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
sys.path.insert(0, APP_DIR)

from main import app
from infra.config.db import engine, SessionLocal, Base
from infra.models.file_model import FileModel

# Create a mock user ID
MOCK_USER_ID = "11111111-2222-3333-4444-555555555555"

class TestResourceEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_DIR, ignore_errors=True)

    def setUp(self):
        # Clear files table
        db = SessionLocal()
        try:
            db.query(FileModel).delete()
            db.commit()
        finally:
            db.close()

        # Start patching verify_token_locally to always authorize our MOCK_USER_ID
        self.patcher_verify_local = patch("infra.security.auth_middleware.verify_token_locally", return_value=MOCK_USER_ID)
        self.mock_verify_local = self.patcher_verify_local.start()

        # Also patch verify_token_remotely just in case
        self.patcher_verify_remote = patch("infra.security.auth_middleware.verify_token_remotely", return_value=MOCK_USER_ID)
        self.mock_verify_remote = self.patcher_verify_remote.start()

    def tearDown(self):
        self.patcher_verify_local.stop()
        self.patcher_verify_remote.stop()

    def test_status_health_endpoints(self):
        # Needs Authorization header to pass middleware check
        headers = {"Authorization": "Bearer mock-token"}
        
        # Test health status check
        response = self.client.get("/health/status", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["data"]["authenticated_user_id"], MOCK_USER_ID)

        # Test files status check
        response = self.client.get("/files/status", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["data"]["authenticated_user_id"], MOCK_USER_ID)

    def test_upload_and_list_files(self):
        headers = {"Authorization": "Bearer mock-token"}
        
        # Upload a file
        file_data = {
            "file": (io.BytesIO(b"Hello World PDF Content"), "sample.pdf")
        }
        response = self.client.post(
            "/files/upload",
            headers=headers,
            data=file_data,
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["data"]["original_name"], "sample.pdf")
        self.assertEqual(data["data"]["content_type"], "application/pdf")
        
        # Verify it lists the file
        response_list = self.client.get("/files", headers=headers)
        self.assertEqual(response_list.status_code, 200)
        data_list = response_list.get_json()
        self.assertTrue(data_list.get("success"))
        self.assertEqual(len(data_list["data"]), 1)
        self.assertEqual(data_list["data"][0]["original_name"], "sample.pdf")

    def test_upload_file_invalid_extension(self):
        headers = {"Authorization": "Bearer mock-token"}
        file_data = {
            "file": (io.BytesIO(b"some invalid extension data"), "sample.exe")
        }
        response = self.client.post(
            "/files/upload",
            headers=headers,
            data=file_data,
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data["error"]["code"], "UNSUPPORTED_TYPE")
        self.assertIn("Extensão de arquivo não permitida", data["error"]["message"])

    def test_upload_file_exceeds_size(self):
        headers = {"Authorization": "Bearer mock-token"}
        # 10MB + 1 byte
        large_data = b"x" * (10 * 1024 * 1024 + 1)
        file_data = {
            "file": (io.BytesIO(large_data), "huge_image.png")
        }
        response = self.client.post(
            "/files/upload",
            headers=headers,
            data=file_data,
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data["error"]["code"], "FILE_TOO_LARGE")
        self.assertIn("excede o limite máximo", data["error"]["message"])

    def test_download_file(self):
        headers = {"Authorization": "Bearer mock-token"}
        
        # Upload a file
        file_data = {
            "file": (io.BytesIO(b"Secret Document Data"), "doc.txt")
        }
        response = self.client.post(
            "/files/upload",
            headers=headers,
            data=file_data,
            content_type="multipart/form-data"
        )
        file_id = response.get_json()["data"]["id"]

        # Download the file
        response_download = self.client.get(f"/files/download/{file_id}", headers=headers)
        self.assertEqual(response_download.status_code, 200)
        self.assertEqual(response_download.data, b"Secret Document Data")
        self.assertEqual(response_download.headers.get("Content-Disposition"), "attachment; filename=doc.txt")

    def test_thumbnail_retrieval(self):
        headers = {"Authorization": "Bearer mock-token"}

        # Create a tiny 1x1 pixel JPEG in memory
        # JPEG signature/content
        img_data = (
            b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06"
            b"\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a"
            b"\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01"
            b"\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00"
            b"\x3f\x00\x37\xff\xd9"
        )

        # Upload the image file
        file_data = {
            "file": (io.BytesIO(img_data), "photo.jpg")
        }
        response = self.client.post(
            "/files/upload",
            headers=headers,
            data=file_data,
            content_type="multipart/form-data"
        )
        file_id = response.get_json()["data"]["id"]

        # Retrieve thumbnail
        response_thumb = self.client.get(f"/files/thumbnail/{file_id}", headers=headers)
        self.assertEqual(response_thumb.status_code, 200)
        self.assertEqual(response_thumb.content_type, "image/jpeg")

    def test_delete_file(self):
        headers = {"Authorization": "Bearer mock-token"}

        # Upload a file
        file_data = {
            "file": (io.BytesIO(b"Delete me"), "delete_target.txt")
        }
        response = self.client.post(
            "/files/upload",
            headers=headers,
            data=file_data,
            content_type="multipart/form-data"
        )
        file_id = response.get_json()["data"]["id"]

        # Delete the file
        response_delete = self.client.delete(f"/files/delete/{file_id}", headers=headers)
        self.assertEqual(response_delete.status_code, 200)
        self.assertTrue(response_delete.get_json().get("success"))

        # Verify downloading the deleted file returns 404
        response_download = self.client.get(f"/files/download/{file_id}", headers=headers)
        self.assertEqual(response_download.status_code, 404)

if __name__ == "__main__":
    unittest.main()
