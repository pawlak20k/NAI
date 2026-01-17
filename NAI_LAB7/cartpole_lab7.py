"""
CartPole RL Agent – w pełni graficzna demonstracja decyzji agenta
Autor: s27118, s27084
Opis:
    Agent RL uczy się utrzymywać drążek w pionie (CartPole-v1) przy użyciu PPO.
    Graficzna wizualizacja w trybie "human" – widać wszystkie decyzje agenta.

Instrukcja użycia:
    1. pip install gymnasium stable-baselines3 torch
    2. python cartpole_lab7.py
"""

import gymnasium as gym
from stable_baselines3 import PPO

def train_agent(env_name="CartPole-v1", timesteps=5_000):
    """
    Funkcja trenuje agenta PPO w środowisku CartPole.

    :param env_name: nazwa środowiska z Gymnasium
    :param timesteps: liczba kroków treningowych
        - 1 krok = jedna interakcja agenta ze środowiskiem (akcja -> nowy stan -> nagroda)
        - 5_000 kroków = bardzo szybki, testowy trening
        - 100_000 kroków = solidny trening, agent uczy się stabilnie utrzymywać drążek
    """
    # Tworzymy środowisko RL, render_mode=None, bo w trakcie treningu nie wyświetlamy grafiki
    env = gym.make(env_name, render_mode=None)

    # Tworzymy agenta PPO z domyślną siecią MLP (wielowarstwowa perceptronowa)
    model = PPO("MlpPolicy", env, verbose=1)

    # Trenujemy agenta
    # total_timesteps = liczba kroków środowiska, czyli ile razy agent podejmie akcję i dostanie nagrodę
    model.learn(total_timesteps=timesteps)

    # Zapisujemy wytrenowany model do pliku ppo_cartpole.zip
    # Dzięki temu możemy go potem wczytać i odtworzyć decyzje agenta
    model.save("ppo_cartpole")

    # Zamykamy środowisko (sprzątanie)
    env.close()

    return model


def play_agent(env_name="CartPole-v1"):
    """
    Funkcja uruchamia wytrenowanego agenta w trybie graficznym ("human").
    Widać jak paletka automatycznie reaguje, żeby utrzymać drążek w pionie.
    """
    # Tworzymy środowisko w trybie graficznym
    env = gym.make(env_name, render_mode="human")

    # Wczytujemy wcześniej wytrenowany model PPO
    model = PPO.load("ppo_cartpole")

    # Resetujemy środowisko i pobieramy początkową obserwację
    obs, _ = env.reset()

    # Główna pętla gry
    while True:
        # Agent przewiduje najlepszą akcję na podstawie obserwacji
        action, _ = model.predict(obs)

        # Wykonujemy akcję w środowisku
        # obs = nowy stan
        # reward = nagroda za tę akcję
        # done = True, jeśli epizod (próba utrzymania drążka) się zakończył
        obs, reward, done, truncated, _ = env.step(action)

        # Jeśli epizod się skończył, resetujemy środowisko (nowa próba)
        if done or truncated:
            obs, _ = env.reset()


if __name__ == "__main__":
    # Jeśli chcesz wytrenować model od nowa:
    # train_agent(timesteps=5_000)   # szybki testowy trening (~30-60s)
    # train_agent(timesteps=100_000) # pełny trening (~1-2 min)

    # Po wytrenowaniu wywołujemy wizualizację:
    play_agent()
