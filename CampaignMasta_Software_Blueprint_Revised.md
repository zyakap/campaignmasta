# CampaignMasta Software Blueprint

**Product Name:** CampaignMasta  
**Product Type:** SaaS Political CRM, Campaign Operations, Voter Coordination, Relationship Management, Messaging, and Constituency Engagement Platform  
**Target Market:** Papua New Guinea political candidates contesting District Open Seats and Provincial Seats, with future expansion to the Pacific region.  
**Primary Election Context:** PNG General Elections 2027 and future election cycles.

---

## 1. Executive Summary

CampaignMasta is a powerful SaaS platform designed to help political candidates coordinate campaign teams, manage potential supporters, track ward-level intelligence, monitor relationships with coordinators and influential people, dispatch targeted messages, plan campaign visits, manage polling-day operations, and continue constituency engagement after elections.

The platform is designed as a multi-tenant SaaS system where each candidate subscribes to CampaignMasta. Each candidate has their own isolated campaign workspace, team members, voter/supporter records, ward intelligence, messages, reports, and campaign operations.

CampaignMasta is not only a voter database. It is a complete political operating system for candidates, campaign managers, IT administrators, district coordinators, LLG coordinators, ward coordinators, village captains, influencers, volunteers, and polling-day teams.

---

## 2. Core Product Positioning

CampaignMasta should be positioned as:

> **The Complete Political CRM, Campaign Management, Voter Coordination, Relationship Monitoring, Messaging, and Constituency Engagement Platform for Papua New Guinea and the Pacific.**

Main value propositions:

1. Helps candidates understand every ward, LLG, district, and province.
2. Helps campaign teams register supporters and potential voters.
3. Helps politicians maintain regular contact with key coordinators and influential people.
4. Helps candidates prepare ward-specific speeches and talking points.
5. Helps campaign managers track activity, reports, events, and follow-ups.
6. Helps campaign teams dispatch structured messages to specific groups.
7. Helps polling-day teams monitor booths, scrutineers, incidents, and turnout.
8. Helps elected leaders continue using the system after elections for constituency management.

---

## 3. SaaS Multi-Tenant Architecture

CampaignMasta will operate as one central platform serving many candidates.

Each candidate is treated as a separate tenant.

```text
CampaignMasta SaaS Platform
│
├── Candidate A Tenant
│   ├── Candidate Profile
│   ├── Campaign Manager
│   ├── IT Administrator
│   ├── Coordinators
│   ├── Supporters
│   ├── Ward Intelligence
│   ├── Messages
│   ├── Reports
│   └── Polling Operations
│
├── Candidate B Tenant
│   ├── Candidate Profile
│   ├── Campaign Team
│   └── Campaign Data
│
└── Candidate C Tenant
    ├── Candidate Profile
    ├── Campaign Team
    └── Campaign Data
```

### 3.1 Tenant Data Isolation

Each candidate's data must be isolated from other candidates.

Every major record should include:

```text
candidate_id
created_by
updated_by
created_at
updated_at
```

This includes:

- Team members
- Supporters
- Potential voters
- Ward records
- Influencers
- Call logs
- Messages
- Events
- Reports
- Tasks
- Polling data

No candidate or campaign user should access another candidate's data unless they are a system-level CampaignMasta administrator.

---

## 4. Candidate Types and Dynamic Campaign Hierarchy

This is a foundational architectural requirement.

CampaignMasta must support only two candidate categories:

1. **District Open Candidate**
2. **Provincial Candidate**

The candidate type determines the campaign hierarchy, available coordinator levels, access permissions, reporting structure, messaging groups, dashboards, and analytics.

---

### 4.1 District Open Candidate

A District Open Candidate contests one district/open electorate.

Examples:

- Moresby North-West Open
- Kandep Open
- Wau-Waria Open
- Kainantu Open
- Gazelle Open

A District Open Candidate does **not** need District Coordinators because the candidate's campaign area is already one district.

#### District Open Candidate Hierarchy

```text
Candidate
│
├── Campaign Manager
│
├── IT Administrator
│
├── LLG Managers / LLG Coordinators
│   │
│   ├── Ward Coordinators
│   │   │
│   │   ├── Village Coordinators
│   │   │   │
│   │   │   └── Supporters / Potential Voters
│   │   │
│   │   └── Ward Influencers
│   │
│   └── Volunteers
│
└── Campaign Support Team
```

#### District Open Seat System Rules

When `candidate_type = DISTRICT_OPEN`:

- Candidate must select one Province.
- Candidate must select one District/Open Electorate.
- System loads LLGs under that district.
- System loads wards under those LLGs.
- District Coordinator role is hidden or disabled.
- Reports roll up from Ward to LLG to Candidate Dashboard.
- Messaging targets start from LLG level downward.
- Call monitoring starts from Candidate/Campaign Manager to LLG Coordinators.

