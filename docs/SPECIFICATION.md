# SPACE GUARD AI
## Product Requirements, Business Rules and Technical Architecture Specification

# PART I — PRODUCT DEFINITION

# 1. Project Overview

## 1.1. Purpose

SPACE GUARD AI is an intelligent software assistant designed to support astronauts during simulated extravehicular activities (EVA).

The system combines two complementary information domains:

1. **Astronaut and Suit Monitoring:** simulated telemetry representing the astronaut's suit, environmental conditions, equipment status, and operational resources.
2. **Planetary Environmental and Scientific Context:** publicly accessible scientific and geospatial information from NASA missions and other recognized planetary data sources.

The system processes these information domains, identifies relevant operational conditions, generates deterministic alerts, and provides contextual assistance through an AI-powered conversational interface.

Its primary purpose is to demonstrate how an intelligent assistant can help an astronaut understand equipment conditions and contextualize mission-related environmental information.

The initial release is a software prototype. It does not connect to physical astronaut equipment, certified life-support systems, or operational NASA mission infrastructure.

## 1.2. Product Vision

The product should function as an intelligent information layer between the astronaut and multiple sources of mission-related information.

Rather than merely displaying isolated sensor readings, SPACE GUARD AI should:

- Monitor simulated suit and astronaut telemetry.
- Retrieve relevant planetary environmental and scientific information.
- Organize information from different sources into a consistent internal representation.
- Identify potentially relevant relationships between equipment conditions and the mission environment.
- Generate deterministic alerts based on configured rules.
- Explain current conditions through a contextual AI assistant.
- Present relevant information through a helmet-inspired HUD interface.

The system must distinguish between directly observed telemetry, simulated measurements, externally retrieved scientific observations, derived information, and AI-generated explanations.

## 1.3. Main Objectives

The system must:

1. Receive and process simulated astronaut telemetry.
2. Retrieve information from publicly accessible NASA and planetary science sources.
3. Normalize heterogeneous external data into consistent internal representations.
4. Preserve the provenance, timestamp, units, and limitations of retrieved information.
5. Maintain a distinction between suit telemetry and planetary environmental data.
6. Monitor equipment and environmental parameters.
7. Evaluate configurable operational rules deterministically.
8. Generate, prioritize, and distribute alerts.
9. Provide contextual assistance through an AI abstraction layer.
10. Maintain continuous communication with the HUD.
11. Support future data-source integrations without requiring changes to the core business logic.
12. Remain operational when external data sources or AI providers are unavailable.

## 1.4. Scope

The initial release includes:

### Astronaut and Suit Monitoring
- Simulated oxygen readings.
- Simulated cabin or suit pressure.
- Simulated suit temperature.
- Simulated battery level.
- Simulated radiation readings.
- Simulated astronaut coordinates.
- Simulated communication status.
- Configurable abnormal scenarios.

### External Planetary Data Integration
- Integration architecture for public NASA and planetary data sources.
- Source discovery and metadata retrieval.
- Retrieval of relevant scientific and environmental observations.
- Data normalization and validation.
- Source attribution and timestamps.
- Basic caching and stale-data identification.
- Contextual access to external information by the AI assistant.

### Operational Intelligence
- Telemetry processing.
- Deterministic safety rules.
- Alert generation and deduplication.
- Mission context management.
- Contextual AI assistance.
- Real-time event distribution.

### User Interface
- Astronaut-inspired HUD.
- Telemetry visualization.
- Environmental context visualization.
- Alert management.
- Data-source status.
- AI assistant interaction.
- Simulation controls.

### Engineering and Delivery
- Modular application architecture.
- Automated testing.
- Containerized execution.
- English technical documentation.

## 1.5. Out of Scope

The initial release will not include:

- Physical helmet integration.
- Real astronaut biometric monitoring.
- Certified life-support monitoring.
- Autonomous spacecraft or equipment control.
- Direct access to operational NASA mission systems.
- Guaranteed real-time data from NASA missions.
- Medical diagnosis.
- Autonomous emergency procedures.
- Certified navigation or EVA route planning.
- Guaranteed communication with Mission Control.
- Autonomous modification of mission parameters.
- Claims of NASA endorsement or certification.

All astronaut and equipment telemetry will initially be simulated.

External planetary information will be retrieved only through publicly accessible sources and supported interfaces.

---

# PART II — BUSINESS DOMAIN AND INFORMATION MODEL

# 2. Core Business Domains

SPACE GUARD AI must be organized around clearly separated business domains.

## 2.1. Suit and Astronaut Telemetry Domain

This domain represents the simulated operational state of the astronaut and the equipment.

Its responsibility is to process measurements associated with the suit and astronaut.

Initial parameters:

| Parameter | Description | Unit |
|---|---|---|
| Oxygen availability | Simulated oxygen availability or supply measurement | Explicitly defined per sensor |
| Pressure | Simulated internal suit or cabin pressure | psi |
| Suit temperature | Simulated suit temperature | °C |
| Battery level | Simulated battery charge | % |
| Radiation rate | Simulated instantaneous radiation rate | mSv/h |
| Astronaut position | Simulated geographical or planetary coordinates | Latitude/longitude or planetary coordinates |
| Communication status | Simulated connection state | Connected/disconnected |

The oxygen measurement must explicitly define its physical meaning.

A percentage must not be ambiguously interpreted as oxygen concentration, oxygen tank capacity, or oxygen partial pressure.

These are different measurements and must be represented as separate properties when required.

## 2.2. Planetary Environmental and Scientific Data Domain

This domain represents external information obtained from public scientific and planetary data sources.

Its responsibility is to retrieve and contextualize information about the planetary environment.

Potential information includes:

- Surface imagery.
- Terrain elevation.
- Geological characteristics.
- Mineralogical observations.
- Surface temperature.
- Environmental conditions recorded by robotic missions.
- Geographic coordinates and spatial references.
- Scientific observations associated with specific regions.

The system must preserve the distinction between environmental observations made by robotic missions and current conditions at the astronaut's location.

For example, MEDA observations collected by the Perseverance rover must not be presented as live measurements from the astronaut's suit.

## 2.3. Mission Context Domain

This domain maintains the information necessary to interpret the current simulated mission.

It may include:

- Mission identifier.
- Mission status.
- Target planetary body.
- Current simulated location.
- Current operational phase.
- Relevant scientific observations.
- Active alerts.
- Recent events.
- Data-source availability.

Mission context must provide a coherent representation of the information consumed by the assistant and displayed by the HUD.

## 2.4. Safety and Alert Domain

This domain evaluates operational conditions independently from the AI assistant.

It is responsible for:

- Applying deterministic rules.
- Detecting abnormal conditions.
- Generating alerts.
- Managing alert lifecycle.
- Preventing duplicate notifications.
- Maintaining alert history during the application session.

The AI model must never be responsible for determining whether a critical alert should exist.

## 2.5. AI Assistance Domain

This domain provides conversational access to the information maintained by the other domains.

It is responsible for:

- Explaining telemetry.
- Explaining active alerts.
- Summarizing mission conditions.
- Contextualizing retrieved planetary information.
- Answering questions using available and attributable data.
- Identifying missing or outdated information.

The assistant must not fabricate measurements, scientific observations, source references, or operational procedures.

---

# 3. External Public Data Sources

## 3.1. Integration Objective

The system must be capable of consuming public planetary science and geospatial information relevant to Mars exploration.

External sources must enrich the mission context rather than replace the suit telemetry monitoring system.

The initial implementation should prioritize a small number of reliable and relevant integrations.

Additional sources may be added through the same integration architecture.

## 3.2. Candidate Sources

The following sources are candidates for integration.

Their availability, access mechanisms, licensing conditions, data formats, and query capabilities must be verified before implementation.

| Source | Primary purpose | Potential use |
|---|---|---|
| NASA Planetary Data System (PDS) | Scientific planetary mission archives | Retrieve mission observations and scientific datasets |
| HiRISE | High-resolution Mars imagery | Surface inspection and terrain context |
| CTX | Context Camera imagery | Regional surface context |
| CRISM | Mineralogical observations | Identify and contextualize mineralogical information |
| THEMIS | Thermal and visual observations | Surface and thermal context |
| TES | Thermal emission observations | Historical thermal and mineralogical context |
| MEDA | Perseverance environmental measurements | Contextualize environmental observations |
| Mars Trek / available map services | Planetary mapping and geospatial visualization | Display geographic context and map layers |
| USGS Astrogeology | Planetary cartographic resources | Reference maps, coordinate systems, and geological context |
| JMARS | Planetary data visualization and analysis | Research and exploration support where programmatic access is available |

