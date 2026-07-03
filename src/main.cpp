#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector> 
#include "httplib.h"
#include "trie.h"
#include "graph.h" 

void loadStreetsIntoTrie(Trie& trie) {
    std::ifstream file("src/nume_strazi.txt");
    if (!file.is_open()) {
        std::cerr << "Eroare critică: Nu am putut deschide fișierul 'src/nume_strazi.txt'!" << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string name, u, v;

        if (std::getline(ss, name, ',') && 
            std::getline(ss, u, ',') && 
            std::getline(ss, v, ',')) {
            
            trie.insert(name, u);
        }
    }
    file.close();
}

int main() {
    std::cout << "--- Initializare Server Backend ---" << std::endl;

    Trie streetsTrie;
    std::cout << "1. Incarc strazile in Trie..." << std::endl;
    loadStreetsIntoTrie(streetsTrie);

    Graph G;
    std::cout << "2. Incarc graful..." << std::endl;
    G.loadFromFile("src/statii.txt");

    std::cout << "Datele au fost incarcate cu succes in memoria RAM!" << std::endl;

    httplib::Server svr;

    svr.Get("/get_route", [&](const httplib::Request& req, httplib::Response& res) {
        
        std::string startName = req.get_param_value("start");
        std::string endName = req.get_param_value("end");

        std::cout << "\n[Request Nou] Calculez ruta: " << startName << " -> " << endName << std::endl;

        std::string startID = streetsTrie.search(startName);
        std::string endID = streetsTrie.search(endName);

        if (startID == "NOT_FOUND" || endID == "NOT_FOUND") {
            res.set_content("EROARE: Una dintre strazi nu a fost gasita.", "text/plain");
            return;
        }

        std::vector<std::string> path = G.Dijkstra(startID, endID);

        if (path.empty()) {
            res.set_content("EROARE: Nu exista drum intre aceste strazi.", "text/plain");
            return;
        }

        std::string response_text = "";
        for (const auto& node : path) {
            response_text += node + "\n";
        }

        res.set_content(response_text, "text/plain");
        std::cout << "[Succes] Traseul a fost calculat si trimis inapoi instant!" << std::endl;
    });

    std::cout << "Serverul este GATA si asculta pe http://127.0.0.1:8085" << std::endl;
    svr.listen("127.0.0.1", 8085);

    return 0;
}