import unittest
import json
from decrypt import Decrypter


class DecrypterTest(unittest.TestCase):
    plain_key = '0000000000000000000000000000000000000000000000000000000000000001'
    password = 'a'
    incorrect_password = 'foo'
    json_string = """
        {  
           "address":"7e5f4552091a69125d5dfcb7b8c2659029395bdf",
           "Crypto":{  
              "cipher":"aes-128-ctr",
              "ciphertext":"f97975cb858242372a7c910de23976be4f545ad6b4d6ddb86e54b7d9b3b1c6a1",
              "cipherparams":{  
                 "iv":"7fa01f1d0d6a7117382632028cb0c323"
              },
              "kdf":"scrypt",
              "kdfparams":{  
                 "dklen":32,
                 "n":262144,
                 "p":1,
                 "r":8,
                 "salt":"859c5d345ee58dfca293950c540016af3a889d0dacb00b8eff2ac2b150f0b07e"
              },
              "mac":"31ccb67e48aba5d64bf727a5c6589fd5857021540d25d12df31323f10ae2bf97"
           },
           "id":"dc74bc44-784b-4293-b1c7-b91e9fd7d6cc",
           "version":3
        }
    """

    def testDecrypt(self):
        json_data = json.loads(self.json_string)
        decrypter = Decrypter(json_data, self.password)
        decrypted_plain_key = decrypter.decrypt()
        self.assertEqual(decrypted_plain_key.hex(), self.plain_key)


    def testWrongPassword(self):
        json_data = json.loads(self.json_string)
        decrypter = Decrypter(json_data, self.incorrect_password)
        try:
            decrypter.decrypt()
            self.fail('decrypter should fail with incorrect password')
        except ValueError as err:
            self.assertEqual(str(err), 'Error: incorrect password')


if __name__ == "__main__":
    unittest.main()
