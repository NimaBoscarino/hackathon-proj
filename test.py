from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from huggingface_hub import get_repo_discussions, get_discussion_details
import base64

claim = get_discussion_details(
    repo_id="Team8/dataset",
    repo_type="dataset",
    discussion_num=int(5)
)

encryptedtext_encoded = claim.events[0].content
encrypted_text = base64.b64decode(encryptedtext_encoded)

file_in = open("encrypted_data.bin", "rb")

private_key = RSA.import_key(open("private.pem").read())

enc_session_key, nonce, tag, ciphertext = \
   [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
print(data.decode("utf-8"))