---

### 4.2 Provincial Candidate

A Provincial Candidate contests a provincial seat.

Examples:

- Eastern Highlands Governor
- Morobe Governor
- Central Governor
- NCD Governor
- East New Britain Governor

A Provincial Candidate requires District Coordinators because a province contains multiple districts.

#### Provincial Candidate Hierarchy

```text
Candidate
│
├── Campaign Manager
│
├── IT Administrator
│
├── District Coordinators
│   │
│   ├── LLG Managers / LLG Coordinators
│   │   │
│   │   ├── Ward Coordinators
│   │   │   │
│   │   │   ├── Village Coordinators
│   │   │   │   │
│   │   │   │   └── Supporters / Potential Voters
│   │   │   │
│   │   │   └── Ward Influencers
│   │   │
│   │   └── Volunteers
│   │
│   └── District-Level Influencers
│
└── Campaign Support Team
```

#### Provincial Seat System Rules

When `candidate_type = PROVINCIAL`:

- Candidate must select one Province.
- Candidate does not select one district as the campaign boundary.
- System loads all districts under the province.
- System loads all LLGs, wards, and villages under the selected province.
- District Coordinator role is enabled.
- Reports roll up from Ward to LLG to District to Candidate Dashboard.
- Messaging targets include Province, District, LLG, Ward, and team category.
- Call monitoring includes Candidate/Campaign Manager to District Coordinators.

---

## 5. PNG Administrative Geography Module

CampaignMasta should maintain a national administrative geography database.

```text
Province
    District / Open Electorate
        LLG
            Ward
                Village / Community / Settlement
```

### 5.1 Geography Features

- Province management
- District/Open electorate management
- LLG management
- Ward management
- Village/community/settlement management
- Landmark registration
- Church/school/market/health facility registration
- Polling location mapping
- GIS/map integration in future version

### 5.2 Candidate Geography Assignment

For District Open Candidate:

```text
Candidate Type: District Open
Province: Selected
District: Selected
LLGs: Auto-loaded from district
Wards: Auto-loaded from LLGs
```

For Provincial Candidate:

```text
Candidate Type: Provincial
Province: Selected
Districts: Auto-loaded from province
LLGs: Auto-loaded from districts
Wards: Auto-loaded from LLGs
```

---

## 6. User Roles and Permissions

CampaignMasta must implement role-based access control.

### 6.1 Platform-Level Roles

#### System Super Administrator

Owned by CampaignMasta SaaS provider.

Can:

- Create candidate tenants
- Manage subscriptions
- Manage platform settings
- Manage national geography data
- View high-level platform usage
- Suspend accounts
- Reset candidate tenant access
- Manage billing plans

#### Platform Support Officer

Can:

- Assist candidate tenants
- View support tickets
- Reset passwords
- Help configure candidate profiles
- Cannot view sensitive political data unless granted temporary support access

---

### 6.2 Candidate Tenant-Level Roles

#### Candidate

Can:

- View all campaign data within own tenant
- View dashboards
- View call reminders
- Send messages
- Assign senior roles
- Review reports
- View key influencers
- View campaign performance
- Approve major events and plans

#### Campaign Manager

Can:

- Manage the campaign team
- View all reports
- Assign tasks
- Manage events
- Send campaign messages
- Monitor coordinators
- Manage call follow-ups
- View ward intelligence
- Manage polling operations

#### IT Administrator

Candidate's technical team leader.

Can:

- Add users
- Assign roles
- Reset passwords
- Configure campaign settings
- Manage team access
- Import data
- Export approved reports
- Configure messaging settings
- Manage candidate profile data
- Configure geography assignment

#### District Coordinator

Only applies to Provincial Candidates.

Can:

- Manage assigned district
- Manage LLG coordinators in assigned district
- View ward data within assigned district
- Submit district reports
- Receive candidate/campaign manager messages
- Monitor LLG coordinator activity
- Record district-level influencers
- Escalate issues to campaign manager

#### LLG Manager / LLG Coordinator

Applies to both District Open and Provincial Candidates.

Can:

- Manage assigned LLG
- View ward coordinators under assigned LLG
- Record LLG-level issues
- Submit LLG reports
- Monitor ward coordinator activity
- Track supporters within assigned LLG
- Create local campaign tasks

#### Ward Coordinator

Can:

- Manage assigned ward
- Register supporters and potential voters
- Record community issues
- Record landmarks and influential people
- Submit ward reports
- Upload meeting notes and photos
- Receive messages
- Track ward-level tasks

#### Village Coordinator

Can:

- Register village-level supporters
- Record village issues
- Report local attendance
- Record follow-up notes
- Assist ward coordinator

