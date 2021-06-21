import hashlib


def dm(user_1_id, user_2_id):
    id_1 = None
    id_2 = None
    if user_1_id > user_2_id:
        id_1 = str(user_1_id).encode()
        id_2 = str(user_2_id).encode()
    else:
        id_1 = str(user_2_id).encode()
        id_2 = str(user_1_id).encode()

    hash_1 = hashlib.sha256(id_1).hexdigest()
    hash_2 = hashlib.sha256(id_2).hexdigest()
    return hash_1+hash_2