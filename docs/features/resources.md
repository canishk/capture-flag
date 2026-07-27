# Resource Feature Specification

Version: 1.0

Status: Living Document

Module: Resources

Related Documents

- docs/features/challenges.md
- docs/features/hints.md
- docs/features/progress.md
- docs/architecture/EventModel.md
- docs/architecture/API.md

---

# Purpose

The Resources module manages educational content that supports learner understanding before, during, or after completing a challenge.

Resources supplement learning without replacing the challenge itself.

Resources are reusable across multiple challenges.

---

# Scope

## Included

- Resource management
- Resource categorization
- Resource reuse
- Resource visibility
- Resource analytics
- External and internal resources

## Excluded

- Challenge descriptions
- Hint management
- Attachments required for challenge execution
- Evaluation logic

---

# Design Principles

Resources follow these principles:

- Learning first
- Reusable
- Vendor neutral
- Version aware
- Analytics driven

Resources should explain concepts rather than reveal challenge solutions.

---

# Actors

## Learner

Can:

- View published resources
- Open resource links
- Download supported files
- Bookmark resources (Future)

Cannot:

- Modify resources

---

## Administrator

Can:

- Create resources
- Edit resources
- Publish resources
- Archive resources
- Associate resources with challenges

---

# User Stories

## RES-001

As a learner,

I want access to high-quality reference material,

So that I can understand the concepts behind a challenge.

---

## RES-002

As a learner,

I want resources that remain useful after completing a challenge,

So that I can continue learning.

---

## RES-003

As an administrator,

I want reusable resources,

So that I don't duplicate educational content.

---

## RES-004

As an administrator,

I want analytics about resource usage,

So that I know which materials are valuable.

---

# Resource Types

Version 1 supports:

## Article

Example:

- OWASP Cheat Sheet
- Blog article
- Official documentation

---

## Documentation

Examples:

- RFCs
- Linux man pages
- Python documentation

---

## Video

Examples:

- Conference talks
- Recorded tutorials

---

## PDF

Examples:

- Whitepapers
- Guides
- Research papers

---

## Download

Examples:

- Sample PCAP
- Log file
- Source code
- Wordlists

---

## External Tool

Examples:

- CyberChef
- VirusTotal
- Shodan
- Nmap documentation

---

Future resource types:

- Interactive labs
- Slides
- Podcasts
- Books
- Courses

---

# Resource Structure

Each resource contains:

- Title
- Summary
- Description
- Resource Type
- URL or File
- Author
- Source
- Status
- Tags

Optional:

- Estimated reading time
- Difficulty
- Language
- Publication date
- Version

---

# Resource Status

Supported states:

```
Draft

Published

Hidden

Archived
```

Only published resources are visible to learners.

---

# Resource Relationships

A resource may belong to:

- Zero or more challenges
- Zero or more categories
- Zero or more learning paths (Future)

Example:

```
OWASP SQL Injection Cheat Sheet

↓

Challenge A

Challenge B

Challenge C
```

Resources are reusable.

---

# Learning Philosophy

Resources should:

- Explain concepts
- Encourage further study
- Build long-term understanding
- Complement practical exercises

Resources should not:

- Reveal answers
- Contain walkthroughs
- Provide challenge flags

---

# Resource Metadata

Recommended metadata:

- Difficulty
- Estimated study time
- Cybersecurity domain
- Technology
- Vendor
- Language

This metadata enables future recommendation engines.

---

# Search

Learners should be able to search resources by:

- Title
- Tags
- Category
- Type
- Technology
- Difficulty

Future:

- Semantic search
- AI recommendations

---

# Analytics

Track:

- Views
- Downloads
- Click-through rate
- Average reading time (where available)
- Challenge completion after viewing
- Most referenced resources

Analytics belongs to the Analytics module.

---

# Validation Rules

Title

- Required
- Maximum length

Type

- Required

URL

- Valid HTTPS URL when applicable

Downloads

- Supported file types only

Status

- Valid lifecycle state

---

# Failure Scenarios

Examples:

- Broken external link
- Missing download
- Unsupported file type
- Hidden resource requested
- Duplicate resource reference

Broken links should be detectable through administrative health checks.

---

# Edge Cases

- Resource referenced by many challenges
- Resource removed after publication
- External website unavailable
- Multiple language versions
- Resource updated while learners are studying

Challenge behavior should remain stable even if a resource becomes unavailable.

---

# Security

Resources should never:

- Execute arbitrary code
- Download unsafe content
- Redirect to untrusted websites

External links should:

- Open safely
- Be validated
- Use HTTPS where possible

Downloaded files should be malware-scanned before publication.

---

# Events

The Resources module publishes:

```
ResourceViewed

ResourceDownloaded

ResourceUpdated
```

Subscribers may include:

- Analytics
- Recommendation Engine (Future)

---

# Audit

Record:

- Resource created
- Resource updated
- Resource published
- Resource archived

Learner activity is tracked separately.

---

# API Resources

Base resource:

```
/api/v1/resources
```

Typical operations:

```
GET /

GET /{resourceId}

POST /

PATCH /{resourceId}

DELETE /{resourceId}

GET /challenge/{challengeId}

GET /search
```

Administrative operations:

```
POST /validate-link

POST /check-health
```

The OpenAPI specification is the authoritative API contract.

---

# Data Ownership

Resources owns:

- Metadata
- Educational content
- External references
- Tags
- Publication status

Challenges own only the association to resources.

---

# Dependencies

Resources depends only on shared infrastructure.

It should not depend directly on:

- Progress
- Evaluations
- Leaderboard
- Trophies

Other modules reference resources through identifiers.

---

# Relationships

```
Challenge

* ───────────── * Resource
```

Many challenges may reference the same resource.

---

# Non-Functional Requirements

- Resource retrieval should be cacheable.
- Search should support pagination.
- External link validation should run periodically.
- Downloads should support large files.
- Resource metadata should be indexed for efficient search.

---

# Future Enhancements

Potential additions:

- AI resource recommendations
- Personalized reading lists
- Resource ratings
- Community recommendations
- Offline downloads
- Learning playlists
- Resource collections
- Multi-language support
- Citation management

These enhancements should build upon the reusable resource model.

---

# Acceptance Criteria

Resource Management

- Administrators can create, edit, publish, hide, and archive resources.
- Resources can be reused by multiple challenges.

Learner Experience

- Learners can access published resources.
- Resources are searchable.
- Broken resources are not presented to learners.

Analytics

- Views and downloads generate events.
- Resource usage can be analyzed independently of challenges.

---

# Guiding Principle

A Resource answers the question:

**"Where can the learner deepen their understanding of this topic?"**

Resources should promote lasting knowledge, remain reusable across the platform, and provide high-quality references that extend learning beyond individual challenges.