#### Volunteer

Can:

- Assist with events
- Receive task assignments
- Submit basic activity reports
- Receive messages

#### Polling-Day Scrutineer

Can:

- View assigned polling location
- Submit polling status
- Report incidents
- Submit turnout updates where legally permitted
- Communicate with polling operations centre

---

## 7. Candidate Profile Module

The candidate profile is the starting point for each tenant.

### 7.1 Candidate Profile Fields

```text
Candidate Name
Candidate Photo
Political Party
Candidate Type: District Open / Provincial
Province
District/Open Electorate: Required only for District Open Candidate
Campaign Slogan
Candidate Biography
Contact Number
Email Address
Campaign Office Address
Subscription Plan
Campaign Start Date
Campaign Status: Active / Suspended / Archived
```

### 7.2 Candidate Type Logic

If candidate selects **District Open**:

```text
Show:
- Province
- District/Open Electorate
- LLG structure
- Ward structure

Hide:
- District Coordinator level
- Province-wide district reports
```

If candidate selects **Provincial**:

```text
Show:
- Province
- District structure
- District Coordinator level
- Province-wide reports
- District performance dashboards

Hide:
- Single district boundary restriction
```

---

## 8. Team Management Module

This module allows Candidate, Campaign Manager, and IT Administrator to manage the campaign team.

### 8.1 Team Member Fields

```text
Full Name
Gender
Phone Number
Email
Role
Candidate Tenant
Province
District: Optional depending on candidate type and role
LLG
Ward
Village
Influence Level
Account Status
Last Login
Profile Photo
Notes
```

### 8.2 Team Assignment Rules

District Open Candidate:

- Campaign Manager has whole district access.
- IT Administrator has whole tenant access.
- LLG Coordinators are assigned to LLGs.
- Ward Coordinators are assigned to wards.
- Village Coordinators are assigned to villages.
- District Coordinator role is not available.

Provincial Candidate:

- Campaign Manager has whole province access.
- IT Administrator has whole tenant access.
- District Coordinators are assigned to districts.
- LLG Coordinators are assigned under districts.
- Ward Coordinators are assigned under LLGs.
- Village Coordinators are assigned under wards.

---

## 9. Ward Intelligence Module

This module helps candidates understand each ward before visiting.

### 9.1 Ward Profile Fields

```text
Ward Name
Ward Number
LLG
District
Province
Councillor Name
Key Clans
Key Churches
Schools
Markets
Health Facilities
Important Landmarks
Main Roads / Access Routes
Common Meeting Places
Population Estimate
Estimated Voting Population
Previous Election Notes
Support Strength: Strong / Medium / Weak / Unknown
Main Community Issues
Security Concerns
Youth Groups
Women's Groups
Church Groups
Business Groups
Important Families
Notes for Candidate
```

### 9.2 Ward Visit Brief

Before a candidate visits a ward, the system should produce a ward brief:

- Ward summary
- Local landmarks
- Local leaders to acknowledge
- Key issues raised by residents
- Previous promises made
- Names of key coordinators
- Event history
- Supporter count
- Undecided supporter count
- Risks and sensitivities
- Suggested talking points

---

## 10. Supporter and Potential Voter Registry

This module records supporters, potential supporters, and community contacts.

Important: CampaignMasta should be designed around supporter/contact coordination, not official ballot choices or intimidation.

### 10.1 Supporter Fields

```text
Full Name
Gender
Age Range
Phone Number
Province
District
LLG
Ward
Village
Clan / Family Group
Church / Community Group
Occupation
Support Status: Strong Supporter / Leaning Supporter / Undecided / Not Supportive / Unknown
Influence Level: High / Medium / Low
Registered By
Introduced By
Main Issue of Interest
Follow-Up Required: Yes / No
Follow-Up Date
Consent to Receive Messages: Yes / No
Notes
```

### 10.2 Supporter Rules

- Avoid recording official vote choices.
- Avoid coercive data fields.
- Require consent for messaging.
- Allow duplicate detection by name, phone, ward, and village.
- Limit access based on user role and geography assignment.
- Allow import from CSV with validation.

---

## 11. Influencer and Key Person CRM Module

This is one of the most important modules for CampaignMasta.

The app must help politicians maintain regular relationships with:

- Ward Coordinators
- LLG Coordinators
- District Coordinators
- Councillors
- Church leaders
- Clan leaders
- Women's leaders
- Youth leaders
- Teachers
- Business owners
- Former candidates
- Community elders
- Sports leaders
- NGO/community group leaders
- Public servants where appropriate

### 11.1 Influencer Fields

