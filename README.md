# ethkey

An Ethereum wallet consists of a _public address_ and a _private key_.
When using the [Ethereum Wallet / Mist Browser](https://github.com/ethereum/mist/releases)
or when running the [geth](https://geth.ethereum.org/downloads/)
Ethereum node the wallet information is stored in a
[keystore](https://medium.com/@julien.maffre/what-is-an-ethereum-keystore-file-86c8c5917b97) file.
In this file the private key is encrypted using the wallet's password.

The _ethkey_ tool reads the keystore file and extracts the decrypted private key and the
[checksum encoded](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md) public wallet address.
It is also possible to generate QR code images of the key and the address.

## Installation Requirements
* [python 3.x](https://realpython.com/installing-python) must be installed
* relevant python packes must be installed using `pip install -r requirements.txt`

## Usage
```
python ethkey.py [-h] [--password PASSWORD] [--address_qr ADDRESS_QR] [--private_key_qr PRIVATE_KEY_QR] keystore_file

positional arguments:
  keystore_file                     path to the Ethereum keystore file.

optional arguments:
  -h, --help                        show this help message and exit
  --password PASSWORD               password of the keystore (use with care!).
  --address_qr ADDRESS_QR           QR code image name representing the public wallet address
  --private_key_qr PRIVATE_KEY_QR   QR code image name representing the private key
```
If the password parameter is omitted the user is prompted for the wallet password.
Since commands are typically stored in the shell history this is the more secure and preferred approach.
If the image name parameters are provided, QR code images are generated for the address and the key, respectively.

An example call would look like this:
```
python ethkey.py ~/Library/Ethereum/keystore/UTC--2016-02-29T20-16-53.925667321Z--0af977bb21cf972a538187f72299614121549454 \
  --address_qr=address.png \
  --private_key_qr=key.png
``` 