**Important:** this is a candidate source catalogue, not a declaration that every listed resource provides a stable public REST API.

Some sources are archives, scientific instruments, map services, downloadable datasets, or visualization applications.

The implementation must identify the actual access method for each source.

## 3.3. Source Integration Classification

Each external source must be classified according to its actual access mechanism.

Supported integration categories may include:

- REST API.
- OData or another documented query protocol.
- Web Map Service (WMS).
- Web Map Tile Service (WMTS).
- Downloadable scientific dataset.
- Public metadata catalogue.
- Documented file access.
- Other documented programmatic interfaces.

A visualization application must not automatically be treated as an API.

If a source does not provide a supported programmatic interface, the system must not rely on undocumented endpoints or fragile scraping.

## 3.4. Source Registry

The application must maintain a centralized registry describing each configured source.

Each source definition should contain:

- Unique source identifier.
- Display name.
- Scientific or operational domain.
- Access method.
- Base URL or documented resource location.
- Authentication requirements, if any.
- Supported query parameters.
- Expected response format.
- Unit conventions.
- Coordinate reference system, when applicable.
- Attribution requirements.
- Availability status.
- Data freshness characteristics.

Source definitions must be configurable rather than scattered across business services.

## 3.5. Initial Integration Priorities

The implementation should use a staged integration strategy.

### Priority 1 — Geospatial and Image Context

Investigate and integrate a supported Mars imagery or mapping service.

Expected capabilities:

- Retrieve imagery or map tiles for a defined region.
- Identify spatial bounds.
- Display geographic context.
- Preserve source and acquisition metadata.

### Priority 2 — Scientific Observation Context

Investigate PDS and relevant instrument archives.

Expected capabilities:

- Search available datasets.
- Retrieve metadata.
- Identify observation location and acquisition time.
- Provide references to the original scientific records.

### Priority 3 — Environmental Context

Investigate available MEDA and THEMIS-related data access mechanisms.

Expected capabilities:

- Retrieve environmental observations.
- Identify the observing mission and instrument.
- Preserve observation timestamps.
- Distinguish historical measurements from current simulated mission conditions.

### Priority 4 — Additional Scientific Sources

Evaluate CRISM, TES, CTX, and other relevant sources according to the mission's selected geographic region and scientific requirements.

No integration should be considered complete until its access method and response format have been verified.

## 3.6. External Data Retrieval Rules

External data retrieval must follow these rules:

1. Only documented and publicly accessible interfaces may be used.
2. The system must respect source-specific access restrictions and usage policies.
3. Requests must have configurable timeouts.
4. Responses must be validated before entering the internal domain model.
5. Failed requests must not crash the application.
6. Data must retain its original source attribution.
7. Observation timestamps must be preserved.
8. Units and coordinate reference systems must be explicit.
9. The application must identify stale or unavailable information.
10. External observations must never be represented as live suit sensor measurements.

## 3.7. Data Provenance

Every normalized external observation must preserve its provenance.

Minimum metadata:

```json
{
  "observation_id": "observation-001",
  "source_id": "meda",
  "source_name": "Mars Environmental Dynamics Analyzer",
  "mission": "Mars 2020",
  "instrument": "MEDA",
  "observed_at": "2026-11-14T12:00:00Z",
  "retrieved_at": "2026-11-14T12:05:00Z",
  "data_type": "environmental_observation",
  "location": {
    "latitude": 0.0,
    "longitude": 0.0
  },
  "values": {},
  "units": {},
  "quality": "unverified",
  "source_reference": "original-source-reference"
}
```

The example is illustrative. Actual fields must be adapted to the source's documented response.

The application must distinguish:

- Observation time.
- Retrieval time.
- Processing time.
- Data validity.
- Source-reported uncertainty or quality indicators.

Unknown values must remain unknown. The application must not invent missing metadata.

---

# PART III — BUSINESS RULES

# 4. Fundamental Business Rules

The following rules govern the entire application.

## BR-001 — Separation of Information Domains

Suit telemetry and planetary scientific observations must remain separate information domains.

External planetary data must not overwrite suit sensor readings.

## BR-002 — Data Provenance

Every externally retrieved scientific observation must identify its source and preserve the available observation metadata.

## BR-003 — Deterministic Safety Evaluation

Safety conditions must be evaluated through deterministic business rules.

An AI model must never be the authority for generating, suppressing, downgrading, or overriding critical alerts.

## BR-004 — Data Availability Independence

The failure of an external NASA data source must not stop local telemetry simulation, safety evaluation, or alert generation.

## BR-005 — AI Availability Independence

The absence or failure of an AI provider must not interrupt telemetry processing or safety alert generation.

## BR-006 — Explicit Data Classification

Every information item must be identifiable as one of the following:

- Simulated telemetry.
- External scientific observation.
- Derived value.
- Operational event.
- AI-generated explanation.

## BR-007 — No Fabricated Observations

The application must never present generated or inferred values as measurements retrieved from an external scientific source.

## BR-008 — Temporal Validity

External observations must be presented with sufficient temporal context to prevent historical information from being mistaken for current conditions.

## BR-009 — No Unauthorized Operational Decisions

The system must not autonomously control suit equipment, life-support systems, spacecraft, or mission operations.

## BR-010 — Graceful Degradation

The application must remain useful when individual external sources, AI providers, or communication channels become unavailable.

---

# 5. Core Business Workflows

## 5.1. Telemetry Monitoring Workflow

1. The simulator generates a new reading.
2. The telemetry processing service validates the reading.
3. The system normalizes the measurement.
4. The latest telemetry state is updated.
5. The safety rules engine evaluates the new state.
6. Alerts are generated when applicable.
7. The system publishes telemetry and alert events.
8. The HUD updates its information.
9. The AI assistant receives the updated context when a user requests assistance.

## 5.2. External Scientific Data Workflow

1. The mission context identifies a relevant geographic region or information requirement.
2. The source registry identifies compatible data providers.
3. The integration layer constructs a source-specific request.
4. The external source returns data.
5. The source adapter validates the response.
6. The normalization layer converts the response into the internal observation model.
7. The system records provenance and timestamps.
8. The cache stores the result according to the source policy.
9. The mission context makes the observation available to the HUD and AI assistant.
10. The application identifies stale, incomplete, or unavailable information.

## 5.3. Alert Generation Workflow

1. A new telemetry reading or supported operational event becomes available.
2. The safety rules engine evaluates applicable rules.
3. A matching rule produces a structured alert.
4. The alert service assigns an identifier, severity, category, and timestamp.
5. Deduplication logic checks whether an equivalent active alert already exists.
6. The alert is stored in the current application session.
7. An alert event is broadcast to connected clients.
8. The HUD displays the alert according to its severity.

## 5.4. AI Assistance Workflow

1. The user submits a question.
2. The assistant receives the current mission context.
3. The context builder selects relevant telemetry, alerts, and external observations.
4. The assistant identifies the provenance and freshness of the information.
5. The configured AI provider generates a response.
6. The response is returned with relevant source references where applicable.
7. The user interface displays the response.

If the requested information is unavailable, the assistant must say so instead of inventing an answer.

---

# PART IV — SYSTEM ARCHITECTURE AND DESIGN PATTERNS

# 6. Architectural Principles

## 6.1. Modular Monolith

The initial system should use a modular monolithic architecture.

Business domains must be separated into well-defined modules, but they do not need to run as independent microservices.

This approach reduces operational complexity while preserving future extensibility.

## 6.2. Separation of Concerns

Each module must have one clear responsibility.

The following concerns must not be mixed:

- External data retrieval.
- Domain normalization.
- Telemetry simulation.
- Safety evaluation.
- Alert lifecycle.
- AI interaction.
- API delivery.
- User interface presentation.

## 6.3. Ports and Adapters (Hexagonal Architecture)