```text
Full Name
Photo
Phone Number
Alternative Phone
Email
Province
District
LLG
Ward
Village
Position / Community Role
Influence Category
Influence Level: High / Medium / Low
Estimated Network Size
Political Relationship Status: Strong / Medium / Weak / Unknown
Preferred Contact Method: Call / SMS / WhatsApp / Visit
Contact Frequency Rule: 7 Days / 14 Days / 30 Days / Custom
Last Call Date
Last Meeting Date
Last Message Date
Next Contact Due Date
Assigned Relationship Owner
Notes
```

### 11.2 Influence Scoring

The system may compute an influence score from:

- Position in community
- Estimated network size
- Event attendance
- Number of supporters referred
- Ward importance
- Relationship strength
- Responsiveness to calls/messages

Example scoring:

```text
Councillor: 90-100
Pastor: 70-95
Clan Leader: 70-95
Youth Leader: 50-80
Women's Leader: 50-85
Business Leader: 50-85
```

---

## 12. Call Monitoring and Relationship Reminder Module

This module tracks who was called, when they were called, who must be called next, and who is overdue.

### 12.1 Purpose

A politician must regularly call coordinators and key/influential people from each ward, LLG, district, and province. CampaignMasta must act as a relationship discipline system.

### 12.2 Call Log Fields

```text
Candidate Tenant
Caller
Person Called
Person Type: Coordinator / Influencer / Supporter / Community Leader / Other
Phone Number
Call Date
Call Time
Call Outcome: Answered / Missed / Call Back / Switched Off / Wrong Number
Discussion Summary
Issues Raised
Commitments Made
Follow-Up Required
Follow-Up Date
Next Call Due Date
Call Duration
Recorded By
```

### 12.3 Call Frequency Rules

Default recommended rules:

```text
High Influence Person: Call every 7 days
Medium Influence Person: Call every 14 days
Low Influence Person: Call every 30 days
Ward Coordinator: Call every 7 days
LLG Coordinator: Call every 7 days
District Coordinator: Call every 7 days, Provincial Candidates only
Undecided Important Contact: Follow up every 7-14 days
```

### 12.4 Call Checklist Dashboard

The system should generate a daily call checklist:

```text
Today's Required Calls
Overdue Calls
Upcoming Calls
Missed Follow-Ups
High Influence People Not Contacted Recently
Coordinators Not Contacted Recently
```

Each checklist item should allow:

- Mark as called
- Record outcome
- Add issue raised
- Add follow-up date
- Snooze reminder
- Escalate to campaign manager

### 12.5 Candidate-Type Call Monitoring

District Open Candidate:

```text
Candidate / Campaign Manager
    ↓
LLG Coordinators
    ↓
Ward Coordinators
    ↓
Village Coordinators
    ↓
Influencers / Supporters
```

Provincial Candidate:

```text
Candidate / Campaign Manager
    ↓
District Coordinators
    ↓
LLG Coordinators
    ↓
Ward Coordinators
    ↓
Village Coordinators
    ↓
Influencers / Supporters
```

### 12.6 Reminder Escalation

Example:

```text
Ward Coordinator not contacted in 7 days
→ Alert assigned LLG Coordinator

LLG Coordinator not contacted in 7 days
→ Alert Campaign Manager or District Coordinator

District Coordinator not contacted in 7 days
→ Alert Candidate and Campaign Manager

High Influence Person not contacted in 14 days
→ Alert Candidate or assigned relationship owner
```

Reminder channels:

- In-app notification
- SMS
- Email
- WhatsApp integration in future version
- Daily summary dashboard

---

## 13. Messaging Platform Module

CampaignMasta must include an internal and broadcast messaging platform.

### 13.1 Messaging Types

1. Internal direct messages
2. Team group messages
3. Broadcast announcements
4. Campaign alerts
5. Event reminders
6. Ward-specific messages
7. Polling-day emergency messages
8. Supporter SMS broadcasts where consent exists

### 13.2 Messaging Targets

District Open Candidate can send to:

```text
All Team
Campaign Manager
IT Administrator
All LLG Coordinators
Specific LLG
All Ward Coordinators
Specific Ward
Village Coordinators
Volunteers
Influencers
Supporters with consent
```

Provincial Candidate can send to:

```text
All Province Team
Campaign Manager
IT Administrator
All District Coordinators
Specific District
All LLG Coordinators
Specific LLG
All Ward Coordinators
Specific Ward
Village Coordinators
Volunteers
Influencers
Supporters with consent
```

### 13.3 Message Fields

```text
Sender
Recipient Type
Recipient Group
Specific Recipients
Subject
Message Body
Priority: Normal / Important / Urgent
Delivery Channel: In-App / SMS / Email / WhatsApp Future
Scheduled Send Date
Status: Draft / Scheduled / Sent / Failed
Read Receipt Required: Yes / No
Acknowledgement Required: Yes / No
Attachment
```

