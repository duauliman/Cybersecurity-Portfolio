# Nimbus Fintech Solutions — ISMS Scenario

*Reference Document*

This document records the fictional company scenario used as a working example for developing Nimbus Fintech Solutions' ISO 27001:2022 Information Security Management System (ISMS) documentation, including the Information Security Policy. It's a shared reference so that all future policies, the Statement of Applicability, and risk assessments stay consistent with the same organizational context and decisions.

> Nimbus Fintech Solutions is a fictional company invented for this exercise, used to work through how an Information Security Policy is built and justified under ISO 27001:2022 in a realistic setting.

---

## 1. Company Overview

Nimbus Fintech Solutions provides payroll and tax filing software to roughly 3,000 small and mid-sized business clients, handling bank account details, national identification numbers, and salary records for thousands of end users who never interact with Nimbus directly.

## 2. Why Nimbus Needs ISO 27001:2022

- A prospective regional banking client requires ISO 27001 certification before signing any vendor contract — this is the primary driver.
- A near-miss incident: a contractor's laptop containing unencrypted client payroll exports was almost lost at an airport.
- Expansion into the EU market requires demonstrable compliance with data protection obligations (GDPR ties in closely with ISO 27001 controls).
- Series B investors flagged the absence of a formal security program as a due-diligence risk.

## 3. Organizational Details

### 3.1 Locations
- Headquarters in Lahore, Pakistan
- A remote engineering team distributed across 3 countries
- A customer support team using a third-party outsourced helpdesk platform

### 3.2 Systems in Scope
- Production AWS environment
- Internal HR/payroll system
- Customer support platform (third-party)
- Employee laptops (BYOD currently informal / unmanaged)
- Contractor-owned devices

### 3.3 Key Roles
- CEO and CTO — joint accountability for the ISMS
- Information Security Manager — currently a part-time role, shared with the DevOps lead
- Engineering leads, HR, and other functional leads

### 3.4 Known Risk Areas (Informally Identified)
- Unmanaged BYOD devices without mandatory encryption
- Contractors using personal/unapproved cloud storage for client data
- No formal, scheduled access review process
- Backups exist but are untested

> **Note:** these risks were identified informally, not through a completed formal risk assessment. A formal risk assessment is a recommended next step so that the Statement of Applicability and future policies are properly evidence-based.

### 3.5 Regulatory Drivers
- Pakistan's applicable data protection framework
- General Data Protection Regulation (GDPR) — due to EU client expansion
- PCI-DSS-adjacent handling requirements — Nimbus does not store card data directly but handles financial data

---

*Related document: [Information Security Policy (POL-001)](./Information-Security-Policy.md)*