The application core must not depend directly on a specific external provider.

External integrations must communicate with the application through explicit interfaces.

Examples:

- Planetary data source ports.
- AI provider ports.
- Telemetry source ports.
- Event publishing ports.
- Cache ports.

Adapters implement these interfaces for specific providers.

The core business logic must depend on the interfaces, not on vendor-specific SDKs or response formats.

## 6.4. Design Patterns

The implementation should use the following patterns where appropriate.

| Pattern | Application |
|---|---|
| Ports and Adapters | Isolate external APIs and providers |
| Adapter | Convert source-specific responses into internal models |
| Strategy | Select different data providers or AI implementations |
| Factory | Instantiate configured providers |
| Repository | Abstract access to cached and session data |
| Observer / Publish-Subscribe | Distribute telemetry and alert events |
| Rule Engine | Evaluate deterministic operational conditions |
| Anti-Corruption Layer | Prevent external data models from contaminating the domain |
| Circuit Breaker | Protect the application from repeatedly failing external sources |
| Dependency Injection | Provide configured implementations to application services |

Patterns must be used to solve actual design problems rather than introduced as unnecessary abstraction.

## 6.5. Data Flow Architecture

The system must follow this logical organization:

```text
                    EXTERNAL INFORMATION
                              |
             +----------------+----------------+
             |                |                |
          NASA PDS          HiRISE           MEDA
             |                |                |
             +----------------+----------------+
                              |
                   SOURCE ADAPTERS
                              |
                  DATA NORMALIZATION
                              |
                  PROVENANCE VALIDATION
                              |
                       DATA CACHE
                              |
                              v
+---------------------------------------------------------+
|                   MISSION CONTEXT                       |
+---------------------------------------------------------+
                              ^
                              |
                 TELEMETRY PROCESSING
                              ^
                              |
                    SIMULATED SENSORS
                              |
                              v
                    SAFETY RULE ENGINE
                              |
                              v
                     ALERT MANAGEMENT
                              |
                              v
                   EVENT DISTRIBUTION
                              |
                 +------------+------------+
                 |                         |
                 v                         v
             ASTRONAUT HUD            AI ASSISTANT
                                           |
                                     AI PROVIDER
```

The diagram represents logical responsibilities, not mandatory deployment services.

## 6.6. Domain Independence

External data source failures must not affect the deterministic safety engine.

The AI assistant must consume contextual information but must not own or modify its underlying records.

The user interface must not contain business rules that belong to the backend.

---

# 7. Application Modules

The backend should be organized into the following logical modules.

## 7.1. Telemetry Module

Responsibilities:

- Receive simulated sensor measurements.
- Validate measurements.
- Normalize units.
- Maintain the latest telemetry state.
- Publish telemetry changes.

## 7.2. External Data Integration Module

Responsibilities:

- Manage configured external sources.
- Execute source-specific requests.
- Validate external responses.
- Normalize observations.
- Preserve provenance.
- Handle timeouts and failures.
- Manage cache policies.

This module must not contain safety rules or AI prompt logic.

## 7.3. Mission Context Module

Responsibilities:

- Maintain the current simulated mission state.
- Associate telemetry with the mission.
- Associate relevant external observations with the mission.
- Expose a consolidated read-only context.
- Track the freshness and availability of mission information.

The mission context must not merge unrelated measurement types into a single ambiguous metric.

## 7.4. Safety Module

Responsibilities:

- Define configurable rules.
- Evaluate incoming telemetry.
- Detect warning and critical conditions.
- Generate deterministic alert events.
- Prevent duplicate alert flooding.
- Maintain alert lifecycle.

## 7.5. AI Assistant Module

Responsibilities:

- Build contextual requests.
- Select the configured AI provider.
- Generate conversational responses.
- Provide source-aware explanations.
- Apply assistant restrictions.

## 7.6. Event Distribution Module

Responsibilities:

- Publish telemetry events.
- Publish alert events.
- Publish mission context changes.
- Manage client connections.
- Handle disconnections.

## 7.7. Simulation Module

Responsibilities:

- Generate repeatable simulated readings.
- Activate and deactivate scenarios.
- Produce simulated communication failures.
- Provide controlled conditions for testing.

---

# PART V — APPLICATION REQUIREMENTS

# 8. Backend Functional Requirements

## 8.1. General Requirements

The backend must expose an application interface for the HUD and external integrations.

It must provide:

- Request validation.
- Consistent response schemas.
- Centralized error handling.
- Structured logging.
- Configurable timeouts.
- Application health reporting.
- Asynchronous processing where appropriate.

## 8.2. REST API

The initial API must expose the following endpoints.

### Application and Mission

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Application health |
| GET | `/api/v1/mission` | Current mission context |
| GET | `/api/v1/mission/status` | Current mission status |

### Telemetry

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/telemetry/current` | Latest simulated telemetry |
| GET | `/api/v1/telemetry/history` | Available session telemetry history |

### Alerts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/alerts` | Active and historical alerts |
| GET | `/api/v1/alerts/{alert_id}` | Retrieve a specific alert |
| POST | `/api/v1/alerts/{alert_id}/acknowledge` | Acknowledge an alert |

Acknowledging an alert must not remove or downgrade its severity.

### Simulation

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/simulation/start` | Start telemetry simulation |
| POST | `/api/v1/simulation/stop` | Stop telemetry simulation |
| POST | `/api/v1/simulation/scenario` | Activate a demonstration scenario |
| GET | `/api/v1/simulation/status` | Retrieve simulation status |

### External Data

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/sources` | List configured external sources |
| GET | `/api/v1/sources/status` | Retrieve source availability |
| GET | `/api/v1/observations` | Retrieve available normalized observations |
| GET | `/api/v1/observations/{observation_id}` | Retrieve an observation |
| POST | `/api/v1/observations/search` | Search configured sources |
| POST | `/api/v1/observations/refresh` | Request an external data refresh |

The observation search request must use validated geographic and temporal filters supported by the selected sources.

Source-specific capabilities must not be assumed to be universal.

### AI Assistant

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/assistant/chat` | Send a message to the assistant |
| GET | `/api/v1/assistant/status` | Retrieve provider status |

## 8.3. API Response Requirements

Responses must:

- Use consistent JSON structures.
- Identify validation errors.
- Include relevant timestamps.
- Preserve source identifiers when applicable.
- Distinguish unavailable information from empty results.
- Avoid exposing credentials or internal secrets.

## 8.4. WebSocket Communication

Endpoint:

```text
/ws/telemetry
```

The WebSocket connection must distribute structured events.

Supported event types:

- `telemetry_update`
- `alert_created`
- `alert_updated`
- `mission_status_changed`
- `external_data_updated`
- `source_status_changed`
- `simulation_status_changed`

Example telemetry event:

```json
{
  "type": "telemetry_update",
  "timestamp": "2026-11-14T12:00:00Z",
  "data": {
    "oxygen_level": 85.0,
    "pressure_psi": 4.3,
    "temperature_celsius": 28.0,
    "battery_level": 62.0,
    "radiation_rate_msv_h": 0.4,
    "communication_status": "connected",
    "data_origin": "simulated_sensor"
  }
}
```

Example external data event:

```json
{
  "type": "external_data_updated",
  "timestamp": "2026-11-14T12:05:00Z",
  "data": {
    "source_id": "meda",
    "observation_id": "observation-001",
    "observation_type": "environmental_observation",
    "observed_at": "2026-11-14T12:00:00Z",
    "retrieved_at": "2026-11-14T12:05:00Z",
    "status": "available"
  }
}
```

Example alert event:

```json
{
  "type": "alert_created",
  "timestamp": "2026-11-14T12:00:00Z",
  "data": {
    "id": "alert-001",
    "severity": "warning",
    "category": "temperature",
    "message": "Temperature exceeded the configured demonstration threshold.",
    "source": "safety_rules_engine",
    "acknowledged": false
  }
}
```

The server must:

- Support multiple connected clients.
- Detect disconnections.
- Avoid allowing one client failure to interrupt the others.
- Send events using a consistent schema.
- Provide a clear reconnection strategy.

The frontend must reconnect automatically after temporary interruptions.

---

# 9. External Data Integration Requirements

## 9.1. Provider Interface

Each external data source must be integrated through a provider interface.

Conceptual example:

```python
from abc import ABC, abstractmethod