### 13.4 Read Receipts and Acknowledgement

For important instructions, the system must track:

```text
Delivered
Read
Acknowledged
Not Read
Failed
```

Campaign Manager should see users who have not read or acknowledged important messages.

---

## 14. Campaign Task Management Module

Used to assign and monitor campaign work.

### 14.1 Task Fields

```text
Task Title
Description
Assigned To
Assigned By
Candidate Tenant
Province
District
LLG
Ward
Priority
Due Date
Status: Pending / In Progress / Completed / Overdue / Cancelled
Attachments
Completion Notes
```

### 14.2 Task Examples

- Arrange venue
- Mobilize youth group
- Print posters
- Organize transport
- Confirm sound system
- Prepare food
- Register attendees
- Call influencers
- Follow up with councillor
- Confirm polling scrutineer

---

## 15. Candidate Visit and Event Management Module

This module manages rallies, ward visits, meetings, fundraisers, and campaign tours.

### 15.1 Event Fields

```text
Event Title
Event Type: Ward Visit / Rally / Meeting / Fundraiser / Awareness / Polling Training
Candidate Tenant
Province
District
LLG
Ward
Village / Venue
Landmark
Host Person
Start Date and Time
End Date and Time
Expected Crowd Size
Actual Attendance
Assigned Team
Talking Points
Issues to Address
People to Acknowledge
Security Notes
Logistics Checklist
Photos
Videos
Event Report
```

### 15.2 Event Checklist

- Venue confirmed
- Host confirmed
- Sound system
- Transport
- Security
- Food/water
- Banners/posters
- Media team
- Attendance registration
- Speech notes
- Follow-up officer assigned

---

## 16. Speech and Talking Points Assistant

The system should generate practical notes for the candidate before public appearances.

### 16.1 Input Data

- Ward profile
- Local landmarks
- Local leaders
- Current community issues
- Previous promises
- Influencer records
- Event history
- Supporter sentiment
- Candidate manifesto points

### 16.2 Output

- 1-page ward brief
- Short speech outline
- People to acknowledge
- Local references to mention
- Sensitive topics to avoid
- Follow-up commitments
- Tok Pisin version in future release

---

## 17. Community Issues and Promises Tracker

This module tracks what people ask for and what the candidate promises.

### 17.1 Issue Categories

- Roads
- Bridges
- Water supply
- School fees
- Health centre
- Youth employment
- SME support
- Church support
- Community hall
- Law and order
- Agriculture
- Sports
- Women's programs
- Market facilities
- Electricity
- Telecommunications

### 17.2 Issue Fields

```text
Issue Title
Issue Category
Description
Province
District
LLG
Ward
Village
Reported By
Reported Date
Priority
Status: New / Under Review / Follow-Up / Resolved / Deferred
Related Event
Related Influencer
Photos
Notes
```

### 17.3 Promise Fields

```text
Promise Title
Description
Made By
Made To
Province
District
LLG
Ward
Event
Promise Date
Target Date
Status: Open / In Progress / Delivered / Cancelled / Deferred
Follow-Up Owner
Notes
```

---

## 18. Reports and Analytics Module

### 18.1 Core Reports

- Supporters by province/district/LLG/ward
- Potential voters by location
- Strong supporter count
- Undecided contact count
- Influencer list by ward
- Overdue call report
- Coordinator performance report
- Ward activity report
- Event attendance report
- Issue trend report
- Message delivery report
- Polling-day readiness report

### 18.2 District Open Candidate Reports

Reports should roll up:

```text
Village
    ↓
Ward
    ↓
LLG
    ↓
Candidate Dashboard
```

### 18.3 Provincial Candidate Reports

Reports should roll up:

```text
Village
    ↓
Ward
    ↓
LLG
    ↓
District
    ↓
Candidate Dashboard
```

---

## 19. Dashboard Module

### 19.1 Candidate Command Centre

The candidate dashboard should show:

- Total supporters registered
- Potential supporters
- Undecided contacts
- Strong wards
- Weak wards
- Wards not visited
- Upcoming events
- Today's call checklist
- Overdue relationship follow-ups
- Top influencers needing contact
- New community issues
- Pending promises
- Coordinator activity
- Message acknowledgement status
- Polling readiness status

### 19.2 Campaign Manager Dashboard

Shows:

- Team activity
- Coordinator reports
- Overdue tasks
- Ward coverage
- Event preparation
- Call monitoring compliance
- Message read receipts
- Supporter registration trends
- Issue escalation

### 19.3 IT Administrator Dashboard

Shows:

- User accounts
- Active/inactive users
- Role assignments
- Data imports
- Login activity
- Messaging configuration
- System usage
- Access control issues

### 19.4 Coordinator Dashboards

