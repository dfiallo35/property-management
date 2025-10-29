# Technical Requirements Based on Clean Architecture

---

## 1. General Architecture

### Main Layers
- **Domain:** Contains entities, use cases, and business rules.
- **Application:** Defines use cases and orchestrates workflows.
- **Infrastructure:** Implements technical details (databases, APIs, file storage).
- **User Interface:** Presentation layer (REST API, CLI, or UI).

### Key Principles
- **Framework Independence:** The domain and application layers do not depend on external libraries.
- **Testability:** Each layer should be testable in isolation.
- **Dependency Injection:** Used to decouple components.

---

## 2. Property Module

### Domain Entities

#### Property
- `id`: UUID
- `property_type`: Enum (configurable via settings)
- `room_count`: int
- `bathroom_count`: int
- `additional_features`: List[Enum] (configurable via settings)
- `location`: `Location` (separate entity)
- `rent_value`: Decimal

#### Location
- `address`: str
- `latitude`: float (optional)
- `longitude`: float (optional)

### Use Cases

#### RegisterPropertyUseCase
- Validates input data.
- Persists the property in the database.
- Returns the ID of the created property.

#### ConfigurePropertyOptionsUseCase
- Allows adding/editing property types and additional features via settings.

### Infrastructure

#### Property Repository
- **Interface:** `PropertyRepositoryInterface`
- **Implementation:** `PropertyRepositoryPostgreSQL` (example using PostgreSQL)
- **Methods:**
  - `save(property: Property)`
  - `find_by_id(id: UUID)`

#### Settings Configuration
- Store property types and additional features in a configuration table.

---

## 3. Customer Profile Module

### Domain Entities

#### Client
- `id`: UUID
- `first_name`: str
- `last_name`: str
- `identification_number`: str
- `reference_address`: str
- `phone`: str
- `workplace`: str
- `work_phone`: str
- `personal_reference`: `PersonalReference`

#### PersonalReference
- `name`: str
- `phone`: str

#### AttachedDocument
- `id`: UUID
- `client_id`: UUID
- `type`: Enum (`personal_photo`, `id_photo`, `free_document`)
- `file_path`: str
- `file_name`: str

### Use Cases

#### RegisterClientUseCase
- Validates client data.
- Persists the client and their references.
- Returns the ID of the created client.

#### AttachDocumentUseCase
- Validates the file type (PDF, Excel, image).
- Stores the file in a storage service (e.g., AWS S3).
- Associates the file with the client.

### Infrastructure

#### Client Repository
- **Interface:** `ClientRepositoryInterface`
- **Implementation:** `ClientRepositoryPostgreSQL`
- **Methods:**
  - `save(client: Client)`
  - `find_by_id(id: UUID)`

#### File Storage Service
- **Interface:** `FileStorageInterface`
- **Implementation:** `S3Storage` (example using AWS S3)
- **Methods:**
  - `upload(file: bytes, name: str) -> str`
  - `get_url(path: str) -> str`

---

## 4. Configuration and Settings

### Configuration Table
- `id`: UUID
- `key`: str (e.g., `"property_types"`, `"additional_features"`)
- `value`: JSON (list of options)

### Configuration API
- Endpoints to add/edit property types and additional features.

---

## 5. REST API (Example Endpoints)

### Properties
- `POST /api/properties`: Register a property.
- `GET /api/properties/settings`: Get configurable options.

### Clients
- `POST /api/clients`: Register a client.
- `POST /api/clients/{id}/documents`: Attach a document.

---

## 6. Suggested Technologies
- **Backend:** Python (FastAPI or Django) or Node.js (NestJS).
- **Database:** PostgreSQL or MySQL.
- **File Storage:** AWS S3 or Firebase Storage.
- **Authentication:** JWT or OAuth2.

---

## 7. Testing
- **Unit Tests:** For use cases and entities.
- **Integration Tests:** For repositories and external services.
- **E2E Tests:** For complete flows (e.g., register client + attach document).