class PlanetaryDataProvider(ABC):

    @abstractmethod
    async def search_observations(
        self,
        query: dict
    ) -> list:
        pass

    @abstractmethod
    async def get_observation(
        self,
        observation_id: str
    ) -> dict:
        pass
```

The actual interface must reflect the capabilities supported by the selected source.

A provider that only supports imagery or map tiles must not be forced to implement scientific observation methods it does not support.

Use capability-specific interfaces when necessary.

## 9.2. Provider Adapters

Each source adapter must:

- Implement its documented access method.
- Construct source-specific requests.
- Validate response status and structure.
- Convert source-specific data into internal models.
- Preserve original identifiers and metadata.
- Handle unsupported queries explicitly.

Potential adapters:

```text
integrations/
├── base/
│   ├── provider.py
│   ├── registry.py
│   └── exceptions.py
├── nasa_pds/
│   ├── adapter.py
│   └── mapper.py
├── hirise/
│   ├── adapter.py
│   └── mapper.py
├── meda/
│   ├── adapter.py
│   └── mapper.py
├── themis/
│   ├── adapter.py
│   └── mapper.py
└── maps/
    ├── adapter.py
    └── mapper.py
```

This is a proposed structure. Only verified and implemented adapters should be created as functional integrations.

## 9.3. Normalized Observation Model

All external observations must be represented through a normalized internal model.

Conceptual example:

```json
{
  "id": "observation-001",
  "source": {
    "id": "nasa-pds",
    "name": "NASA Planetary Data System"
  },
  "mission": "Mars 2020",
  "instrument": "Example Instrument",
  "observation_type": "scientific_observation",
  "observed_at": "2026-11-14T12:00:00Z",
  "retrieved_at": "2026-11-14T12:05:00Z",
  "location": {
    "latitude": 0.0,
    "longitude": 0.0,
    "coordinate_reference_system": "source-defined"
  },
  "measurements": [],
  "metadata": {},
  "quality": {
    "status": "unknown",
    "uncertainty": null
  },
  "references": []
}
```

The model is illustrative.

Each source adapter must map its actual response without inventing fields or values.

## 9.4. Data Normalization Rules

Normalization must address:

- Measurement units.
- Date and time formats.
- Coordinate reference systems.
- Spatial bounds.
- Observation identifiers.
- Mission and instrument identifiers.
- Missing values.
- Quality indicators.
- Source-specific metadata.

The original source payload may be retained selectively for debugging or traceability, subject to size and licensing considerations.

## 9.5. Caching

External data must be cached when appropriate.

The cache policy must be configurable per source and data type.

The system must distinguish:

- Fresh data.
- Cached data.
- Stale data.
- Unavailable data.
- Failed retrieval.

Cache expiration must not imply that a scientific observation itself has become invalid. It only describes the freshness of the application's retrieved copy.

The application must display the observation date separately from the retrieval date.

## 9.6. Failure Handling

External integrations must implement:

- Connection timeout.
- Read timeout.
- Bounded retries.
- Exponential backoff where appropriate.
- Circuit breaker behavior for repeated failures.
- Structured error reporting.
- Graceful degradation.

A failed external source must not prevent other sources from operating.

A failed external request must not stop the telemetry simulator or safety rules engine.

## 9.7. Source Health

Each source must expose an operational status.

Suggested states:

- `available`
- `degraded`
- `unavailable`
- `not_configured`
- `unknown`

A source health status must not be confused with the scientific validity of its observations.

---

# 10. Mission Context and Data Correlation

## 10.1. Mission Context

The mission context is the consolidated information model used by the assistant and HUD.

It may include:

- Mission identification.
- Planetary body.
- Simulated astronaut location.
- Current telemetry.
- Active alerts.
- Recent operational events.
- Relevant external observations.
- Source availability.
- Observation freshness.

## 10.2. Spatial Correlation

External observations may be associated with a mission region when sufficient spatial metadata exists.

The system must:

1. Identify the observation coordinates or spatial bounds.
2. Identify the mission's current simulated location or region.
3. Verify coordinate reference compatibility.
4. Apply a configured spatial matching method.
5. Record the matching criteria.
6. Expose the association as contextual information, not as a definitive scientific conclusion.

The system must not infer proximity or spatial relevance when coordinates are missing or incompatible.

## 10.3. Temporal Correlation

The system may compare observation times with mission events.

However:

- Historical observations must remain identified as historical.
- The system must not imply simultaneous measurements when timestamps differ.
- Missing timestamps must be explicitly identified.
- Time-zone conversion must be consistent.

## 10.4. Contextual Relevance

Not every retrieved scientific record is relevant to the current mission.

The system should support filters such as:

- Geographic region.
- Observation date.
- Instrument.
- Data type.
- Mission.
- Source.
- Spatial relevance.

The initial release should use transparent and deterministic filtering rules.

AI-generated relevance assessments must be identified as interpretations, not source-provided facts.

---

# PART VI — TELEMETRY AND SAFETY

# 11. Telemetry Simulation

## 11.1. Simulation Behavior

The simulator must generate readings at a configurable interval.

Default interval:

```text
1 second
```

Initial parameters:

- Oxygen availability.
- Pressure.
- Suit temperature.
- Battery level.
- Radiation rate.
- Astronaut position.
- Communication status.

All generated measurements must be identified as simulated.

## 11.2. Demonstration Scenarios

The simulator must support:

- Normal operation.
- High temperature.
- Low oxygen.
- Low battery.
- Pressure anomaly.
- Radiation warning.
- Communication interruption.

Scenarios must be reproducible enough for automated tests and demonstrations.

## 11.3. Scenario Activation

Example:

```json
{
  "scenario": "high_temperature"
}
```

The scenario must modify the simulated telemetry and allow the safety engine to evaluate the resulting readings.

Scenarios must be activated and deactivated without restarting the backend.

## 11.4. Future Telemetry Sources

The telemetry architecture should support future adapters for:

- Physical sensors.
- Hardware simulators.
- External telemetry feeds.
- Recorded test datasets.

These are extension points only. They are not part of the initial implementation.

---

# 12. Safety Rules Engine

## 12.1. Deterministic Evaluation

The safety engine must be deterministic and independent of the AI model.

Each rule must define:

- Unique rule identifier.
- Parameter.
- Comparison operator.
- Demonstration threshold.
- Severity.
- Message template.
- Evaluation conditions.
- Cooldown or deduplication policy.
- Optional recovery condition.

## 12.2. Alert Severity

Initial severities:

- `INFO`
- `WARNING`
- `CRITICAL`

The HUD must visually distinguish these levels.

Critical alerts must remain visible and must not depend on AI availability.

## 12.3. Alert Lifecycle

An alert may have the following states:

- Active.
- Acknowledged.
- Resolved.

Acknowledgment does not mean resolution.

Resolution must occur only when the corresponding rule's recovery condition is satisfied or when an explicitly defined application workflow resolves the alert.

The AI assistant must not change alert lifecycle states.

## 12.4. Deduplication

Repeated readings that satisfy the same rule must not create uncontrolled alert flooding.

The system must identify equivalent active alerts and apply the configured cooldown policy.

New alerts may be generated when:

- A previous alert has been resolved.
- A defined cooldown has expired and a new notification is justified.
- The condition has materially changed according to the rule definition.

## 12.5. Safety Boundary

All thresholds are illustrative demonstration values.

They are not NASA-approved operational limits and must never be presented as certified astronaut safety parameters.

The system is not a certified safety system.

No AI-generated answer may replace validated operational procedures.

---

# PART VII — AI ASSISTANT

# 13. AI Assistant Architecture

## 13.1. Provider Independence

The assistant must use a provider abstraction.

Conceptual interface:

```python
from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    async def generate_response(
        self,
        message: str,
        context: dict
    ) -> str:
        pass
