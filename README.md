# Web Security Labs

📚 Hands-on write-ups from working through **[PortSwigger Web Security
Academy](https://portswigger.net/web-security)** labs — documenting real
vulnerabilities, the exact payloads used to exploit them, and what each
one teaches about secure coding.

![Status](https://img.shields.io/badge/status-in--progress-brightgreen)
![Labs Solved](https://img.shields.io/badge/labs%20solved-6-blue)
![Focus](https://img.shields.io/badge/focus-SQL%20Injection-orange)

---

## About Me

<!-- TODO: replace with your own intro -->
I'm learning application security hands-on through PortSwigger's Web
Security Academy, documenting each lab as I go. This repo is my working
log — part study notes, part portfolio — showing how I approach finding,
understanding, and exploiting real vulnerability classes.

- 🔗 **LinkedIn:** [add your link]
- 🔗 **Portfolio/site:** [add your link]
- 📫 **Contact:** [add your email]

---

## Why this repo exists

Most "I did some labs" claims aren't verifiable. This repo shows the
actual work: the vulnerable request, the reasoning behind each payload,
the raw output, and the lesson learned — so anyone reviewing it (a
recruiter, a mentor, future me) can see the thought process, not just a
"Solved ✅" badge.

Each write-up follows the same format:
**Vulnerability → Payload → Result → Key Takeaway**

---

## SQL Injection

| # | Lab | Technique | Status |
|---|---|---|---|
| 1 | [SQLi in WHERE clause — retrieving hidden data](sql-injection/01-login-bypass-hidden-data/notes.md) | Boolean tautology (`' OR 1=1--`) | ✅ Solved |
| 2 | [SQLi login bypass](sql-injection/02-login-bypass-auth/notes.md) | Comment-based auth bypass (`admin'--`) | ✅ Solved |
| 3 | [UNION attack — column count](sql-injection/03-union-column-count/notes.md) | `UNION SELECT NULL...` probing | ✅ Solved |
| 4 | [DB fingerprinting — Oracle](sql-injection/04-db-fingerprint-oracle/notes.md) | `v$version` system view | ✅ Solved |
| 5 | [DB fingerprinting — MySQL & MSSQL](sql-injection/05-db-fingerprint-mysql-mssql/notes.md) | `@@version` global variable | ✅ Solved |
| 6 | [Listing database contents](sql-injection/06-list-db-contents/notes.md) | `information_schema` enumeration + credential extraction | ✅ Solved |

**Skills demonstrated in this section:**
`UNION-based injection` · `authentication bypass` · `DB fingerprinting` · `schema enumeration` · `data exfiltration`

---

## Repo structure

```
web-security-labs/
├── README.md
└── sql-injection/
    ├── 01-login-bypass-hidden-data/
    │   ├── notes.md
    │   └── solved.png
    ├── 02-login-bypass-auth/
    │   ├── notes.md
    │   ├── analysis.png
    │   └── solved.png
    ├── 03-union-column-count/
    │   ├── notes.md
    │   ├── step1.png
    │   ├── step2.png
    │   └── solved.png
    ├── 04-db-fingerprint-oracle/
    │   ├── notes.md
    │   └── solved.png
    ├── 05-db-fingerprint-mysql-mssql/
    │   ├── notes.md
    │   └── solved.png
    └── 06-list-db-contents/
        ├── notes.md
        ├── step1-columns.png
        ├── step2-extract.png
        └── solved.png
```

---

## Roadmap

- [x] SQL Injection — UNION attacks, auth bypass, DB fingerprinting, data extraction
- [ ] SQL Injection — Blind (boolean-based & time-based)
- [ ] SQL Injection — Error-based & second-order
- [ ] Cross-Site Scripting (XSS) — reflected, stored, DOM-based
- [ ] Authentication vulnerabilities
- [ ] Server-Side Request Forgery (SSRF)
- [ ] Access control vulnerabilities
- [ ] CSRF

---

## ⚠️ Ethics & Scope

All testing here was performed exclusively on **PortSwigger's official,
sandboxed, disposable lab environments**, built specifically for this
kind of practice. Lab URLs are unique and temporary per session, and any
"leaked" data (usernames, passwords, etc.) shown in these notes belongs
to those throwaway instances — not real systems or real people.

**None of the techniques documented here were used against systems I
don't own or have explicit authorization to test.** Unauthorized access
to computer systems is illegal — always practice on legal platforms
like PortSwigger, TryHackMe, HackTheBox, or your own lab setup.
