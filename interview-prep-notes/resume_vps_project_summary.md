# Vehicle Processing System (VPS) - Resume Summary

## Position Context
**Role**: Junior Software Engineer → Software Engineer
**Company**: Copart
**Tech Stack**: JRuby, Sinatra, Sequel ORM, IBM DB2/AS400 (116 legacy models), MariaDB (28 VPS models), Redis, Sidekiq Pro, Apache Kafka, Firebase Realtime Database (Google SDK), Apache Solr, Docker, RSpec

---

## Project Overview

Developed and maintained three interconnected microservices modules within Copart's **Vehicle Processing System (VPS)** — a large-scale JRuby/Sinatra platform managing the complete salvage vehicle lifecycle from buyer pickup scheduling through yard departure across US and UK markets.

---

## Core Modules & Contributions

### 1. **Buyer Pickup Module** (61 services, 337-line API handler)

Built RESTful APIs for buyer and transporter management, enabling self-service vehicle pickup operations:

- **Appointment Scheduling**: Developed appointment creation and rescheduling services with capacity management, facility schedules, holiday handling, and slot availability validation
- **Transporter Management**: Implemented user registration, vehicle management, QR code generation for gate access, and transporter blocking/activation workflows
- **Real-time Search**: Integrated Apache Solr for full-text search across appointments and lots, with bulk/individual indexing services for mobile app consumption
- **Notifications**: Built push notification and SMS services for appointment reminders and status updates
- **UK Hazardous Waste Compliance**: Designed and implemented ATF (Authorized Treatment Facility) permit validation, CBDU waste number verification, and conditional document generation workflows for Category B hazardous vehicles
- **Lot Validation**: Created lot status tracking, payment verification, and QR code validation for secure pickup authorization

### 2. **Loader Bundle Module** (35 services, 121-line API handler)

Developed APIs for yard operations and real-time vehicle tracking during loading/transport:

- **Transporter Queue Management**: Built services for transporter creation, activation, blacklisting, and bulk Firebase synchronization for real-time mobile tracking
- **Lot Lifecycle Operations**: Implemented claim, deliver, unclaim, undeliver, and delete workflows with lot staging/unstaging capabilities
- **Lot Left Yard (LLY) Processing**: Developed country-specific (US/UK) lot departure workflows with hazardous waste document creation, electronic member signatures, and Dispatch API integration
- **Real-time Firebase Tracking**:
  - Integrated Firebase Realtime Database with Sequel ORM hooks for automatic sync on every lot status change (claim, deliver, stage)
  - Built Firebase path structure (`facility_id/transporter_id/lots/lot_num`) enabling mobile apps to query lots by facility and transporter
  - Synced nested JSON payloads including lot details, appointment info, buyer data, images, and real-time flags to Firebase
  - Implemented conditional Firebase operations - update on status change, delete on completion/cancellation
  - Enabled live transporter queue tracking for iOS/Android loader apps without polling
- **Database Architecture**:
  - Built `Ycs::LoaderBundle::Activity` model (MariaDB) with associations to `Ycs::Cas::Lot` (DB2/AS400) for cross-database joins
  - Implemented eager loading with `.eager(:lot, :active_appointment_detail, :lot_extension, :yds_lot)` for performance
  - Used database transactions with after_commit hooks for reliable Firebase sync
- **Hazardous Waste Handling**: Engineered three conditional processing paths for UK CATB lots:
  - **Overseas with ATF**: Fast-track claim with automated document creation and e-sign at yard departure
  - **Overseas without ATF**: Manual compliance path with CBDU-only updates
  - **Domestic**: Standard automation with e-sign workflows
- **Background Jobs**: Built asynchronous Sidekiq jobs for bulk operations and document generation with Dispatch API integration

### 3. **Appointment Module** (18 services, 101-line API handler)

Developed VVV (Vehicle Viewing Visit) appointment system for facility staff and external members:

- **Appointment Management**: Created services for appointment creation, confirmation, cancellation, and bulk updates with lot-level action tracking
- **Schedule Administration**: Built default schedule management, date-range scheduling, and capacity planning services
- **Event Logging**: Implemented comprehensive audit trail system capturing appointment and lot-level events for compliance and debugging
- **Search & Filtering**: Developed list services with facets, quick counts, and detail views for appointment querying
- **Notifications**: Integrated SMS text messaging for appointment confirmations and reminders
- **Reference Data**: Built services for facility information, reason codes, and appointment metadata

---

## Technical Achievements

### Database & ORM (Dual Database Architecture)

**MariaDB (Primary VPS Database)**
- Designed and maintained 28+ Sequel ORM models across buyer_pickup, loader_bundle, and appointment domains (MariaDB tables)
- Implemented model lifecycle hooks (before_save, after_save, before_create) for auditing, defaults, and Firebase synchronization
- Built complex multi-table joins with eager loading across VPS tables for performance optimization
- Managed database transactions with after_commit hooks for reliable Firebase sync

**IBM DB2/AS400 (Legacy CAS Mainframe)**
- Integrated with 116 legacy CAS (Copart Auction System) models on IBM DB2/AS400 mainframe database
- Implemented dynamic schema resolution - queries `sysibm.tables` at runtime to find correct schema for multi-schema environments
- Built custom CAS field mappers to handle DB2's packed decimal date/time fields (century, year, month, day components) and convert to Ruby Date/Time objects
- Handled cross-database joins between MariaDB (VPS) and DB2 (CAS) - e.g., `Ycs::LoaderBundle::Activity` (MariaDB) joining `Ycs::Cas::Lot` (DB2) via lot_number
- Worked with connection pooling and FILE lock error handling for DB2's record-level locking mechanism

**Database Operations**
- Built Sequel model base classes (`Ycs::BuyerPickup::Base`, `Ycs::LoaderBundle::Base`) with shared concerns for validations, user tracking, and timezone handling
- Implemented complex eager loading strategies: `.eager(:lot, :active_appointment_detail, :lot_extension, :yds_lot)` for N+1 query prevention
- Used Sequel's `.where()`, `.eager_graph()`, `.select()`, and `.all()` for optimized queries
- Managed UTC timestamp handling for multi-timezone support (US/UK)
- Built custom field mapping system to translate DB2 abbreviated column names (e.g., `lblotnbr`, `ltbuynbr`) to readable names

### API Development
- Built 100+ RESTful endpoints following consistent service-oriented architecture (validate → execute → respond pattern)
- Implemented proper HTTP status codes, error handling, and JSON response formatting
- Designed idempotent APIs for retry safety in distributed systems

### Asynchronous Processing
- Developed 23+ Sidekiq Pro background jobs for document generation, bulk Firebase synchronization, Solr indexing, and external Dispatch API integration
- Implemented job retry logic, error handling, dead letter queue management, and idempotent job execution
- Built Kafka consumer jobs for processing CAS data change events and Dispatch system changes
- Used Redis as Sidekiq job queue backend for reliable async processing

### Real-time Systems

**Firebase Realtime Database (Mobile App Sync)**
- Architected Firebase integration triggered by Sequel ORM model hooks - automatic sync to Firebase on every database save via `after_save` callbacks
- Designed hierarchical Firebase path structure: `facility_id/transporter_id/lots/lot_num` for efficient mobile app queries by facility and transporter
- Built `sync_to_firebase()` method with conditional logic - updates Firebase on claim/deliver actions, deletes Firebase node on lot completion/cancellation
- Implemented `direct_sync_to_firebase()` for force-sync scenarios and transporter-level updates
- Synced complex nested JSON payloads to Firebase including lot details, appointment info, buyer data, images, disclaimers, and real-time status flags
- Integrated Google Firebase Java SDK in JRuby environment - imported Java classes (`FirebaseOptions`, `FirebaseCredentials`, `FirebaseDatabase`) for database reference and authentication
- Built Firebase service wrapper with error handling, connection management, and update/delete operations
- Enabled real-time transporter queue tracking for iOS/Android mobile apps - loaders see live lot status updates without polling
- Handled Firebase-offline scenarios gracefully - included `firebase_online` flag in API responses to inform mobile clients of sync status

