# Nimbus Fintech Solutions — Information Security Policy

> Nimbus Fintech Solutions is a fictional company invented for this assignment, used to work through how an Information Security Policy is built and justified under ISO 27001:2022 in a realistic setting. (Scenario generated for this exercise — see [ISMS Scenario](./ISMS-Scenario.md) for full background.)

## Document Control

| Attribute | Details |
|---|---|
| Policy Title | Information Security Policy |
| Reference Number | POL-001 |
| Version | 1.0 |
| Owner | CTO and Information Security Manager |
| Approved By | Chief Technology Officer |
| Effective Date | 17 July 2026 |
| Next Review Date | 17 January 2027 |

### Version History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 17 July 2026 | Information Security Manager | Initial release |

---

## Definitions

- **ISMS:** Information Security Management System — the overall framework of policies, processes, and controls Nimbus uses to manage information security risk.
- **CIA:** Confidentiality, Integrity, and Availability — the three properties of information this policy is designed to protect.
- **BYOD:** Bring Your Own Device — a personally owned laptop, phone, or tablet used to access Nimbus systems or data.
- **Annex A control:** One of the 93 security controls listed in Annex A of ISO 27001:2022, used as a reference point for the rules in this policy.
- **SoA:** Statement of Applicability — the document that records which Annex A controls apply to Nimbus and why.

---

## 1. Purpose

Nimbus Fintech Solutions provides payroll and tax filing software to roughly 3,000 small and mid-sized business clients. Doing that well means handling bank account details, national identification numbers, and salary records for thousands of people who never interact with Nimbus directly — which is why information security is treated as core.

This policy sets out how Nimbus protects the confidentiality, integrity, and availability of that information. It was written for three concrete reasons:

1. A regional banking partner will not sign a vendor contract without ISO 27001:2022 certification in place.
2. A contractor's laptop containing unencrypted payroll exports was nearly lost at an airport last year.
3. Nimbus's expansion into EU markets brings GDPR obligations that this policy needs to support rather than conflict with.

None of confidentiality, integrity, or availability takes priority over the others here. A payroll platform that leaks data is a problem, but so is one that quietly corrupts a salary figure, or one that goes down the day client payroll is due.

## 2. Scope

This policy covers the whole of Nimbus — there is no carved-out team, location, or system. In practice, that means:

- **Everywhere Nimbus operates:** the Lahore headquarters, the remote engineering team spread across three countries, and the third-party helpdesk platform used for customer support.
- **Everyone who touches Nimbus systems or data:** employees, part-time staff, contractors, and any third party with system access.
- **Every system in production use:** the AWS environment, the internal HR/payroll system, the customer support platform, and any endpoint used to reach them.
- **Every device used to do that work:** whether Nimbus-issued, a contractor's own laptop, or an employee's personal phone under the current BYOD arrangement.

## 3. Policy Statement

The rules below are mandatory, not aspirational. Each one is written in response to a specific gap Nimbus has identified in how it currently operates.

- **Data storage** (Annex A 5.12, 8.12): Client and company data stays in approved, centrally managed storage. Personal cloud accounts — Dropbox, Google Drive, or similar — are not an acceptable place to keep Nimbus or client data, and access to the approved systems is logged and monitored.
- **Device encryption** (Annex A 8.24): Every device used to reach Nimbus systems or data is fully encrypted, full stop — company laptops, BYOD devices, and contractor equipment alike. This closes the exact gap that nearly caused an incident last year.
- **Access control** (Annex A 5.15, 5.18): Access is granted on a least-privilege basis tied to someone's actual role, and access rights are reviewed every quarter so that unused or excessive permissions don't quietly accumulate.
- **Backup and recovery** (Annex A 8.13): Critical systems are backed up on a regular schedule, and restoration is tested monthly — a backup nobody has tried to restore is not a control, it's an assumption.
- **Regulatory compliance:** Data handling follows GDPR for anything touching EU data subjects, applicable Pakistani data protection requirements, and PCI-DSS-adjacent practices for financial information, even though Nimbus doesn't store card data directly.
- **Acceptable use** (Annex A 5.10): Nimbus systems and data are for authorized business purposes. Anyone who notices a suspected incident or a policy violation is expected to raise it with the Information Security Manager promptly, not sit on it.

These rules were shaped by risk areas Nimbus has already noticed informally: unmanaged BYOD devices, contractors reaching for whatever storage is convenient, no set schedule for reviewing who has access to what, and backups that exist but have never actually been tested.

## 4. Roles and Responsibilities

Security works better with named accountability than with everyone being vaguely responsible, so:

- **CEO and CTO:** Jointly accountable for the ISMS as a whole — its resourcing, its direction, and whether it actually reflects how the business operates.
- **Information Security Manager:** Owns the day-to-day of this policy — implementing controls, watching for compliance gaps, coordinating audits, and running incident response when something goes wrong. This is currently a part-time role shared with the DevOps lead; Nimbus has committed to making it full-time within 12 months as the ISMS matures.
- **Engineering leads, HR, and other functional leads:** Responsible for putting the technical and procedural pieces of this policy into practice within their own area, and for cooperating with the Information Security Manager.
- **Everyone else — staff, contractors, third parties:** Expected to follow the acceptable use and data handling rules in this policy, and to say something the moment they notice a problem rather than waiting to be asked.

## 5. Compliance and Enforcement

Nimbus checks that this policy is actually being followed not just on paper but through quarterly internal audits combined with ongoing automated monitoring of systems and access.

When something is found, the response is proportionate to the risk. A first-time or low-risk issue typically results in the relevant access being revoked while it's sorted out. Repeated or serious violations escalate further — formal disciplinary action for employees, or contract termination for contractors and third parties — at the discretion of the CTO and Information Security Manager.

## 6. Review and Improvement

This policy is reviewed every six months as a matter of course, in line with the continual improvement expectation in ISO 27001:2022 Clause 10. Six months rather than the more common annual cycle reflects the fact that Nimbus's ISMS is still new and likely to need adjustment as gaps get found.

Outside of that schedule, the policy is also revisited immediately after any major security incident, and ahead of any certification or surveillance audit, so it never goes into an audit stale.

## 7. Exceptions

Occasionally a system or team may have a legitimate reason it cannot meet a specific rule in this policy right away — a legacy integration that cannot yet support encryption, for example. Exceptions are handled by written request to the Information Security Manager, who reviews the risk and grants a time-limited exception only with CTO sign-off.

Undocumented workarounds are not exceptions; they are policy violations.

## 8. Related Documents

This policy sits at the top of Nimbus's ISMS documentation and is intended to be supported by the documents below as the ISMS matures:

- **Statement of Applicability** — maps Annex A controls to Nimbus's environment.
- **Risk Assessment and Risk Treatment Plan** — the formal version of the risk areas referenced in Section 3.
- **Access Control Policy, Acceptable Use Policy, Backup Policy, and Incident Response Policy** — topic-specific policies expanding on the rules in Section 3.

## Approval

This policy is approved for release by:

| Name / Role | Signature | Date |
|---|---|---|
| Chief Technology Officer | | |
| Chief Executive Officer | | |

---

*Reference: [Nimbus ISMS Scenario](./ISMS-Scenario.md)*
