# City PathFinder

[![C++ Unit Tests](https://github.com/abby833/City-pathfinder/actions/workflows/ci.yml/badge.svg)](https://github.com/abby833/City-pathfinder/actions)

A high-performance hybrid navigation system that calculates the shortest path between two street addresses using real-world data from OpenStreetMap. 

![Navigation Demo](demo0.png)
![Navigation Demo](demo1.png)

## Tech Stack
- **Backend/Engine:** C++17 (Dijkstra's Algorithm, Trie lookup with O(L) complexity, Local HTTP Daemon via `cpp-httplib`).
- **Testing:** Catch2 (Behavior-Driven Development methodology).
- **Frontend/Visualization:** Python (Streamlit, Folium, `requests`).
- **Data Source:** OpenStreetMap API (via OSMnx).
- **Build System & CI/CD:** CMake and GitHub Actions.

## Performance Optimization: The Client-Server Evolution
Initially, the system used a Subprocess execution model where the Python frontend triggered the C++ engine for every request. This resulted in a "Cold Start" bottleneck: the engine had to read text files from the disk, rebuild the Trie and Graph data structures, calculate the route, and then shut down.

**The Solution:** The architecture was refactored into a **Client-Server (Daemon) model**. 
* The C++ routing engine now runs continuously as a local HTTP server. 
* Data structures (Graph & Trie) are loaded into RAM **only once** at startup (Hot Start).
* Python acts as a client, requesting routes via a REST-like API.
* **Result:** Route calculation and rendering now happen almost instantly (in milliseconds), completely eliminating disk I/O overhead during user queries.

## System Architecture
This project follows a "Separation of Concerns" modular design to ensure high performance, maintainability, and testability:

1. **Data Processing (`server.py`):** Python script that extracts the street network from OSM and serializes it into structured files.
2. **Computation Engine (C++ Backend):** An optimized, long-running engine leveraging `std::unordered_map` for O(1) lookup times and memory-safe STL containers. It listens for HTTP requests and handles the core routing logic.
3. **Automated Testing (`tests/`):** A dedicated testing suite ensuring the reliability of the core algorithms in isolated environments.
4. **Web Interface (Python Frontend):** Provides an autocomplete-enabled UI and communicates seamlessly with the C++ backend via HTTP requests.
5. **Visualization:** The computed route is rendered instantly as an interactive Polyline.

## How to Build and Run

To get the system running, you need to start both the backend server and the frontend interface.

### 1. Build the C++ Engine (CMake)
```bash
mkdir build
cd build
cmake ..
cmake --build .

### 2. Run the Application (Two-Terminal Setup)
# On Windows:
.\build\Debug\navigator.exe
# On Linux/Mac:
./build/navigator

Open a new terminal and run the Streamlit interface: python -m streamlit run web_app.py

### 3. Run the Unit Tests
To verify the core logic:
# On Windows:
.\build\Debug\run_tests.exe
# On Linux/Mac:
./build/run_tests