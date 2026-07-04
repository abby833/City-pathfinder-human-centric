# City PathFinder

[![C++ Unit Tests](https://github.com/abby833/City-pathfinder/actions/workflows/ci.yml/badge.svg)](https://github.com/abby833/City-pathfinder/actions)

A high-performance hybrid navigation system calculating the shortest path between addresses using real-world OpenStreetMap data.

![Navigation Demo](demo0.png) ![Navigation Demo](demo1.png)

## Core Architecture & Tech Stack

- **C++17 Backend:** Powered by Dijkstra's Algorithm and a Trie data structure (O(L) complexity) for instant street lookups.
- **Client-Server Optimization:** Refactored from a slow subprocess model into a persistent HTTP Daemon (`cpp-httplib`). Graph data is loaded into RAM once (Hot Start), eliminating disk I/O and reducing routing responses to milliseconds.
- **Python Frontend:** Streamlit & Folium provide an interactive, autocomplete-enabled UI that communicates with the C++ engine via REST-like API requests.
- **Testing & CI/CD:** Reliable core logic ensured by Catch2 unit tests and automated via GitHub Actions.

---

## Quick Start

**Prerequisites:** C++17 Compiler, CMake, and Python 3.8+

```bash
# 1. Build the C++ Engine
mkdir build && cd build
cmake .. && cmake --build .

# 2. Install Python Dependencies
pip install -r requirements.txt