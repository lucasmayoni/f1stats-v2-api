# Fast-F1 Data Analysis

This project is set up to use the [Fast-F1](https://github.com/theOehrly/Fast-F1) library for Formula 1 data analysis.

## Setup

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

-   **Scripts**: Python scripts are located in `src/`.
-   **Notebooks**: Jupyter notebooks are located in `notebooks/`.
-   **Data**: Cached data is stored in `data/`.

## Deployment

This project is configured for deployment using Docker (e.g., on Render, Railway, Fly.io).

1.  Build the Docker image:
    ```bash
    docker build -t f1-api .
    ```
2.  Run the container:
    ```bash
    docker run -p 8000:8000 f1-api
    ```
3.  Access the API at `http://localhost:8000/api/fastest_lap`.