**Apache Solr (Full-Text Search)**
- Integrated Apache Solr for appointment and lot search with bulk/individual indexing services
- Built Solr query services for member detail lookups, faceted search, and quick counts
- Implemented real-time Solr updates via Sidekiq background jobs for eventual consistency

**Apache Kafka (Event Streaming)**
- Built event-driven architecture with Kafka for cross-service communication
- Published lot activity events for downstream consumers (APRSC integration)

### Multi-Country Support
- Implemented country-specific business logic for US and UK markets within a unified codebase
- Handled regulatory compliance variations (UK hazardous waste, US state-specific requirements)
- Built conditional processing paths based on member/lot country combinations

### Testing & Quality
- Wrote RSpec integration and unit tests using Airborne gem for API endpoint validation
- Implemented request correlation IDs for distributed tracing and debugging
- Built comprehensive error handling with meaningful validation messages

---

## Key UK Hazardous Waste Project (Major Feature)

Designed and implemented end-to-end regulatory compliance for UK Category B hazardous waste vehicles:

- **Scope**: Full lot lifecycle from appointment scheduling through yard departure
- **Complexity**: Engineered three distinct processing paths (overseas with/without ATF permits, domestic) with conditional validation rules, API integrations, and document workflows at each stage (Schedule, Arrive, Claim, Lot Left Yard)
- **Integration**: Connected to 6 external Dispatch API endpoints for hazardous waste documentation, electronic member signatures, carrier/broker waste number (CBDU) validation, and document lifecycle management
- **Async Processing**: Built Sidekiq background jobs for document generation pipeline with real-time status synchronization to Firebase and Solr
- **Edge Cases**: Handled complex bulk-lot scenarios mixing CATB and non-CATB lots, overseas and domestic members, with idempotent API calls and production-hardened error handling
- **Files Modified**: 25+ files across services, models, handlers, and background jobs

---

## Impact & Scale

- **Services**: 114 services (~10,000 lines of business logic)
- **Models**: 28 Sequel ORM models
- **Background Jobs**: 23 Sidekiq jobs
- **API Endpoints**: 100+ RESTful endpoints
- **Markets**: Multi-country deployment (US + UK)
- **Mobile Integration**: Real-time data for iOS/Android transporter apps via Firebase and Solr

---

## Technical Skills Demonstrated

- **Backend Development**: JRuby, Ruby, Sinatra framework, RESTful API design
- **Databases**: IBM DB2/AS400, MariaDB, Sequel ORM, Redis
- **Async Processing**: Sidekiq Pro, background job patterns, job retry strategies
- **Real-time Systems**: Firebase Realtime Database, Apache Solr full-text search
- **Event Streaming**: Apache Kafka for event-driven architecture
- **Testing**: RSpec, Airborne gem, integration/unit testing
- **DevOps**: Docker containerization, Prometheus monitoring, distributed tracing
- **Architecture**: Service-oriented architecture, multi-country support, regulatory compliance

---

## Resume Bullet Point Options

### Option A: Full Project Description (3-5 bullets)

- Developed and maintained 114 RESTful services across three microservices modules (Buyer Pickup, Loader Bundle, Appointment) in a JRuby/Sinatra platform managing Copart's salvage vehicle lifecycle operations across US and UK markets
- Built appointment scheduling APIs with capacity management, transporter registration, QR code validation, push notifications, and real-time Apache Solr search integration for mobile app consumption
- Implemented yard operations APIs for lot lifecycle management (claim, deliver, stage, left yard) with Firebase Realtime Database integration using Sequel ORM hooks for automatic real-time sync on every status change, enabling live transporter queue tracking on iOS/Android mobile apps without polling
- Architected dual database system with 28 Sequel ORM models (MariaDB) for VPS tables and 116 legacy models (IBM DB2/AS400) for CAS mainframe system, implementing cross-database joins, custom field mappers for DB2 abbreviated columns, and connection pooling for FILE lock handling
- Designed UK hazardous waste compliance module handling three conditional processing paths for Category B vehicles — integrating ATF permit validation, CBDU waste number verification, electronic signature workflows, and asynchronous document generation via Sidekiq Pro background jobs with 6 external Dispatch API endpoints and Redis job queue

