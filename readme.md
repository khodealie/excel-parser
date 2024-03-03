# Excel Parser Project

## Technologies Used
This project leverages several technologies:
- **Django**: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **Redis**: An open-source, in-memory data structure store, used as a database, cache, and message broker.
- **MySQL**: An open-source relational database management system.
- **Docker**: A set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX, a pre-fork worker model.

## Services
- **Excel Service**: Processes Excel files to extract and organize data into the database. 
  - **Input**: Excel files with device categories, brands, series, and models.
  - **Output**: Structured data stored in MySQL.
  
- **Hierarchy Service**: Retrieves and displays the hierarchical structure of devices, utilizing Redis for efficient data retrieval.
  - **Input**: HTTP requests for device hierarchy data.
  - **Output**: JSON structure representing the hierarchy of device categories, brands, series, and models.

## Setup and Running
The application is containerized with Docker, simplifying the setup and execution. Use the provided `docker-compose.yml` to run all required services with Docker Compose. Before starting the project, execute the `setup.sh` script to configure necessary environment variables, perform database migrations, and collect static files. This ensures a smooth startup and operation of the project.
