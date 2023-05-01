from django.conf import settings
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import base64


class AESCipher(object):
    """
    Encrypt and Decrypt a String with AES Protocol
    """
    def __init__(self):
        self.block_size = 16
        self.key = base64.urlsafe_b64decode(settings.AES_ENCRYPTION_KEY)
        self.iv = base64.urlsafe_b64decode(settings.AES_ENCRYPTION_IV)

    def encrypt(self, plain_text):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_text = cipher.encrypt(pad(plain_text.encode(), self.block_size))
        encoded = base64.b64encode(encrypted_text)
        return encoded.decode()

    def decrypt(self, encrypted_text):
        encrypted_text = base64.b64decode(encrypted_text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_text = unpad(cipher.decrypt(encrypted_text), self.block_size)
        return decrypted_text.decode()
