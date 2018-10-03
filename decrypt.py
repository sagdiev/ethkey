import scrypt
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import keccak


class Decrypter:

    def __init__(self, json_data, password):
        self.__extract_variables_from_json__(json_data)
        self.password = password

    def decrypt(self):
        dec_key = self.__compute_derivation_key__()
        self.__validate_password__(dec_key)
        return self.__decrypt_derived_key__(dec_key)

    def __extract_variables_from_json__(self, json_data):
        crypto = json_data['Crypto']
        cipher = crypto['cipher']
        if cipher != 'aes-128-ctr':
            raise ValueError('The used cipher is not aes-128-ctr')
        self.ciphertext = crypto['ciphertext']
        self.iv = crypto['cipherparams']['iv']
        kdf = crypto['kdf']
        if kdf != 'scrypt':
            raise ValueError('The used hashing function is not scrypt')
        kdfparams = crypto['kdfparams']
        self.dklen = kdfparams['dklen']
        self.n = kdfparams['n']
        self.p = kdfparams['p']
        self.r = kdfparams['r']
        self.salt = kdfparams['salt']
        self.mac = crypto['mac']

    def __compute_derivation_key__(self):
        scrypt_hash = scrypt.hash(password=bytes(self.password, 'utf-8'),
                                  salt=bytes.fromhex(self.salt),
                                  N=self.n,
                                  r=self.r,
                                  p=self.p,
                                  buflen=self.dklen)
        return scrypt_hash

    def __validate_password__(self, dec_key):
        validate = dec_key[16:] + bytes.fromhex(self.ciphertext)
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(validate)
        if keccak_hash.hexdigest() != self.mac:
            raise ValueError('Error: incorrect password')

    def __decrypt_derived_key__(self, dec_key):
        iv_int = int(self.iv, 16)
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
        dec_suite = AES.new(dec_key[:16], AES.MODE_CTR, counter=ctr)
        plain_key = dec_suite.decrypt(bytes.fromhex(self.ciphertext))
        return plain_key
