from flask import jsonify, Response

class ResponseBuilder:
    
    @staticmethod
    def success(data=None, message: str = "Operação realizada com sucesso", status_code: int = 200):
        response_payload = {
            "success": True,
            "data": data,
            "message": message
        }
        return jsonify(response_payload), status_code

    @staticmethod
    def error(code: str, message: str, details=None, status_code: int = 400):
        response_payload = {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details
            }
        }
        return jsonify(response_payload), status_code
