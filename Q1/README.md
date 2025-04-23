System Architecture

                      +--------------------+
                      | External REST APIs |
                      +--------------------+
                              ↓
                      +--------------------+
                      | External GraphQL   |
                      +--------------------+
                              ↓
                      +-----------------------------+
                      | Data Ingestion Worker       |
                      | (Python / Threading / Async)|
                      +-----------------------------+
                              ↓
                      +------------------------+
                      | Data Transformer       |
                      +------------------------+
                              ↓
                      +------------------------+
                      | SQL DB (PostgreSQL)    |
                      +------------------------+
                              ↓
                      +--------------------------+
                      | RESTful API (FastAPI)    |
                      +--------------------------+
                              ↓
                      +--------------------------+
                      | Frontend / Clients       |
                      +--------------------------+


Features

Performance: Asynchronous fetching.

Reliability:Retry on failed fetches.

Health checks and fallback data sources.

Sanitized input/output (e.g., to prevent injection).