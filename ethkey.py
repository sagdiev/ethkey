#!/usr/bin/env python3

import sys
import json
import argparse
import qrcode
import getpass

from eth_utils import address
from decrypt import Decrypter


def main(args):
    password = args.password
    if not password:
        print('Please enter wallet password: ')
        password = getpass.getpass()
    json_data = load_keystore_file(args.keystore_file)

    decrypter = Decrypter(json_data, password)
    encoded_address = address.to_checksum_address(json_data['address'])
    private_key = None
    try:
        private_key = decrypter.decrypt().hex()
    except ValueError as err:
        print(str(err), file=sys.stderr)
        exit(-1)
    print('public address: ' + encoded_address)
    print('private key: ' + private_key)
    if args.address_qr:
        generate_qr_code(address, args.address_qr)
    if args.private_key_qr:
        generate_qr_code(private_key, args.private_key_qr)


def load_keystore_file(filename):
    with open(filename) as keystore_file:
        data = json.load(keystore_file)
    return data


def generate_qr_code(plain_key, qr_code_filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(plain_key)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(qr_code_filename)


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Extract private key from Ethereum Wallet keystore file')
    parser.add_argument('keystore_file', type=str, help='path to the Ethereum keystore file.')
    parser.add_argument('--password', type=str, help='password of the keystore.')
    parser.add_argument('--address_qr', type=str, help='QR code image name representing the public wallet address')
    parser.add_argument('--private_key_qr', type=str, help='QR code image name representing the private key')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
