
import rsa
import cryptocode



def symmetrical_enc(secret):
    # Содаёт и возвращает ключи rsa
    # primaty key сразу симметрично шифруется по секретному ключу

    pbk, prk = rsa.newkeys(1024)
    encoded = cryptocode.encrypt(
        message=repr(prk),
        password=secret
    )

    return repr(pbk), encoded


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


def _chunked(file: bytes, n: int):
    temp = []

    start = 0
    n = int(n / 8 - 11)

    while start < len(file):
        temp.append(file[start: start + n])
        start += n

    return temp


# from Cryptodome.Cipher import PKCS1_v1_5
# from Cryptodome.PublicKey import RSA



# def encr(text: bytes, public):

#     rsa_key = RSA.importKey(public)
#     cipher = PKCS1_v1_5.new(rsa_key)
#     ciphertext = cipher.encrypt(text)

#     return ciphertext

# def decr(text: bytes, private):
#     rsa_key = RSA.importKey(private)
#     cipher = PKCS1_v1_5.new(rsa_key)

#     aes_key = cipher.decrypt(text, b'0')

#     return aes_key


# key = RSA.generate(1024)

# private = key.export_key()
# public = key.publickey().export_key()

# super_word = b"awdfeergsrg[oisrjgsoiijgpsoifjpsoijpsoijbp"
# print(super_word)

# encr_text = encr(super_word, public)
# print(encr_text)

# text = decr(encr_text, private)

# print(text)



# with open("test.jpg", "rb") as file:
#     data = file.read()

# data = encr(data, public)

# with open("encrypted.bin", "wb") as _out:
#     _out.write(data)

# data = decr(data, private)

# with open("decrypted.jpg", "wb") as _decrypt:
#     _decrypt.write(data)

# print("Done!")


n = 512
public, primary = rsa.newkeys(n)

def encr(file_name):
    with open(file_name, 'rb') as file:
        data = file.read()

        data = _chunked(data, n)

        for chunk in data:
            index = data.index(chunk)
            chunk = rsa.encrypt(chunk, public)
            data[index] = chunk
        
    with open(file_name + ".bin", "wb") as _out:
        for chunk in data:
            _out.write(chunk)
        
    return data
    

def decr(file_name, encrypted_data):
    for chunk in encrypted_data:
        index = encrypted_data.index(chunk)
        chunk = rsa.decrypt(
            bytes(chunk),
            priv_key=primary
        )
        encrypted_data[index] = chunk


    with open(file_name, "wb") as _out:
        for chunk in encrypted_data:
            _out.write(chunk)


if __name__ == "__main__":
    file_name = "test.jpg"
    
    data = encr(file_name)
    decr("new.jpg", data)

