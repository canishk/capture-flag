# CipherForge Requirements

Version: 1.0
Status: Living Document

---

# Purpose

This document defines the functional and non-functional requirements for CipherForge.

It serves as the primary reference for product planning, architecture, implementation, testing, and future enhancements.

Every feature implemented within the platform should be traceable to one or more requirements defined here.

---

# Functional Requirements

## FR-001 User Registration

The platform shall allow new users to create an account.

Requirements:

- Email registration
- Password validation
- Email verification (future)
- Duplicate email prevention

---

## FR-002 Authentication

The platform shall authenticate registered users.

Requirements:

- Login
- Logout
- Password hashing
- Secure session management

---

## FR-003 User Profile

Users shall have a personal profile.

The profile includes:

- Name
- Username
- Email
- Avatar (future)
- Biography (future)
- Joined date
- Current level
- Trophy summary

---

## FR-004 Roles

Version 1 supports only two roles.

Administrator

- Manage platform

Learner

- Participate in challenges

No additional role hierarchy exists.

---

## FR-005 Categories

Administrators can create learning categories.

Examples:

- Web Security
- Cryptography
- Networking
- Reverse Engineering
- Digital Forensics
- Malware Analysis
- Cloud Security
- Secure Coding

Categories may contain multiple levels.

---

## FR-006 Levels

Each category contains one or more learning levels.

Examples:

Beginner

Intermediate

Advanced

Expert

Administrators define progression rules.

---

## FR-007 Challenge Management

Administrators can create challenges.

Challenge properties include:

- Title
- Description
- Difficulty
- Points
- Categories
- Level
- Visibility
- Status
- Tags
- Resources
- Hints

---

## FR-008 Challenge Types

Version 1 supports:

- Text Answer
- AI Conversation
- External Web Challenge

Future challenge types may include:

- Docker Labs
- Virtual Machines
- File Upload
- Multiple Choice

---

## FR-009 Answer Evaluation

Text challenges shall support configurable evaluation.

Evaluation methods may include:

- Exact Match
- Case-insensitive Match
- Regular Expression
- Cosine Similarity

Evaluation strategy is selected per challenge.

---

## FR-010 AI Challenges

AI challenges simulate realistic cybersecurity scenarios.

Examples:

- SOC Analyst
- Incident Responder
- Help Desk
- Penetration Tester
- Security Consultant

AI acts as a participant within the challenge.

---

## FR-011 Hints

Administrators may attach multiple hints to a challenge.

Each hint includes:

- Display order
- Penalty (optional)
- Visibility conditions

---

## FR-012 Progress Tracking

The platform shall track user progress.

Examples:

- Completed challenges
- Category progress
- Level progress
- Completion percentage
- Earned points

---

## FR-013 Unlock Rules

Users unlock content according to administrator-defined progression rules.

Possible rules include:

- Complete all challenges
- Reach minimum score
- Complete required challenges

---

## FR-014 Trophy System

Users earn trophies for achievements.

Examples:

- Category completion
- First challenge
- Speed completion
- Hidden achievements
- AI achievements

---

## FR-015 Leaderboard

The platform shall display rankings.

Examples:

- Overall points
- Category points
- Monthly rankings (future)

---

## FR-016 Resources

Challenges may include learning resources.

Examples:

- Articles
- Documentation
- Videos
- External websites

---

## FR-017 Search

Users can search:

- Categories
- Challenges
- Tags

---

## FR-018 Administrator Portal

Administrators can manage:

- Users
- Categories
- Levels
- Challenges
- Hints
- Trophies
- Tags

---

## FR-019 Notifications (Future)

Future support includes:

- Achievement unlocked
- New challenges
- Announcements

---

## FR-020 Analytics

The platform shall record learning analytics.

Examples:

- Challenge completion
- Average solve time
- Hint usage
- Failed attempts

---

# Non-Functional Requirements

## NFR-001 Performance

API response time should generally remain below 300 ms under normal load.

---

## NFR-002 Scalability

Architecture should support future modularization.

---

## NFR-003 Availability

The platform should remain available during normal operation except scheduled maintenance.

---

## NFR-004 Security

The application shall:

- Validate all inputs
- Hash passwords
- Protect sensitive information
- Use HTTPS in production
- Prevent common web vulnerabilities

---

## NFR-005 Maintainability

Code shall be:

- Modular
- Documented
- Tested
- Readable

---

## NFR-006 Accessibility

The interface should follow modern accessibility practices where practical.

---

## NFR-007 Mobile Experience

Version 1 is mobile-first.

Desktop support is equally important.

---

## NFR-008 Observability

The application shall provide:

- Logging
- Error tracking
- Health endpoints

---

## NFR-009 Configuration

Configuration shall be environment-based.

No secrets shall exist in source code.

---

## NFR-010 Testability

Business logic should be independently testable.

---

# Constraints

Version 1 intentionally excludes:

- Multi-tenancy
- Organization management
- Challenge versioning
- Docker-hosted labs
- VM provisioning
- Payment processing

---

# Assumptions

- Internet connectivity exists.
- Users have modern browsers.
- AI services may be unavailable temporarily.
- External challenge URLs are maintained by administrators.

---

# Success Criteria

The platform is successful if users can:

- Register
- Learn progressively
- Complete challenges
- Track progress
- Earn trophies
- Stay engaged
- Improve cybersecurity skills

---

# Requirement Traceability

Every architecture document, database design, API endpoint, user story, sprint, and test case should reference one or more requirement IDs from this document.

This document is the canonical source of product requirements.