Shows only assigned geography:

- Assigned area summary
- Supporter records
- Influencer records
- Tasks
- Messages
- Reports due
- Call reminders
- Events
- Issues raised

---

## 20. Polling-Day Operations Module

### 20.1 Polling Location Fields

```text
Polling Location Name
Province
District
LLG
Ward
Village
GPS Coordinates
Assigned Scrutineer
Backup Scrutineer
Contact Number
Status
Notes
```

### 20.2 Polling-Day Features

- Assign scrutineers
- Send polling instructions
- Track scrutineer attendance
- Report incidents
- Record logistical issues
- Monitor transport status
- Submit booth-level status updates
- Send emergency alerts
- Track communication with polling teams

### 20.3 Polling-Day War Room Dashboard

Shows:

- All polling locations
- Active scrutineers
- Missing scrutineers
- Reported incidents
- Urgent messages
- Transport issues
- Communication gaps

---

## 21. AI Assistant Module

CampaignMasta should include AI-assisted tools where practical.

### 21.1 AI Features

- Ward briefing generator
- Speech note generator
- Relationship reminder summary
- Daily campaign summary
- Coordinator performance insights
- Issue trend analysis
- Suggested next ward to visit
- Suggested people to call today
- Duplicate supporter detection
- Message drafting assistant
- Event report summarizer

### 21.2 AI Safety Rules

- AI should assist with organization, summaries, and reminders.
- AI should not encourage intimidation, harassment, coercion, or vote-buying.
- AI should not generate misleading political claims.
- AI-generated messages should require human review before sending.
- AI should respect role-based access and tenant boundaries.

---

## 22. Subscription and Billing Module

CampaignMasta is a SaaS product, so subscription management is required.

### 22.1 Candidate Subscription Fields

```text
Candidate Tenant
Subscription Plan
Billing Cycle: Monthly / Quarterly / Annual / Campaign Period
Start Date
End Date
Status: Trial / Active / Overdue / Suspended / Cancelled
Amount
Payment Method
Invoice Number
Receipt
```

### 22.2 Suggested Pricing Tiers

#### Basic Campaign Plan

- Candidate profile
- Team management
- Ward intelligence
- Supporter registry
- Basic reports

#### Professional Campaign Plan

- All Basic features
- Messaging platform
- Call monitoring
- Events
- Task management
- Advanced dashboards

#### Premium Campaign Plan

- All Professional features
- AI assistant
- Polling-day war room
- Advanced analytics
- Data import/export
- Priority support

#### Constituency Plan

For elected leaders after elections.

- Citizen requests
- Project tracking
- Ward development plans
- Complaints
- Public service delivery monitoring

---

## 23. Constituency Management Module

After elections, CampaignMasta should transition into a constituency management system for elected leaders.

### 23.1 Features

- Citizen request registry
- Ward development project tracking
- Community grants tracking
- Issue resolution tracking
- Public event planning
- Constituency service reports
- Development commitment tracker
- Ward visit schedule
- Community feedback
- Continued relationship CRM

This creates long-term recurring revenue after the election.

---

## 24. Security, Privacy, and Compliance Requirements

CampaignMasta handles sensitive political and personal information.

### 24.1 Security Requirements

- Secure authentication
- Strong passwords
- Optional two-factor authentication
- Role-based permissions
- Tenant-based data isolation
- Audit logs
- Login history
- Data backups
- Encrypted database fields for sensitive information
- Secure file uploads
- HTTPS only
- Rate limiting
- Session timeout
- Admin activity logs

### 24.2 Privacy Requirements

- Consent for messaging
- Clear data collection purpose
- Ability to correct personal data
- Limit exports by role
- Avoid storing official vote choices
- Avoid coercive tracking
- Avoid intimidation-related features
- Allow candidate tenant data deletion or archival after subscription ends

---

## 25. Audit Log Module

Every important action should be logged.

### 25.1 Audit Events

- Login
- Failed login
- User created
- Role changed
- Supporter created
- Supporter updated
- Influencer updated
- Message sent
- Data exported
- Report viewed
- Candidate profile changed
- Subscription changed
- Permission changed
- Bulk import
- Bulk delete

### 25.2 Audit Log Fields

```text
User
Candidate Tenant
Action
Object Type
Object ID
Old Value
New Value
IP Address
Device
Timestamp
```

---

## 26. Data Import and Export Module

### 26.1 Imports

- Supporters CSV
- Team members CSV
- Influencers CSV
- Ward data CSV
- Polling locations CSV
- Geography data by system admin

### 26.2 Exports

Exports should be permission-controlled.

- Supporter report
- Call report
- Ward report
- Event report
- Messaging report
- Polling readiness report
- Coordinator performance report

---

## 27. Suggested Django App Structure

