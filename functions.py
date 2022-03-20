
import Cryptodome
import rsa
import cryptocode



def symmetrical_enc(secret):
    # Содаёт и возвращает ключи rsa
    # primaty key сразу симметрично шифруется по секретному ключу

    pbk, prk = rsa.newkeys(512)
    encoded = cryptocode.encrypt(
        message=repr(prk),
        password=secret
    )

    return repr(pbk), encoded, repr(prk)


def symmetrical_dec(encoded, secret) -> str:
    # Функция дешифрования

    decoded = cryptocode.decrypt(
        enc_dict=encoded,
        password=secret
    )

    # Возвращает исходное слово, только в случае когда поле password правильное, иначе false
    return decoded




def to_key(key):
    # Преобразует из str в ключи

    import re
    nums = re.findall("\d+", key)
    args = map(int, nums)
    if len(nums) < 3:
        return rsa.PublicKey(*args)

    else:
        return rsa.PrivateKey(*args)
    



# password = "qwerty"

# pbk, prk, answer = symmetrical_enc(password)

# pbk = to_key(pbk)

# prk = symmetrical_dec(prk, password)

# print(prk == answer)


def chunked(file: bytes, n: int):
    temp = []

    start = 0
    n = int(n / 8 - 11)

    while start < len(file):
        temp.append(file[start: start + n])
        start += n

    return temp


from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
import Cryptodome.Random as Random
from base64 import b64encode
from base64 import b64decode

class RSA_Cipher:
  def generate_key(self, key_length):
    assert key_length in [1024,2048,4096]
    rng = Random.new().read
    self.key = RSA.generate(key_length,rng)

  def encrypt(self, data):
    plaintext = b64encode(data.encode())
    rsa_encryption_cipher = PKCS1_v1_5.new(self.key)
    ciphertext = rsa_encryption_cipher.encrypt(plaintext)
    return b64encode(ciphertext).decode()

  def decrypt(self,data):
    ciphertext = b64decode(data.encode())
    rsa_decryption_cipher = PKCS1_v1_5.new(self.key)
    plaintext = rsa_decryption_cipher.decrypt(ciphertext,16)
    return b64decode(plaintext).decode()


chiper = RSA_Cipher()
chiper.generate_key(1024)



key = RSA.generate(1024)
private = key.export_key()

public = key.publickey().export_key()

import Cryptodome


from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
aes_key = get_random_bytes(16)
rsa_key = RSA.importKey(public)
cipher = PKCS1_v1_5.new(rsa_key)
ciphertext = cipher.encrypt(aes_key)


from Cryptodome.Random import get_random_bytes
rsa_key = RSA.importKey(private)
sentinel = get_random_bytes(16)
cipher = PKCS1_v1_5.new(rsa_key)
aes_key = cipher.decrypt(ciphertext, sentinel, expected_pt_len=16)


# n = 512
# public, primary = rsa.newkeys(n)
# print(public, primary, sep='\n')

# with open('test.jpg', 'br') as file:
    

#     data = file.read()

#     temp = chunked(data, n)


#     for chunk in temp:
#         index = temp.index(chunk)

#         chunk = rsa.encrypt(chunk, public)

#         temp[index] = chunk


#     with open("encrypted.bin", "wb") as _out:
#         for chunk in temp:
#             _out.write(chunk)
#         pass
    
#     print("Done!")
    
    
# with open("encrypted.bin", "rb") as file:
#     data = file.read()

    


#     for chunk in temp:
#         index = temp.index(chunk)

#         print(len(chunk))

#         chunk = rsa.decrypt(
#             bytes(chunk),
#             priv_key=primary
#         )

#         temp[index] = chunk


#     with open("decrypted.jpg", "wb") as _out:
#         for chunk in temp:
#             _out.write(chunk)
    


