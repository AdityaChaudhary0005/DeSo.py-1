import requests
import jwt
import binascii
from base58 import b58decode_check
from ecdsa import SECP256k1, VerifyingKey, SigningKey


def submitTransaction(signedTransactionHex, nodeURL):
    endpointURL = nodeURL + "submit-transaction"
    payload = {'TransactionHex': signedTransactionHex}
    response = requests.post(endpointURL, json=payload)
    return response


def appendExtraData(transactionHex, derivedKey, nodeURL):

    payload = {"TransactionHex": transactionHex,
               "ExtraData": {"DerivedPublicKey": derivedKey}}
    endpoint = nodeURL + "append-extra-data"
    response = requests.post(endpoint, json=payload)
    return response


def validateJWT(JWT, publicKey):
    # this method is used to for public key validation
    try:
        rawPublicKeyHex = b58decode_check(publicKey)[3:].hex()
        public_key = bytes(rawPublicKeyHex, 'utf-8')
        public_key = binascii.unhexlify(public_key)
        key = VerifyingKey.from_string(public_key, curve=SECP256k1)
        key = key.to_pem()
        decoded = jwt.decode(JWT, key, algorithms=['ES256'])
        return {"isValid": True, "decodedJWT": decoded}
    except Exception as e:
        return {"isValid": False, "error": str(e)}


def getUserJWT(seedHex):
    # returns JWT token of user that helps in public key validation in backend
    private_key = bytes(seedHex, 'utf-8')
    private_key = binascii.unhexlify(private_key)
    key = SigningKey.from_string(private_key, curve=SECP256k1)
    key = key.to_pem()
    encoded_jwt = jwt.encode({}, key, algorithm="ES256")
    return encoded_jwt
