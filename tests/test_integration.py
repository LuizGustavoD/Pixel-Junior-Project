import unittest
import requests
import io
import time

AUTH_URL = "http://localhost:5000"
RESOURCE_URL = "http://localhost:5001"

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Wait for services to be online (up to 15 seconds)
        print("Aguardando os serviços subirem no Docker...")
        for i in range(15):
            try:
                auth_resp = requests.get(f"{AUTH_URL}/health", timeout=2)
                if auth_resp.status_code == 200:
                    print("Serviço de Autenticação está online!")
                    break
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(1)
        else:
            raise RuntimeError("Serviço de Autenticação não iniciou a tempo.")

    def test_end_to_end_flow(self):
        print("\n[Passo 1] Testando Health Checks...")
        resp = requests.get(f"{AUTH_URL}/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("status"), "healthy")

        resp = requests.get(f"{AUTH_URL}/status")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))

        print("[Passo 2] Registrando novo usuário...")
        user_email = f"int_test_{int(time.time())}@example.com"
        user_username = f"int_user_{int(time.time())}"
        user_password = "Password123!"

        register_payload = {
            "email": user_email,
            "username": user_username,
            "password": user_password
        }

        resp = requests.post(f"{AUTH_URL}/auth/register", json=register_payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertTrue(data.get("success"))
        user_id = data["data"]["id"]
        self.assertIsNotNone(user_id)

        resp_dup = requests.post(f"{AUTH_URL}/auth/register", json=register_payload)
        self.assertEqual(resp_dup.status_code, 400)
        self.assertEqual(resp_dup.json()["error"]["code"], "USER_ALREADY_EXISTS")

        print("[Passo 3] Fazendo login para obter token JWT...")
        login_payload = {
            "email": user_email,
            "password": user_password
        }
        resp = requests.post(f"{AUTH_URL}/auth/login", json=login_payload)
        self.assertEqual(resp.status_code, 200)
        login_data = resp.json()
        self.assertTrue(login_data.get("success"))
        token = login_data["data"]["access_token"]
        self.assertIsNotNone(token)

        print("[Passo 4] Buscando chave pública do servidor de autenticação...")
        resp = requests.get(f"{AUTH_URL}/token/public-key")
        self.assertEqual(resp.status_code, 200)
        pub_key_data = resp.json()
        self.assertTrue(pub_key_data.get("success"))
        self.assertIn("public_key", pub_key_data["data"])

        print("[Passo 5] Verificando validade do token JWT no servidor de autenticação...")
        resp = requests.post(f"{AUTH_URL}/token/verify", json={"token": token})
        self.assertEqual(resp.status_code, 200)
        verify_data = resp.json()
        self.assertTrue(verify_data.get("success"))
        self.assertEqual(verify_data["data"]["user_id"], user_id)

        headers = {"Authorization": f"Bearer {token}"}

        print("[Passo 6] Validando status no servidor de recursos (validação de token integrada)...")
        resp = requests.get(f"{RESOURCE_URL}/health/status", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))
        self.assertEqual(resp.json()["data"]["authenticated_user_id"], user_id)

        resp = requests.get(f"{RESOURCE_URL}/files/status", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))

        print("[Passo 7] Listando arquivos no servidor de recursos...")
        resp = requests.get(f"{RESOURCE_URL}/files", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()["data"]), 0)

        print("[Passo 8] Fazendo upload de arquivo de imagem no servidor de recursos...")
        img_data = (
            b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06"
            b"\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a"
            b"\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01"
            b"\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00"
            b"\x3f\x00\x37\xff\xd9"
        )
        files = {"file": ("integration_photo.jpg", io.BytesIO(img_data), "image/jpeg")}
        resp = requests.post(f"{RESOURCE_URL}/files/upload", headers=headers, files=files)
        self.assertEqual(resp.status_code, 201)
        upload_data = resp.json()
        self.assertTrue(upload_data.get("success"))
        file_id = upload_data["data"]["id"]
        self.assertIsNotNone(file_id)

        print("[Passo 9] Confirmando que o arquivo foi listado...")
        resp = requests.get(f"{RESOURCE_URL}/files", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()["data"]), 1)
        self.assertEqual(resp.json()["data"][0]["id"], file_id)

        print("[Passo 10] Baixando arquivo original...")
        resp = requests.get(f"{RESOURCE_URL}/files/download/{file_id}", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, img_data)

        print("[Passo 11] Recuperando miniatura da imagem...")
        resp = requests.get(f"{RESOURCE_URL}/files/thumbnail/{file_id}", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "image/jpeg")

        print("[Passo 12] Deletando arquivo...")
        resp = requests.delete(f"{RESOURCE_URL}/files/delete/{file_id}", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))

        print("[Passo 13] Verificando exclusão do arquivo...")
        resp = requests.get(f"{RESOURCE_URL}/files/download/{file_id}", headers=headers)
        self.assertEqual(resp.status_code, 404)

        print("\nBateria de Testes de Integração concluída com sucesso! Todos os testes passaram.")

if __name__ == "__main__":
    unittest.main()
