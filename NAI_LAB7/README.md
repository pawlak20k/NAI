# NAI | GIn I.7 - 75c | s27118, s27084

---

# CartPole RL Agent (Python)

**Symulacja agenta RL w środowisku CartPole-v1** przy użyciu **algorytmu PPO (Proximal Policy Optimization)**.  
Program umożliwia trenowanie agenta, wizualizację jego decyzji w czasie rzeczywistym oraz eksperymentowanie z liczbą kroków treningowych.

---

# Działanie programu

*Program działa w trybie graficznym (render_mode="human") i widać, jak agent podejmuje decyzje, aby utrzymać drążek w pionie.*

Program wykonuje następujące kroki:  

1. **Tworzenie środowiska RL** (`CartPole-v1`) z Gymnasium:
   - render_mode=None podczas treningu (szybsze),
   - render_mode="human" podczas wizualizacji decyzji agenta.

2. **Tworzenie agenta PPO**:
   - sieć MLP (`MlpPolicy`) do podejmowania decyzji,
   - verbose=1, aby obserwować postęp treningu.

3. **Trenowanie agenta** (`model.learn(total_timesteps=...)`):
   - `total_timesteps` = liczba kroków środowiska (akcja → nowy stan → nagroda),
   - 5_000 kroków → szybki testowy trening (~30–60s),
   - 100_000 kroków → pełny trening (~1–2 min).

4. **Zapis wytrenowanego modelu** do pliku `ppo_cartpole.zip`.

5. **Wizualizacja działania agenta**:
   - agent w czasie rzeczywistym podejmuje decyzje,
   - po zakończeniu epizodu (drążek upadnie) środowisko resetuje się.

---

# Wymagania środowiskowe

- **Python 3.8+** (testowane na Python 3.11)  
- Biblioteki:
  - `gymnasium`
  - `stable-baselines3`
  - `torch` (PyTorch)  
- System operacyjny: dowolny (Windows / macOS / Linux)

---

# Instalacja i uruchomienie

1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install gymnasium stable-baselines3 torch
    ```
2. Trening agenta (jednorazowo, w pliku cartpole_rl.py odkomentuj linię train_agent()):
    ```bash
    python cartpole_rl.py
    ```
3. Wizualizacja agenta (po treningu, odkomentuj linię play_agent()):
    ```bash
    python cartpole_rl.py
    ```
Program automatycznie:

- trenuje model (jeśli wywołane train_agent()),
- zapisuje go do pliku ppo_cartpole.zip,
- wizualizuje działanie agenta w czasie rzeczywistym.

---

# Logika działania

1. Środowisko CartPole

- Paletka na dole, drążek na niej, który agent musi utrzymać w pionie.
- Jeśli drążek upadnie lub przekroczy granicę, epizod się kończy i środowisko resetuje się.

2. Trening agenta PPO

- Agent uczy się przewidywać najlepszą akcję w każdym stanie, aby maksymalizować nagrodę.
- timesteps określają liczbę kroków środowiska (jedna akcja + stan + nagroda).

3. Wizualizacja

- W trybie render_mode="human" widać paletkę i reakcje agenta.
- Po zakończeniu epizodu środowisko resetuje się automatycznie.

4. Parametry treningowe

- timesteps=`5_000` → szybki test, wystarczy do sprawdzenia działania.
- timesteps=`20_000` → agent zaczyna stabilnie reagować.
- timesteps=`100_000` → pełny trening, agent utrzymuje drążek w pionie długo i stabilnie.

# Struktura plików

```
CartPoleRL/
├── cartpole_rl.py        # Główny plik programu
├── README.md             # Dokumentacja projektu
└── ppo_cartpole.zip      # Wytrenowany model PPO
```

# Przykład użycia

Program uruchomiony w konsoli:

```bash
python cartpole_rl.py
```

- Trening: agent zaczyna uczyć się utrzymywać drążek w pionie (liczba kroków określona w timesteps).
- Wizualizacja: agent podejmuje decyzje w czasie rzeczywistym, widać paletkę i drążek.
- Po zakończeniu epizodu środowisko resetuje się i agent rozpoczyna nowy epizod automatycznie.

# Podsumowanie

Projekt przygotowany w ramach zajęć:
NAI GIn I.7 - 75c, LAB7

Twórcy:
- s27118
- s27084