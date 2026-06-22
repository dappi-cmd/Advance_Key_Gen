import hashlib
import hmac
import base64
import datetime


class KeyGenerator:
    def __init__(self, secret_salt="AdV@nCe_K3y_G3n#2024"):
        self.secret_salt = secret_salt

    def _clean_serial(self, value):
        cleaned = "".join(c for c in str(value).upper() if c.isalnum())
        return cleaned if cleaned else "UNKNOWN"

    def generate_key(self, hardware_info, key_length=16):
        raw = "|".join([
            self._clean_serial(hardware_info.get("motherboard", "")),
            self._clean_serial(hardware_info.get("ram", "")),
            self._clean_serial(hardware_info.get("vga", "")),
            self._clean_serial(hardware_info.get("hdd", "")),
            self._clean_serial(hardware_info.get("windows_key", "")),
            self._clean_serial(hardware_info.get("cpu", "")),
            self._clean_serial(hardware_info.get("mac", "")),
        ])

        today = datetime.date.today().strftime("%Y%m%d")
        raw_with_date = f"{raw}|{today}"

        hash_obj = hashlib.sha256(raw_with_date.encode("utf-8"))
        hex_digest = hash_obj.hexdigest().upper()

        hmac_obj = hmac.new(
            self.secret_salt.encode("utf-8"),
            hex_digest.encode("utf-8"),
            hashlib.sha256,
        )
        final_hash = hmac_obj.hexdigest().upper()

        key = final_hash[:key_length]

        formatted_key = "-".join(
            [key[i : i + 4] for i in range(0, len(key), 4)]
        )

        return formatted_key

    def generate_license_key(self, hardware_info):
        return self.generate_key(hardware_info, 16)

    def generate_activation_code(self, hardware_info):
        return self.generate_key(hardware_info, 25)

    def verify_key(self, key, hardware_info):
        expected = self.generate_license_key(hardware_info)
        return key.upper() == expected.upper()
