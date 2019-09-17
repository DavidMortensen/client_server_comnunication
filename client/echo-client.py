#!/usr/bin/env python3
import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 7007       # The port used by the server
message = b'Hello there'

#load public key for encryption:
with open("certificate.pem", "rb") as cert_file:
    pem_data = cert_file.read()
    cert = x509.load_pem_x509_certificate(pem_data, default_backend())

public_key = cert.public_key()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #encryption of message
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
    s.sendall(encrypted_message)
    data = s.recv(1024)

print('Received', repr(data))