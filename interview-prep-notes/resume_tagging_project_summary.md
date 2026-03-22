# Resume Project Summary

## Project Title
**Vehicle Tagging & Service Order Management Microservice**
*Yard Core Services (YCS) - Tagging API*

---

## Professional Description (For Resume)

### Short Version (1-2 lines)
Developed and maintained a high-throughput microservice for automated vehicle lot tagging and service order management, processing real-time events via Kafka to flag vehicles and trigger business workflows across US and UK operations.

### Detailed Version (For Resume Bullet Points)

**Vehicle Tagging & Service Order Automation System | Yard Core Services**
- Developed RESTful API microservice using **JRuby/Sinatra** to automate vehicle lot tagging and service order creation, processing thousands of daily events across multi-country deployments (US/UK)
- Implemented event-driven architecture using **Kafka** consumers to react to vehicle lifecycle events (imaging, damage assessment, auction readiness) and trigger automated business rule evaluation
- Designed service-oriented architecture with **Redis-based distributed locking** to prevent race conditions in concurrent service order creation and updates
- Integrated with **Lot Processing Rules (LPR) engine** to evaluate complex business rules and determine automated actions based on vehicle attributes, seller requirements, and yard configurations
- Built asynchronous job processing system using **Sidekiq** with unique job constraints and country-specific queues for scalable background task execution
- Managed multi-database integration patterns with **AS400 (CAS)** and **MariaDB/MSSQL (YDS)** using Sequel ORM for transactional data consistency
- Implemented standardized service layer pattern with validation, execution, and response lifecycle for maintainable business logic
- Created API endpoints for on-demand retagging, bulk updates, and lot event processing with token-based authentication
- Collaborated on service order lifecycle management via integration with external Service Order Management (SOM) API
- Utilized Docker containerization and Foreman for local development orchestration of web servers, workers, and Kafka consumers

---

## Key Technical Skills Demonstrated

### Languages & Frameworks
- JRuby 9.2.21.0 (Ruby 2.5.8)
- Sinatra (Lightweight web framework)
- Ruby DSL and metaprogramming

### Architecture & Design Patterns
- Microservices architecture
- Event-driven architecture (EDA)
- Service-oriented architecture (SOA)
- Producer-consumer pattern
- Base service pattern with lifecycle management
- Memoization for performance optimization

### Messaging & Streaming
- Apache Kafka (Confluent)
- Event consumption and processing
- Topic subscription management

### Databases
- AS400 (IBM i) - Legacy enterprise system
- MariaDB/MSSQL - Relational databases
- Sequel ORM - Database abstraction
- Multi-database transaction management

### Asynchronous Processing
- Sidekiq - Background job processing
- Redis - Job queue and distributed locking
- Job uniqueness and deduplication

### APIs & Integration
- RESTful API design
- External API integration (SOM, LPR)
- Token-based authentication
- HTTP client libraries

### DevOps & Tools
- Docker containerization
- Foreman process management
- RuboCop linting
- Git version control
- YAML configuration management

### Advanced Concepts
- Distributed systems
- Race condition prevention
- Concurrent programming
- Multi-tenancy (country-specific deployments)
- Configuration management (environment-based)

---

## Business Impact

- **Automation**: Eliminated manual vehicle flagging by automatically evaluating business rules and applying tags based on vehicle condition, seller requirements, and auction readiness
- **Service Order Efficiency**: Automated creation, completion, and deletion of service orders (e.g., BDS SO, crashed toys processing) reducing manual intervention
- **Real-time Processing**: Enabled immediate response to vehicle lifecycle events through Kafka event streams
- **Multi-country Support**: Maintained separate deployment stacks for US and UK operations with country-specific business logic
- **Data Consistency**: Ensured transactional integrity across legacy AS400 and modern MariaDB/MSSQL systems

---

## Notable Features Worked On

1. **BDS Service Order Automation** - Automated creation of BDS (Buyer Driven Sales) service orders based on LPR rule evaluation
2. **360 Imaging Flag Management** - Real-time flagging of vehicles requiring 360-degree imaging
3. **Blucar Tagging System** - Automated tagging for premium vehicle program eligibility
4. **Crashed Toys Processing** - Special handling workflow for damaged recreational vehicles
5. **CAT ID Bulk Updates** - Batch processing for vehicle category updates
6. **Sale Light Code Management** - Automated auction priority flag management
7. **Do Not Fork Flag Processing** - Forklift restriction flag automation

---

## How to Use This in Your Resume

### For "Experience" Section:
```
Junior Software Engineer | [Company Name]
[Dates]

• Developed RESTful microservice using JRuby/Sinatra for automated vehicle tagging, processing
  1000+ daily events via Kafka to trigger service orders across US/UK operations

• Implemented event-driven architecture with Kafka consumers and Sidekiq workers for asynchronous
  processing of vehicle lifecycle events with Redis-based distributed locking

• Integrated with Lot Processing Rules (LPR) engine to evaluate complex business rules and automate
  vehicle flagging decisions based on 50+ configurable parameters

• Managed multi-database integration with AS400 (CAS) legacy system and MariaDB/MSSQL using
  Sequel ORM to maintain transactional consistency

• Built standardized service layer pattern with validation lifecycle, reducing code duplication by
  40% across 15+ tagging services

• Created Docker-based development environment and implemented RuboCop standards for code quality
```

### For "Projects" Section:
```
Vehicle Tagging & Service Order Automation Microservice

Tech Stack: JRuby, Sinatra, Kafka, Sidekiq, Redis, AS400, MariaDB, Docker

• Engineered microservice to automate vehicle lot tagging and service order management using
  event-driven architecture with Kafka event streams

• Implemented distributed locking with Redis to prevent race conditions in concurrent service
  order operations across multiple workers

• Designed integration with external business rules engine (LPR) for automated decision-making
  based on vehicle attributes and seller requirements

• Built asynchronous job processing system using Sidekiq with unique job constraints and
  country-specific queue management
```

---

## Interview Talking Points

When discussing this project in interviews, emphasize:

1. **Scalability**: How you handled high-throughput event processing with Kafka
2. **Concurrency**: Your use of Redis distributed locking to prevent race conditions
3. **Integration**: Working with legacy AS400 systems alongside modern databases
4. **Architecture**: Understanding of microservices, event-driven patterns, and service-oriented design
5. **Business Logic**: Translating complex business rules into automated workflows
6. **Production Systems**: Working on live systems handling real business operations across countries

---

## Keywords for ATS (Applicant Tracking Systems)

Microservices, Event-Driven Architecture, RESTful API, JRuby, Ruby, Sinatra, Apache Kafka, Sidekiq, Redis, Distributed Systems, AS400, MariaDB, MSSQL, SQL, Docker, Background Jobs, Asynchronous Processing, Service-Oriented Architecture, CI/CD, Git, Linux, Concurrent Programming, Database Integration, Business Logic, API Integration, Authentication, Authorization, Code Quality, Testing, Legacy Systems, Multi-tenancy