Since the preferred technology stack is Django, the system can be structured as follows:

```text
campaignmasta/
│
├── accounts/
│   ├── CustomUser
│   ├── Roles
│   ├── Permissions
│   └── Authentication
│
├── tenants/
│   ├── CandidateTenant
│   ├── Subscription
│   └── TenantSettings
│
├── geography/
│   ├── Province
│   ├── District
│   ├── LLG
│   ├── Ward
│   └── Village
│
├── candidates/
│   ├── CandidateProfile
│   ├── CandidateType
│   └── CampaignProfile
│
├── teams/
│   ├── TeamMember
│   ├── RoleAssignment
│   └── CoordinatorAssignment
│
├── supporters/
│   ├── Supporter
│   ├── SupportStatus
│   └── SupporterFollowUp
│
├── crm/
│   ├── Influencer
│   ├── RelationshipStatus
│   ├── CallLog
│   ├── ReminderRule
│   └── RelationshipReminder
│
├── messaging/
│   ├── Message
│   ├── MessageRecipient
│   ├── MessageReadReceipt
│   └── BroadcastGroup
│
├── events/
│   ├── CampaignEvent
│   ├── EventAttendance
│   ├── EventChecklist
│   └── EventReport
│
├── tasks/
│   ├── CampaignTask
│   └── TaskComment
│
├── intelligence/
│   ├── WardProfile
│   ├── Landmark
│   ├── CommunityIssue
│   └── PromiseTracker
│
├── polling/
│   ├── PollingLocation
│   ├── Scrutineer
│   ├── PollingIncident
│   └── PollingStatus
│
├── aiassistant/
│   ├── WardBriefGenerator
│   ├── SpeechAssistant
│   └── SummaryGenerator
│
├── reports/
│   ├── DashboardMetrics
│   ├── ReportExports
│   └── Analytics
│
├── audit/
│   ├── AuditLog
│   └── AccessLog
│
└── core/
    ├── BaseModel
    ├── Utilities
    └── SharedServices
```

---

## 28. Core Database Models

### 28.1 CandidateTenant

```text
id
name
candidate
candidate_type
province
district: nullable for Provincial Candidate
subscription_plan
status
created_at
updated_at
```

### 28.2 CandidateProfile

```text
id
tenant
full_name
photo
party
candidate_type
province
district
slogan
biography
phone
email
campaign_office
status
```

### 28.3 TeamMember

```text
id
tenant
user
full_name
phone
email
role
province
district
llg
ward
village
is_active
last_login
```

### 28.4 Supporter

```text
id
tenant
full_name
phone
gender
age_range
province
district
llg
ward
village
clan
church_group
support_status
influence_level
main_issue
consent_to_messages
registered_by
follow_up_required
follow_up_date
notes
```

### 28.5 Influencer

```text
id
tenant
full_name
phone
email
province
district
llg
ward
village
community_role
influence_category
influence_level
influence_score
relationship_status
preferred_contact_method
contact_frequency_days
last_call_date
last_meeting_date
last_message_date
next_contact_due_date
assigned_owner
notes
```

### 28.6 CallLog

```text
id
tenant
caller
person_called
person_type
phone_number
call_datetime
call_outcome
discussion_summary
issues_raised
commitments_made
follow_up_required
follow_up_date
next_call_due_date
call_duration
recorded_by
```

### 28.7 Message

```text
id
tenant
sender
recipient_type
recipient_group
subject
body
priority
delivery_channel
scheduled_send_date
status
read_receipt_required
acknowledgement_required
created_at
sent_at
```

### 28.8 CampaignEvent

```text
id
tenant
title
event_type
province
district
llg
ward
village
venue
landmark
host_person
start_datetime
end_datetime
expected_crowd_size
actual_attendance
talking_points
security_notes
event_report
```

### 28.9 CommunityIssue

```text
id
tenant
title
category
description
province
district
llg
ward
village
reported_by
priority
status
related_event
created_at
updated_at
```

### 28.10 PromiseTracker

```text
id
tenant
title
description
made_by
made_to
province
district
llg
ward
event
promise_date
target_date
status
follow_up_owner
notes
```

---

## 29. Key Workflows

### 29.1 Candidate Onboarding Workflow

1. CampaignMasta admin creates candidate tenant.
2. Candidate type is selected:
   - District Open
   - Provincial
3. Province is selected.
4. If District Open, district is selected.
5. System loads relevant geography.
6. IT Administrator is created.
7. Campaign Manager is created.
8. Team hierarchy is configured based on candidate type.
9. Coordinators are added.
10. Ward profiles are completed.
11. Supporter registration begins.

### 29.2 District Open Candidate Setup