```

Initial implementation:

- Mock provider.
- Provider configuration.
- Context builder.
- Assistant service.

A real provider adapter may be added later.

The application must start and remain functional without an external AI API key.

## 13.2. Context Builder

The context builder is responsible for selecting relevant information before it is passed to the AI provider.

Potential context:

- Current simulated telemetry.
- Active alerts.
- Mission status.
- Recent mission events.
- Relevant external scientific observations.
- Data-source status.
- Observation timestamps.
- Source references.
- Data freshness indicators.

The context builder must avoid passing unnecessary or excessively large raw datasets.

## 13.3. Assistant Responsibilities

The assistant may:

- Explain telemetry readings.
- Explain active alerts.
- Summarize the simulated mission state.
- Explain relevant planetary observations.
- Identify the source and date of external information.
- Compare available observations when the data supports comparison.
- Identify uncertainty and missing information.
- Answer general questions related to the available mission context.

## 13.4. Assistant Restrictions

The assistant must:

- Never create or modify safety alerts.
- Never suppress or downgrade a critical alert.
- Never invent sensor readings.
- Never invent scientific observations.
- Never claim that external data is current when it is historical or stale.
- Never present simulated data as real astronaut measurements.
- Never present historical rover observations as live suit telemetry.
- Never invent NASA procedures.
- Never autonomously control equipment.
- Clearly identify uncertainty.
- Refer users to validated procedures when appropriate.

## 13.5. Source-Aware Responses

When an answer relies on external scientific information, the assistant should identify:

- Source.
- Mission or instrument.
- Observation date.
- Retrieval date when relevant.
- Source reference.
- Limitations or uncertainty.

The assistant must distinguish between source facts and its own interpretation.

---

# PART VIII — FRONTEND AND USER EXPERIENCE

# 14. Helmet HUD Interface

## 14.1. Interface Concept

The interface should resemble a professional astronaut helmet HUD.

Visual direction:

- Dark background.
- High-contrast information.
- Cyan and blue informational elements.
- Amber warnings.
- Red critical alerts.
- Clear typography.
- Minimal visual clutter.
- Responsive layout.

Readability and information hierarchy must take precedence over decoration.

## 14.2. Main Dashboard

The initial dashboard must include:

1. Mission identification.
2. Mission status.
3. Astronaut and suit telemetry.
4. Active alert panel.
5. WebSocket connection indicator.
6. AI assistant panel.
7. Simulation controls.
8. External data source status.
9. Planetary environmental context.
10. Observation provenance and freshness.
11. Geographic or image context when supported.

## 14.3. Information Separation

The interface must visually distinguish:

### Suit Telemetry

Examples:

- Oxygen.
- Pressure.
- Temperature.
- Battery.
- Radiation rate.
- Communication status.

### Planetary Context

Examples:

- Surface imagery.
- Terrain information.
- Scientific observations.
- Environmental measurements from robotic missions.
- Geographic references.

External scientific observations must never be presented in a way that makes them appear to be live suit sensor readings.

## 14.4. Data Freshness Indicators

External information must display an appropriate freshness status.

Suggested labels:

- LIVE — only when the source genuinely provides live information.
- RECENT — according to a source-specific freshness policy.
- HISTORICAL — for historical observations.
- CACHED — for previously retrieved information.
- STALE — when the configured freshness limit has been exceeded.
- UNAVAILABLE — when retrieval is not possible.

The application must not use LIVE as a generic label for recently downloaded data.

## 14.5. Suggested Frontend Components

- MissionStatus.
- TelemetryCard.
- AlertPanel.
- AssistantPanel.
- SimulationControls.
- DataSourceStatus.
- EnvironmentalContextPanel.
- ObservationCard.
- MapPanel.
- ConnectionIndicator.

Components must receive normalized data through application state and service interfaces.

---

# PART IX — TECHNICAL IMPLEMENTATION GUIDELINES

# 15. Proposed Application Structure

The implementation should follow a modular organization similar to the following.

```text
space-guard-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── websocket/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   ├── domain/
│   │   │   ├── telemetry/
│   │   │   ├── mission/
│   │   │   ├── observations/
│   │   │   ├── alerts/
│   │   │   └── assistant/
│   │   ├── application/
│   │   │   ├── services/
│   │   │   └── context/
│   │   ├── integrations/
│   │   │   ├── base/
│   │   │   ├── nasa_pds/
│   │   │   ├── hirise/
│   │   │   ├── meda/
│   │   │   ├── themis/
│   │   │   └── maps/
│   │   ├── infrastructure/
│   │   │   ├── cache/
│   │   │   ├── events/
│   │   │   └── repositories/
│   │   ├── sensors/
│   │   ├── safety/
│   │   └── agent/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── contract/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── views/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   └── router/
│   ├── tests/
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
├── docs/
│   ├── SPECIFICATION.md
│   ├── ARCHITECTURE.md
│   ├── BUSINESS_RULES.md
│   ├── DATA_SOURCES.md
│   ├── DATA_PROVENANCE.md
│   ├── API.md
│   ├── WEBSOCKET.md
│   ├── TELEMETRY.md
│   ├── SAFETY_RULES.md
│   ├── AI_INTEGRATION.md
│   ├── DOCKER.md
│   ├── DEVELOPMENT.md
│   ├── TESTING.md
│   └── LIMITATIONS.md
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

This is a proposed logical structure. The implementation may adjust file placement while preserving module boundaries and responsibilities.

## 15.1. Configuration

Configuration must be centralized and environment-driven.

External data source settings must not be hardcoded into business services.

Provider-specific configuration must be isolated.

Secrets must never be committed to version control.

## 15.2. Database Strategy

The first release should avoid introducing a database unless persistence is justified by an explicit requirement.

The initial prototype may use in-memory state and a configurable cache.

The implementation must clearly document that telemetry history, alert history, and cached observations may be lost when the application restarts.

A future persistent storage layer should be introduced through repository interfaces.

---

# 16. Environment Configuration

Create:

```text
.env.example
```

Initial configuration:

```env
APP_NAME=SPACE GUARD AI
APP_ENV=development
APP_DEBUG=true

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

FRONTEND_PORT=5173

TELEMETRY_INTERVAL_SECONDS=1

AI_PROVIDER=mock
AI_API_KEY=
AI_MODEL=

EXTERNAL_DATA_ENABLED=true
EXTERNAL_DATA_TIMEOUT_SECONDS=15
EXTERNAL_DATA_CACHE_TTL_SECONDS=3600

NASA_PDS_ENABLED=false
HIRISE_ENABLED=false
MEDA_ENABLED=false
THEMIS_ENABLED=false
MARS_MAPS_ENABLED=false
```

These flags must be enabled only when the corresponding integration has been verified and implemented.

Public data access must not be assumed to require authentication. Authentication and API-key requirements must be established individually for each provider.

---

# PART X — TESTING AND QUALITY ASSURANCE

# 17. Testing Requirements

## 17.1. Backend Unit Tests

Test:

- Telemetry validation.
- Unit normalization.
- Simulator behavior.
- Scenario activation.
- Safety rule evaluation.
- Alert generation.
- Alert deduplication.
- Alert lifecycle.
- Observation normalization.
- Provenance preservation.
- Mission context construction.
- Mock AI responses.

## 17.2. External Integration Tests

Each implemented source adapter must be tested for:

- Request construction.
- Response validation.
- Mapping to internal models.
- Missing metadata.
- Unsupported query parameters.
- Timeout behavior.
- HTTP errors.
- Invalid payloads.
- Retry behavior.
- Source attribution.

Use mocked HTTP responses for deterministic automated tests.

Live external API tests should be separate from the normal unit test suite to avoid making ordinary builds dependent on network availability.

## 17.3. Contract Tests

Contract tests must verify that each provider adapter conforms to its declared interface and returns valid internal models.

The tests must identify unsupported capabilities explicitly.

## 17.4. Frontend Tests

Test:

- Dashboard rendering.
- Telemetry presentation.
- Alert severity presentation.
- Source status presentation.
- Observation freshness labels.
- Source attribution.
- WebSocket connection state.
- Assistant interaction.
- Simulation controls.
- Graceful handling of unavailable external data.

## ## Visual Identity and Design Principles

### 1. Design Philosophy

SPACE GUARD AI must adopt a minimalist, functional, and information-oriented visual identity inspired by the visual language of NASA and the Jet Propulsion Laboratory (JPL).

The interface must prioritize operational clarity, readability, consistency, and efficient information recognition.

