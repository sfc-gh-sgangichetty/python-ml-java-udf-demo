import os
os.environ['PRIVATE_KEY_PASSPHRASE'] = '****'  #update with your passphrase
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

def get_pkb():
    #should be updated to your privatekey
    with open("../my_pk/rsa_key.p8", "rb") as key:
        p_key= serialization.load_pem_private_key(
            key.read(),
            password=os.environ['PRIVATE_KEY_PASSPHRASE'].encode(),
            backend=default_backend()
        )
    account_id ='*****' # add your account_id here
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    return account_id,pkb