### Option B: Mid-Level Focus (2-3 bullets)

- Built and maintained 114 RESTful services in a JRuby/Sinatra microservices platform managing vehicle pickup scheduling, yard operations, and appointment workflows for Copart's US and UK markets
- Architected dual database system with Sequel ORM — 28 MariaDB models for VPS tables and 116 IBM DB2/AS400 models for legacy CAS mainframe, implementing cross-database joins, custom field mappers, and Firebase Realtime Database sync via ORM hooks for live mobile app tracking
- Implemented UK hazardous waste compliance for Category B vehicles with conditional processing logic, ATF permit validation, electronic signatures, async document generation (Sidekiq Pro), and external Dispatch API integration

### Option C: Compact (1-2 bullets)

- Developed 114 RESTful services in a JRuby/Sinatra platform for vehicle processing operations (buyer pickup, yard loading, appointments) across US/UK markets with dual database architecture (28 MariaDB models, 116 IBM DB2/AS400 legacy models), Firebase Realtime Database sync via Sequel ORM hooks, Apache Solr search, Sidekiq Pro async jobs, and Kafka event streaming
- Designed and implemented UK hazardous waste compliance module with conditional processing paths, ATF permit validation, electronic signature workflows, and asynchronous document generation

### Option D: Skills-Forward (emphasizes technologies)

- Built RESTful APIs using JRuby/Sinatra framework with Sequel ORM managing dual database architecture: 28 MariaDB models for VPS tables and 116 IBM DB2/AS400 models for legacy mainframe with cross-database joins, custom field mappers, and connection pooling
- Integrated Firebase Realtime Database with Sequel ORM lifecycle hooks (after_save, after_commit) for automatic real-time sync to mobile apps, Apache Solr for full-text search, Redis for caching/job queues, and Apache Kafka for event streaming
- Developed asynchronous workflows using Sidekiq Pro for document generation and external API integration, handling UK regulatory compliance with conditional business logic for hazardous waste vehicles
- Wrote RSpec integration tests, implemented distributed tracing with correlation IDs, and deployed Docker containers with Prometheus monitoring across multi-country environments (US/UK)

---

## Talking Points for Interviews

1. **Service-Oriented Architecture**: Explain the validate → execute → respond pattern used across all 114 services
2. **Dual Database Architecture**:
   - MariaDB for VPS tables (buyer_pickup, loader_bundle, appointment) with 28 Sequel models
   - IBM DB2/AS400 for legacy CAS mainframe with 116 models
   - Cross-database joins (e.g., Activity [MariaDB] joining Cas::Lot [DB2])
   - Dynamic schema resolution querying sysibm.tables
   - Custom field mappers for DB2 packed decimal date/time fields
   - Connection pooling and FILE lock handling
3. **Firebase Real-time Integration**:
   - Sequel ORM lifecycle hooks (after_save, after_commit) trigger Firebase sync
   - Path structure: facility_id/transporter_id/lots/lot_num
   - Conditional sync logic (update vs delete based on status)
   - Nested JSON payloads with lot/appointment/buyer data
   - Google Firebase Java SDK integration in JRuby
   - Enables live transporter queue tracking on mobile apps
4. **Complex Business Logic**: Walk through the three conditional paths in UK hazardous waste (ATF-based routing)
5. **Async Processing**: Discuss Sidekiq job patterns, retry strategies, and idempotency for external API calls
6. **Multi-Country Support**: Describe how country-specific logic is handled within a unified codebase
7. **Testing Strategy**: RSpec integration tests, API endpoint validation, correlation ID tracing
8. **Error Handling**: Comprehensive validation, meaningful error messages, HTTP status code usage