The design must avoid unnecessary visual elements, excessive decoration, visual noise, and complex interface patterns.

The application should feel like a professional aerospace monitoring interface rather than a conventional administration dashboard.

### 2. Global Typography

Clarity City must be the primary typeface throughout the entire application.

Google Sans must be configured as the secondary fallback typeface, followed by the generic sans-serif family.

The typography must be applied globally, including:

- Page titles and section headings.
- Navigation and interface labels.
- Telemetry values and measurements.
- Alert messages and descriptions.
- Buttons and form controls.
- AI assistant messages.
- Simulation controls.
- Dialogs, tooltips, and notifications.

The font configuration must use the following Google Fonts import:

```css
@import url('https://fonts.googleapis.com/css2?family=Clarity+City:ital,wght@0,500;1,500&family=Google+Sans:ital,opsz,wght@0,17..18,400..700;1,17..18,400..700&display=swap');
```

Global typography configuration:

```css
:root {
  font-family: "Clarity City", "Google Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
}

body,
button,
input,
textarea,
select {
  font-family: inherit;
}
```

The typography must be centralized in the global stylesheet. Individual components must not introduce unrelated font families.

## Primary Visual Identity and User Experience Reference

The official Jet Propulsion Laboratory (JPL) website (https://www.jpl.nasa.gov/) is the primary visual identity and user experience reference for SPACE GUARD AI.

This reference must guide the entire application, not just the landing page or dashboard.

The implementation should study and adapt the JPL website's:
- Visual identity and graphic language.
- Typography and typographic hierarchy.
- Navigation structure and information architecture.
- Layout composition, spacing, and alignment.
- Content organization and component consistency.
- Use of imagery, colors, and visual emphasis.

### Adaptation Principles

SPACE GUARD AI must translate the JPL visual language into a minimalist, scientific, and operational interface suitable for an astronaut helmet monitoring system.

The application must retain its own identity and must not become a direct copy of the JPL website.

The interface should prioritize:
- Mission status and operational context.
- Real-time simulated telemetry.
- Deterministic safety alerts.
- Assistant interaction.
- Clear and intuitive navigation.
- Readability and accessibility.

### Typography

Use Clarity City (weight 500) as the primary font throughout the entire application.

Use Google Sans (variable weights 400–700) as the secondary font and fallback, followed by a generic sans-serif fallback.

Typography must be centralized through global styles and applied consistently to all interface components.

### Design Constraints

- Avoid excessive gradients, glow effects, decorative animations, and unnecessary shadows.
- Avoid visual clutter and excessive card nesting.
- Use restrained colors and consistent spacing.
- Reserve semantic colors for operational states and alerts.
- Maintain responsive behavior and accessible contrast.
- Do not use NASA or JPL logos, trademarks, or visual assets in a way that implies official affiliation or endorsement.

### Implementation Requirement

Before modifying the interface, inspect the existing frontend architecture, global styles, components, and navigation.

Refactor the existing interface to follow this visual direction consistently. Do not limit the changes to the homepage or introduce an unrelated design system.

The JPL website is the primary design reference; SPACE GUARD AI's operational requirements remain the authority for interface behavior and information hierarchy.

### 3. Minimalist Interface

The interface must follow these principles:

- Dark, neutral background.
- Restrained use of color.
- Clear information hierarchy.
- Consistent spacing.
- Minimal borders and shadows.
- Simple geometric shapes.
- Subtle separators.
- Limited use of rounded corners.
- No unnecessary gradients, glow effects, or animations.
- No decorative elements that compete with operational information.

### 4. Color and Information Hierarchy

Colors must communicate operational meaning rather than serve as decoration.

- Neutral tones: background, surfaces, and secondary information.
- Cyan or blue: informational elements and normal telemetry.
- Amber: warning conditions.
- Red: critical alerts.
- Green: normal operational status, when appropriate.

Critical alerts must remain visually prominent regardless of the interface theme.

### 5. Telemetry Presentation

Telemetry must be presented with emphasis on the measured value, followed by its unit and a concise parameter label.

Sensor origin and simulation status must be identifiable without dominating the interface.

Avoid excessive icons, illustrations, and ornamental graphics.

### 6. Responsive and Accessible Design

The interface must remain readable across desktop, tablet, and mobile resolutions.

Maintain sufficient text contrast, visible focus states, keyboard accessibility, and appropriate font sizes.

The design reference is the visual simplicity and technical clarity of NASA/JPL interfaces. The application must not imply official NASA affiliation or reproduce protected NASA branding.

## 17.5. Integration Tests

Test:

- Backend startup.
- Frontend-to-backend communication.
- WebSocket event delivery.
- Scenario activation.
- Alert propagation.
- External data normalization.
- Mission context updates.
- AI context construction.
- External source failure isolation.
- AI provider failure isolation.

## 17.6. Critical Reliability Tests

The following conditions must be verified:

1. A failed external source does not stop telemetry processing.
2. A failed AI provider does not stop safety evaluation.
3. A critical alert is still generated when the AI provider is unavailable.
4. Historical external observations are not labeled as live.
5. Missing source metadata is not fabricated.
6. An AI response cannot change alert severity.
7. Invalid external responses do not contaminate the mission context.

---

# PART XI — EXECUTION AND DEPLOYMENT

# 18. Execution Requirements

The application must support local development and Docker-based execution.

The initial deployment must contain:

- Backend application.
- Frontend application.
- Internal service networking.
- Environment configuration.
- Health checks where practical.
- Source-code mounting for development where appropriate.

No additional microservices should be introduced without a clear business or operational justification.

## 18.1. Docker Networking

The frontend must communicate with the backend through an appropriate development proxy or service networking configuration.

The browser must not attempt to use `localhost:8000` from inside the frontend container as a reference to the backend container.

A recommended development configuration is:

- Browser accesses the frontend through `localhost:5173`.
- Vite proxies `/api` to `http://backend:8000`.
- Vite proxies `/ws` to `ws://backend:8000`.
- The backend remains reachable through the Docker network.

The actual proxy and URL configuration must be consistent across REST and WebSocket communication.

## 18.2. Initial Ports

| Service | Host port |
|---|---|
| Backend API | 8000 |
| Frontend | 5173 |

## 18.3. Docker Commands

From the repository root:

```powershell
docker compose config

docker compose up --build
```

Detached execution:

```powershell
docker compose up --build -d
```

Inspect services:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs -f
```

Stop services:

```powershell
docker compose down
```

---

# PART XII — DOCUMENTATION

# 19. Documentation Requirements

All project documentation must be written in English.

Required files:

```text
README.md

docs/
├── SPECIFICATION.md
├── ARCHITECTURE.md
├── BUSINESS_RULES.md
├── DATA_SOURCES.md
├── DATA_PROVENANCE.md
├── API.md
├── WEBSOCKET.md
├── TELEMETRY.md
├── SAFETY_RULES.md
├── AI_INTEGRATION.md
├── DOCKER.md
├── DEVELOPMENT.md
├── TESTING.md
└── LIMITATIONS.md
```

Documentation must explain:

- Product purpose.
- Business domains.
- Business rules.
- Architectural principles.
- Design patterns.
- External data sources.
- Verified source access methods.
- Provider adapters.
- Data normalization.
- Data provenance.
- Mission context.
- Telemetry simulation.
- Safety rules.
- Alert lifecycle.
- AI integration.
- API endpoints.
- WebSocket events.
- Environment variables.
- Installation.
- Docker execution.
- Testing.
- Known limitations.

The documentation must clearly distinguish:

- Proposed integrations.
- Verified integrations.
- Implemented integrations.
- Tested integrations.

A source must not be documented as operational merely because it appears in the candidate source catalogue.

---

# PART XIII — ACCEPTANCE CRITERIA

# 20. Initial Release Acceptance Criteria

The first release is considered operational when:

1. The backend starts successfully.
2. The frontend starts successfully.
3. Docker Compose starts the application.
4. Simulated telemetry is displayed in the HUD.
5. Telemetry is distributed through WebSockets.
6. Demonstration scenarios can be activated.
7. The deterministic safety engine generates alerts.
8. Alerts appear in the HUD.
9. The mock AI assistant responds to questions.
10. Mission context is constructed from available information.
11. At least one public planetary data source has been integrated through a verified programmatic access method.
12. The source adapter normalizes its response into the internal observation model.
13. Observation provenance is preserved.
14. External data is visibly distinguished from suit telemetry.
15. Source failure does not interrupt telemetry or safety evaluation.
16. Historical data is not presented as live information.
17. Automated tests cover the implemented domains.
18. All required documentation is available in English.
19. The application works without an external AI API key.
20. The implementation does not claim certified astronaut safety functionality.

## 20.1. Integration Acceptance Criteria

For each external source claimed as integrated:

- Its access method must be documented.
- Its actual endpoint or resource must be verified.
- Its request and response format must be tested.
- Its data must be normalized.
- Its provenance must be preserved.
- Its failure behavior must be tested.
- Its status must be represented in the application.

---

# PART XIV — DEVELOPMENT PRINCIPLES AND LIMITATIONS

# 21. Engineering Principles

The implementation must follow:

- Separation of concerns.
- Modular architecture.
- Explicit business rules.
- Ports and Adapters.
- Provider independence.
- Typed internal models.
- Centralized configuration.
- Explicit data provenance.
- Deterministic safety evaluation.
- Graceful degradation.
- Asynchronous external requests where appropriate.
- Automated tests.
- Reproducible execution.
- English-language documentation.

Avoid:

- Unnecessary microservices.
- Unnecessary abstraction.
- Direct coupling to vendor-specific APIs.
- AI-dependent safety decisions.
- Fabricated scientific observations.
- Mixing historical observations with live measurements.
- Unverified external endpoints.
- Hardcoded credentials.
- Unjustified database dependencies.

# 22. Known Limitations

The initial release is a demonstration prototype.

Its limitations include:

- Simulated suit telemetry.
- Non-certified demonstration thresholds.
- Limited external data integrations.
- Potentially historical scientific observations.
- External source availability and latency.
- In-memory application state unless persistence is explicitly implemented.
- AI provider variability.
- No physical astronaut equipment integration.
- No operational safety certification.

The product must communicate these limitations clearly.

---

# PART XV — IMPLEMENTATION PRIORITIES

# 23. Development Phases

Implementation should follow these phases.

| Phase | Objective | Main deliverable |
|---|---|---|
| 1 | Domain and application foundation | Project structure and core models |
| 2 | Telemetry and simulation | Working simulated telemetry |
| 3 | Safety and alerts | Deterministic rule engine |
| 4 | External integration foundation | Source registry and provider interfaces |
| 5 | First planetary data integration | One verified external source |
| 6 | Data normalization and provenance | Internal observation model |
| 7 | Mission context | Consolidated contextual information |
| 8 | WebSocket distribution | Real-time event communication |
| 9 | AI assistant | Context-aware mock assistant |
| 10 | HUD interface | Integrated monitoring dashboard |
| 11 | Docker and integration | Reproducible end-to-end execution |
| 12 | Testing and documentation | Validated initial release |

The team should prioritize a working end-to-end vertical slice rather than implementing numerous external integrations simultaneously.

---

# 24. Final Product Definition

SPACE GUARD AI is an intelligent mission-support prototype that combines simulated astronaut suit telemetry with publicly available planetary scientific information.

Its architecture separates operational monitoring, external data retrieval, mission context, deterministic safety evaluation, and conversational assistance.

The system's central value is the ability to transform heterogeneous information into a contextual and understandable interface while maintaining strict boundaries between measurements, observations, derived information, and AI-generated interpretations.

**End of Specification.**

---

# CODEX IMPLEMENTATION PROMPT

## SPACE GUARD AI — Architecture, Business Rules and Implementation

You are a senior software architect and full-stack engineer responsible for implementing SPACE GUARD AI.

Your task is to inspect the existing repository and incrementally implement the system according to `docs/SPECIFICATION.md`.

The project is being developed on Windows using Visual Studio Code, PowerShell, and Docker Desktop.

The specification is the source of truth for product behavior and architectural decisions.

Do not prioritize technology selection over business requirements and domain boundaries.

---

## 1. Primary Objective

Build a functional prototype of an intelligent astronaut helmet assistant.

The system must combine two independent information domains:

1. Simulated astronaut and suit telemetry.
2. Public planetary scientific and environmental information.

It must normalize and contextualize information from these domains, evaluate operational conditions through deterministic rules, distribute events, and provide contextual assistance through an AI provider abstraction.

The system must not claim physical helmet integration or certified astronaut safety functionality.

---

## 2. Repository Inspection

Before changing any files:

1. Inspect the repository structure.
2. Read `docs/SPECIFICATION.md` completely.
3. Inspect existing source code and configuration.
4. Identify implemented and missing functionality.
5. Preserve valid existing work.
6. Identify dependencies and architectural inconsistencies.
7. Check whether any external integrations already exist.
8. Report the repository's current state.
9. Propose an incremental implementation plan.

Do not overwrite existing files without understanding their purpose.

Do not assume that an existing feature works merely because a corresponding file exists.

---

## 3. Architecture Requirements

Use a modular monolithic architecture.

Separate business domains and application responsibilities.

The system must follow the principles of:

- Separation of concerns.
- Ports and Adapters.
- Dependency inversion.
- Provider independence.
- Explicit domain models.
- Deterministic business rules.
- Data provenance.
- Graceful degradation.

Use design patterns only where they provide a clear architectural benefit.

The application core must not depend directly on external NASA API response formats or AI provider SDKs.

---

## 4. Business Domain Implementation

Implement the following logical domains:

### A. Telemetry Domain

Responsible for simulated astronaut and suit readings.

### B. External Data Domain

Responsible for retrieving and normalizing public planetary observations.

### C. Mission Context Domain

Responsible for consolidating relevant mission information without merging incompatible measurements.

### D. Safety Domain

Responsible for deterministic rule evaluation and alert generation.

### E. AI Assistance Domain

Responsible for contextual conversational responses.

### F. Event Distribution Domain

Responsible for distributing telemetry, alerts, and mission events.

Each domain must have clear responsibilities and explicit interfaces.

---

## 5. External Data Integration

External planetary data integration is a core requirement, not an optional decorative feature.

However, do not implement unverified APIs or assume that every NASA resource exposes a REST endpoint.

### 5.1. Candidate Sources

Investigate the programmatic access methods of:

- NASA Planetary Data System.
- HiRISE.
- CTX.
- CRISM.
- THEMIS.
- TES.
- MEDA.
- Mars Trek and supported map services.
- USGS Astrogeology.
- JMARS, where documented programmatic access is available.

### 5.2. Source Verification

Before implementing an adapter:

1. Identify the official source.
2. Locate its official documentation.
3. Verify its access method.
4. Verify the actual endpoint or resource.
5. Identify authentication requirements.
6. Identify request parameters.
7. Identify response formats.
8. Identify coordinate systems and measurement units.
9. Identify source attribution requirements.
10. Identify rate limits and usage policies where documented.

Do not fabricate endpoints.

Do not rely on undocumented interfaces or fragile scraping.

If an integration cannot be verified, document the blocker and leave it as a proposed integration.

### 5.3. Provider Interfaces

Implement provider interfaces that isolate external source behavior.

Use adapters to transform source-specific responses into internal observation models.

Do not force all sources into one interface if their capabilities differ.

For example, imagery providers and scientific observation providers may require separate capability interfaces.

### 5.4. Initial Integration Strategy

Do not implement every candidate source at once.

Prioritize one geospatial or imagery integration and one scientific observation integration when their access methods are verified.

If implementation time is limited, deliver one fully functional source integration first.

### 5.5. Data Normalization

Every external observation must preserve:

- Source identifier.
- Source name.
- Mission.
- Instrument, when available.
- Observation identifier.
- Observation timestamp.
- Retrieval timestamp.
- Measurement units.
- Coordinates and coordinate reference system, when available.
- Original source reference.
- Quality indicators and uncertainty, when available.

Do not invent missing fields.

### 5.6. External Data Failure Isolation

External API failures must never stop:

- Telemetry simulation.
- Safety rule evaluation.
- Alert generation.
- WebSocket operation.

Implement appropriate timeouts, bounded retries, error handling, caching, and circuit breaker behavior where justified.

---

## 6. Mission Context

Implement a mission context service that consolidates:

- Current simulated telemetry.
- Active alerts.
- Mission status.
- Relevant external observations.
- Source availability.
- Observation freshness.
- Recent operational events.

Do not merge external scientific observations with suit sensor readings.

Do not treat historical rover measurements as current astronaut measurements.

The mission context must be read-only from the AI assistant's perspective.

---

## 7. Telemetry Simulator

Implement a background simulator.

Generate readings every second by default.

Support:

- Normal operation.
- High temperature.
- Low oxygen.
- Low battery.
- Pressure anomaly.
- Radiation warning.
- Communication interruption.

The simulator must support scenario activation and deactivation without restarting the backend.

All readings must be identified as simulated.

Make scenarios deterministic enough for testing.

---

## 8. Deterministic Safety Rules

Implement the safety engine independently from the AI assistant.

Each rule must define:

- Rule identifier.
- Parameter.
- Comparison operator.
- Demonstration threshold.
- Severity.
- Message.
- Cooldown.
- Deduplication behavior.
- Recovery condition where applicable.

Support:

- INFO.
- WARNING.
- CRITICAL.

The AI must never create, suppress, downgrade, or override critical alerts.

All thresholds must be clearly documented as illustrative demonstration values.

---

## 9. Alert Management

Implement:

- Alert creation.
- Alert identifiers.
- Severity.
- Category.
- Timestamp.
- Acknowledgment.
- Resolution.
- Deduplication.
- Alert event distribution.

Acknowledgment must not resolve an alert.

The AI assistant must not modify alert state.

---

## 10. AI Assistant

Implement a provider-independent architecture.

Start with a mock provider.

The assistant must receive a structured context containing relevant:

- Telemetry.
- Active alerts.
- Mission status.
- External observations.
- Source attribution.
- Observation timestamps.
- Freshness information.

The assistant must:

- Explain telemetry.
- Explain alerts.
- Summarize mission context.
- Explain available planetary observations.
- Identify missing information.
- Distinguish facts from interpretations.

It must not invent data or operational procedures.

The application must start without an AI API key.

Do not select a paid provider without explicit approval.

---

## 11. API and WebSocket

Implement the endpoints documented in `docs/SPECIFICATION.md`.

Use consistent schemas and validation.

Implement:

`/ws/telemetry`

Support the documented event types:

- `telemetry_update`
- `alert_created`
- `alert_updated`
- `mission_status_changed`
- `external_data_updated`
- `source_status_changed`
- `simulation_status_changed`

Implement connection handling and frontend reconnection.

Do not expose secrets or source credentials in events.

---

## 12. Frontend

Build a professional astronaut helmet HUD.

The dashboard must include:

- Mission status.
- Suit telemetry.
- Active alerts.
- Connection status.
- AI assistant.
- Simulation controls.
- External data source status.
- Planetary context.
- Observation freshness.
- Source attribution.
- Map or imagery visualization when supported.

Clearly distinguish suit telemetry from external scientific observations.

Do not display historical data as live.

Prioritize readability and critical information hierarchy.

---

## 13. Docker

Implement:

- Backend Dockerfile.
- Frontend Dockerfile.
- Docker Compose.
- `.dockerignore`.
- Environment configuration.

Ensure that the frontend can reach the backend through Docker networking.

Use a development proxy for REST and WebSocket requests when appropriate.

The project must start with:

```powershell
docker compose up --build
```

---

## 14. Testing

Create automated tests for:

### Business Rules
- Domain separation.
- Alert generation.
- Alert deduplication.
- Alert lifecycle.
- AI restrictions.

### Telemetry
- Validation.
- Normalization.
- Simulation scenarios.

### External Data
- Provider contracts.
- Request construction.
- Response normalization.
- Provenance preservation.
- Missing metadata.
- Timeouts.
- Source failures.
- Cache behavior.

### Mission Context
- Context construction.
- Spatial matching.
- Temporal matching.
- Data freshness.

### Integration
- API behavior.
- WebSocket communication.
- External source failure isolation.
- AI provider failure isolation.
- End-to-end scenario execution.

Use mocked HTTP responses for ordinary automated tests.

Do not make the normal unit test suite depend on live external APIs.

---

## 15. Documentation

All documentation must be written in English.

Create and maintain:

- `README.md`
- `docs/SPECIFICATION.md`
- `docs/ARCHITECTURE.md`
- `docs/BUSINESS_RULES.md`
- `docs/DATA_SOURCES.md`
- `docs/DATA_PROVENANCE.md`
- `docs/API.md`
- `docs/WEBSOCKET.md`
- `docs/TELEMETRY.md`
- `docs/SAFETY_RULES.md`
- `docs/AI_INTEGRATION.md`
- `docs/DOCKER.md`
- `docs/DEVELOPMENT.md`
- `docs/TESTING.md`
- `docs/LIMITATIONS.md`

Documentation must identify each external source as one of:

- Proposed.
- Investigated.
- Verified.
- Implemented.
- Tested.

Never claim an integration is operational if it has not been implemented and tested.

---

## 16. Engineering Constraints

Follow these restrictions:

- Do not introduce n8n.
- Do not introduce unnecessary microservices.
- Do not introduce a database without justification and approval.
- Do not introduce a mandatory paid AI dependency.
- Do not hardcode secrets.
- Do not invent NASA endpoints.
- Do not fabricate scientific observations.
- Do not mix historical planetary data with live telemetry.
- Do not treat simulated values as real astronaut measurements.
- Do not present demonstration thresholds as certified safety limits.
- Do not allow the AI assistant to override critical alerts.
- Do not claim physical helmet integration.
- Do not claim NASA endorsement or certification.

---

## 17. Incremental Implementation Workflow

Work in the following order.

### Phase 1 — Repository and Domain Foundation
- Inspect repository.
- Define domain models.
- Define business rules.
- Establish module boundaries.
- Implement centralized configuration.

### Phase 2 — Telemetry and Simulation
- Implement simulated sensors.
- Implement telemetry validation.
- Implement scenario management.

### Phase 3 — Safety and Alerts
- Implement deterministic rules.
- Implement alert lifecycle.
- Implement deduplication.

### Phase 4 — External Integration Foundation
- Investigate official source documentation.
- Define source registry.
- Define provider interfaces.
- Define normalized observation models.
- Define error handling and caching.

### Phase 5 — First External Integration
- Select a source with verified programmatic access.
- Implement its adapter.
- Validate its response.
- Normalize its observations.
- Preserve provenance.
- Write contract and integration tests.

### Phase 6 — Mission Context
- Consolidate telemetry.
- Associate relevant external observations.
- Apply freshness and provenance rules.

### Phase 7 — Event Distribution
- Implement WebSocket events.
- Implement reconnection handling.

### Phase 8 — AI Assistant
- Implement context builder.
- Implement mock provider.
- Implement source-aware responses.

### Phase 9 — HUD
- Implement dashboard.
- Implement telemetry and alert presentation.
- Implement external data context.
- Implement simulation controls.

### Phase 10 — Docker and Integration
- Configure containers.
- Configure networking.
- Validate end-to-end operation.

### Phase 11 — Testing and Documentation
- Run automated tests.
- Fix implementation errors.
- Verify source integrations.
- Review documentation.

After each phase:

1. Inspect modified files.
2. Run relevant tests.
3. Fix errors.
4. Update documentation.
5. Report what was implemented.
6. Identify what remains incomplete.

Do not proceed as if a phase were complete when its acceptance criteria have not been met.

---

## 18. Final Delivery

At the end, provide:

- Implemented business domains.
- Implemented architecture and design patterns.
- Project directory tree.
- Verified external data sources.
- Implemented external source adapters.
- Data normalization and provenance behavior.
- API endpoint list.
- WebSocket event documentation.
- Safety rule behavior.
- AI assistant behavior.
- Installation instructions.
- PowerShell execution commands.
- Docker execution commands.
- Automated test results.
- Known limitations.
- Remaining tasks.

For every external source, explicitly report whether it was investigated, verified, implemented, and tested.

Do not claim success without execution evidence.

Start by inspecting the repository and reporting the implementation plan.

Do not stop after generating directories or placeholder files. Implement and validate a working end-to-end prototype incrementally.