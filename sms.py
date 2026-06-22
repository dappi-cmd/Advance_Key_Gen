import requests
import json


class SMSSender:
    def __init__(self):
        self.providers = {
            "TextBelt": {
                "url": "https://textbelt.com/text",
                "method": "POST",
                "format": "json",
                "payload": {"phone": None, "message": None, "key": "textbelt"},
                "response_key": "success",
            },
            "Fast2SMS": {
                "url": "https://www.fast2sms.com/dev/bulkV2",
                "method": "POST",
                "format": "json",
                "headers": {"authorization": None, "Content-Type": "application/json"},
                "payload": {
                    "route": "q",
                    "sender_id": "TXTIND",
                    "message": None,
                    "language": "english",
                    "flash": 0,
                    "numbers": None,
                },
                "response_key": "return",
            },
        }
        self.active_provider = "TextBelt"
        self.api_key = ""

    def set_provider(self, provider_name, api_key=""):
        if provider_name in self.providers:
            self.active_provider = provider_name
            self.api_key = api_key

    def send_sms(self, phone_number, message):
        provider = self.providers.get(self.active_provider)
        if not provider:
            return {"success": False, "error": "Invalid provider"}

        try:
            payload = dict(provider["payload"])
            headers = {}

            if self.active_provider == "TextBelt":
                payload["phone"] = phone_number
                payload["message"] = message
                if self.api_key:
                    payload["key"] = self.api_key

            elif self.active_provider == "Fast2SMS":
                headers = dict(provider.get("headers", {}))
                headers["authorization"] = self.api_key
                payload["numbers"] = phone_number
                payload["message"] = message
                payload = {k: v for k, v in payload.items() if v is not None}

            resp = requests.post(
                provider["url"],
                json=payload if provider["format"] == "json" else payload,
                headers=headers,
                timeout=30,
            )

            result = resp.json()
            success = result.get(provider["response_key"], False)

            return {
                "success": bool(success) if isinstance(success, bool) else success == "true",
                "response": result,
                "raw": resp.text,
            }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "No internet connection"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class SMSConfig:
    PROVIDER_TEXTBELT = "TextBelt"
    PROVIDER_FAST2SMS = "Fast2SMS"

    @staticmethod
    def get_providers():
        return [
            {"name": "TextBelt", "desc": "Free (1 text/day), no API key needed for basic"},
            {"name": "Fast2SMS", "desc": "Paid, requires API key (India numbers)"},
        ]

    @staticmethod
    def needs_api_key(provider):
        return provider != "TextBelt"