1. Select candidate type: District Open.
2. Select province.
3. Select district/open electorate.
4. Add Campaign Manager.
5. Add IT Administrator.
6. Add LLG Coordinators.
7. Add Ward Coordinators.
8. Add Village Coordinators.
9. Add influencers and supporters.
10. Begin call monitoring and reporting.

### 29.3 Provincial Candidate Setup

1. Select candidate type: Provincial.
2. Select province.
3. System loads all districts.
4. Add Campaign Manager.
5. Add IT Administrator.
6. Add District Coordinators.
7. Add LLG Coordinators under each district.
8. Add Ward Coordinators.
9. Add Village Coordinators.
10. Add influencers and supporters.
11. Begin province-wide call monitoring and reporting.

### 29.4 Call Monitoring Workflow

1. Influencer or coordinator is added.
2. Contact frequency rule is selected.
3. System calculates next contact due date.
4. Daily reminder engine checks due and overdue calls.
5. Candidate/manager sees call checklist.
6. User records call outcome.
7. System updates last call date.
8. System schedules next call.
9. Overdue calls trigger escalation alerts.

### 29.5 Messaging Workflow

1. User creates message.
2. User selects target group.
3. System filters recipients based on role, geography, and consent.
4. User previews recipient count.
5. Message is sent or scheduled.
6. System tracks delivery, read receipt, and acknowledgement.
7. Campaign Manager views non-read or non-acknowledged recipients.

---

## 30. Development Phases

### Phase 1: Core SaaS Foundation

- User authentication
- Candidate tenant management
- Candidate profile
- Candidate type logic
- Geography module
- Role-based access control
- Team management
- Basic dashboard

### Phase 2: Ward and Supporter Management

- Ward intelligence
- Supporter registry
- Influencer registry
- Duplicate detection
- CSV import
- Basic reports

### Phase 3: Relationship and Call Monitoring

- Call logs
- Contact frequency rules
- Call checklist
- Reminder engine
- Escalation alerts
- Relationship dashboard

### Phase 4: Messaging and Task Management

- Internal messaging
- Broadcast messaging
- Read receipts
- Acknowledgements
- Task assignment
- Notifications

### Phase 5: Events, Issues, and Promises

- Campaign event planner
- Event checklist
- Attendance records
- Community issues tracker
- Promise tracker
- Speech/talking point data preparation

### Phase 6: AI Assistant

- Ward brief generator
- Speech note generator
- Daily summary
- Suggested call list
- Issue trend analysis
- Message drafting assistant

### Phase 7: Polling-Day Operations

- Polling locations
- Scrutineer assignments
- Incident reports
- Polling-day dashboard
- Emergency messages

### Phase 8: Constituency Management

- Citizen request registry
- Project tracking
- Community grant tracking
- Ward development plans
- Post-election service delivery dashboard

---

## 31. Minimum Viable Product

The MVP should include:

1. Candidate tenant setup
2. Candidate type selection
3. District Open vs Provincial hierarchy rules
4. Geography module
5. Team management
6. Ward coordinator records
7. Supporter registry
8. Influencer registry
9. Call monitoring checklist
10. Basic reminders
11. Messaging to teams
12. Ward intelligence profiles
13. Basic dashboards and reports

---

## 32. Future Enhancements

- Mobile app for coordinators
- Offline data capture
- SMS gateway integration
- WhatsApp Business API integration
- GIS campaign map
- Voice call integration
- Automatic call logging through mobile app
- Biometric login for field users
- Tok Pisin language support
- AI speech generator in Tok Pisin
- Mobile polling-day command centre
- Integration with payment gateways for subscriptions
- White-label version for political parties

---

## 33. Critical Build Principles

1. Candidate type must drive hierarchy and permissions.
2. Every record must belong to a candidate tenant.
3. District Open candidates must not require District Coordinators.
4. Provincial candidates must include District Coordinators.
5. Ward-level data must roll up correctly based on candidate type.
6. Messaging must be targeted by role and geography.
7. Call monitoring must be central to the relationship CRM.
8. The system must protect sensitive personal and political data.
9. The app must work well on mobile because coordinators will use phones.
10. The platform must continue to provide value after elections.

---

## 34. Final Product Vision

CampaignMasta should become the leading campaign intelligence and political CRM platform for PNG candidates.

It should help politicians answer these daily questions:

- Which ward needs my attention?
- Which coordinator has gone quiet?
- Which influential person have I not called?
- Which community issues are rising?
- Which supporters need follow-up?
- Which areas are strong, weak, or undecided?
- What should I say when I visit this ward?
- Who needs to receive today's message?
- Are my campaign teams active?
- Are we ready for polling day?

CampaignMasta should not only help candidates campaign better. It should help them build disciplined, data-driven, respectful, and continuous relationships with people before, during, and after elections.

