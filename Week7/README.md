# Pfadfindung mit Mehrzieloptimierung

__author__: "8636650, Kara, 8658986, Al-Ramessi"  
Semester: WiSe 2025/2026  

Dieses Projekt implementiert Algorithmen, um den besten Pfad in einem Graphen zu finden, der Kosten und Ablenkung für jede Kante hat. Ziel ist die Mehrzieloptimierung (Pareto-Optimierung).

---

## Dateien

### 1. `graph_tools.py`
- Enthält die Kernlogik des Projekts
- `Graph` – ungerichteter Graph mit Knoten und Kanten (Kosten, Ablenkung)
- Strategien für Mehrzieloptimierung:
  - `strategy_diff(cost, distraction)` – Kosten minimieren, Ablenkung maximieren
  - `strategy_ratio(cost, distraction)` – Ablenkung pro Kosteneinheit maximieren
  - `strategy_max_distraction(cost, distraction)` – nur Ablenkung maximieren
- Pfadfindung:
  - `find_greedy(graph, start, target, strategy_func, mode)` – lokal beste Kante
  - `find_recursive(graph, start, target, strategy_func, mode)` – global optimal

### 2. `benchmark_graph_tools.py`
- Enthält Testgraphen und Zeitmessung
- Erstellt drei Beispielgraphen
- `benchmark_graph(graph, start, target)` misst Laufzeit von Greedy- und Rekursiv-Algorithmen
- Ergebnisse werden auf der Konsole ausgegeben und als Kommentar dokumentiert


---

## Graph-Beispiel
**Kanten (Kosten / Ablenkung)**

- A-B: 3 / 2  
- B-D: 4 / 5  
- C-D: 2 / 3  
- D-H: 3 / 4  
- B-E: 2 / 1  
- E-H: 5 / 0  
- A-C: 1 / 0  

---

## Unterschied Greedy vs Rekursiv

**Greedy:** wählt lokal beste Kante basierend auf der Strategie  
- Kann in Sackgassen oder suboptimalen Pfaden enden  

**Rekursiv:** prüft alle Pfade und wählt den global besten Pfad  
- Garantiert optimalen Pfad für die gewählte Strategie  

**Beispielergebnisse** (bei Strategie `strategy_diff` min):

- Greedy: `A -> B -> D -> H`  
- Rekursiv: `A -> C -> D -> H`  

---

## Kurze Anleitung

**Pfadberechnung testen:**

```python
from graph_tools import Graph, find_greedy, strategy_diff

g = Graph()
g.add_edge("A", "B", 5, 2)
result = find_greedy(g, "A", "B", strategy_diff, "min")
print(result)
# Ausgabe: (['A', 'B'], 5, 2)


Benchmark ausführen:
python benchmark_graph_tools.py