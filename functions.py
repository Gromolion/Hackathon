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
    



password = "qwerty"

pbk, prk, answer = symmetrical_enc(password)

pbk = to_key(pbk)

prk = symmetrical_dec(prk, password)

print(prk == answer)









