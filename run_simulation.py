import os
import numpy as np
import matplotlib.pyplot as plt
from environment import Environment
from population import Population
from mutation import mutate_population
from selection import threshold_selection
from reproduction import asexual_reproduction
from visualization import plot_population
import config


def create_gif_from_frames(frames_dir, gif_filename, duration=0.2):
    """
    Łączy wszystkie obrazki z katalogu `frames_dir` w jeden plik GIF.
    Wymaga biblioteki imageio (pip install imageio).
    :param frames_dir: folder z plikami .png
    :param gif_filename: nazwa pliku wyjściowego GIF
    :param duration: czas wyświetlania jednej klatki w sekundach
    """
    import imageio
    import os

    # Sortujemy pliki po nazwach, żeby zachować kolejność generacji
    filenames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    
    with imageio.get_writer(gif_filename, mode='I', duration=duration) as writer:
        for file_name in filenames:
            path = os.path.join(frames_dir, file_name)
            image = imageio.imread(path)
            writer.append_data(image)

    return


def run_simulation(
    N,      # liczba osobników w populacji
    mu,       # prawdopodobieństwo mutacji dla osobnika
    mu_c,     # prawdopodobieństwo mutacji konkretnej cechy, jeśli osobnik mutuje
    xi,        # odchylenie standardowe w rozkładzie normalnym mutacji
    sigma,    # parametr w funkcji fitness (kontroluje siłę selekcji)
    threshold,  # przykładowy próg do selekcji progowej (do ewentualnego użycia)
    hibernation_thresh, # próg hibernacji
    h_p,        # prawdopodobieństwo obudzenia się z hibernacji przy jednym pokoleniu (do rozkładu geometrycznego losowania długości hibernacji)
    mu_h,       # prawdopodobieństwo hibernacji, gdy w dobrym progu
    # amplituda i okres sinusoidalnej zmiany optymalnego fenotypu
    A,
    B,
    max_generations, # liczba pokoleń do zasymulowania
):

    n=config.n
    alpha0=config.alpha0

    env = Environment(alpha_init=alpha0, A=A, B=B)
    pop = Population(size=N, n_dim=n)

    # Katalog, w którym zapisujemy obrazki
    frames_dir = f"frames_{mu}_{sigma}_{A}_{B}"
    os.makedirs(frames_dir, exist_ok=True)  # tworzy folder, jeśli nie istnieje

    #listy do wykresu liczby hibernacji w zależności od optimum
    opts=[]
    hibernated=[]

    active=[]

    fitnesses=[] # lista do zbierania średniego fitness

    no_generation=max_generations # zmienna do sprawdzania, czy i kiedy cała populacja wymarła 

    for generation in range(max_generations):

        # 1. Mutacja
        mutate_population(pop, mu=mu, mu_c=mu_c, xi=xi)

        # 2. Selekcja
        survivors, current_fitnesses= threshold_selection(pop, env.get_optimal_phenotype(), sigma, threshold,  hibernation_thresh, h_p, mu_h)
        fitnesses.extend(current_fitnesses)

        # 3. Reprodukcja
        new_pop=asexual_reproduction(survivors, N)

        pop.set_individuals(new_pop)

        if len(new_pop) <= 0:
            print(f"Wszyscy wymarli w pokoleniu {generation}. Kończę symulację.")
            no_generation=generation
            break

        # 4. Zmiana środowiska
        env.update()


        # Zapis aktualnego stanu populacji do pliku PNG
        frame_filename = os.path.join(frames_dir, f"frame_{generation:03d}.png")
        plot_population(pop, env.get_optimal_phenotype(), generation, save_path=frame_filename, show_plot=False)
        
        no_hib=0
        no_active=0
        for ind in pop.get_individuals():
            if ind.is_hibernated():
                no_hib+=1
            else:
                no_active+=1

        hibernated.append(no_hib)
        opts.append(env.get_optimal_phenotype()[0])

        active.append(no_active)
                

    print("Symulacja zakończona.")

    print("Przeżyte hibernacje: ", pop.get_survived_hib(), "; Powtórzone hibernacje: ", pop.get_repeated_hib(), "; Wszystkie hibernacje: ", pop.get_total_hib(), "\n")
    print("średnie fitness = ", np.mean(fitnesses))

    print("Tworzenie GIF-a...")

    # Tutaj wywołujemy funkcję, która połączy zapisane klatki w animację
    create_gif_from_frames(frames_dir, f"simulation_{mu}_{sigma}_{A}_{B}.gif")
    print(f"GIF zapisany jako simulation_{mu}_{sigma}_{A}_{B}.gif")

    print("Tworzenie wykresu z liczbą hibernacji...")

    plt.figure(figsize=(5, 5))
    plt.scatter(opts, hibernated, alpha=0.7)
    plt.title(f"Liczba hibernacji w zależności od optimum")
    plt.xlim(-A-0.5, A+0.5)
    xlabels=np.linspace(-A, A, 7)
    plt.xticks(xlabels, [f"({x:.1f}, {x:.1f})" for x in xlabels], rotation ='vertical')
    plt.xlabel("Optimum")
    plt.ylabel("Liczba osobników w hibernacji")
    plt.tight_layout()
    plt.savefig(f"hibernacje_{mu}_{sigma}_{A}_{B}.png")
    plt.close()

    print(f"Liczba hibernacji zapisana jako hibernacje_{mu}_{sigma}_{A}_{B}.png")

    print("Tworzenie wykresu z liczbą aktywnych i zahibernowanych osobników w czasie...")

    plt.figure(figsize=(5, 5))

    plt.plot(active, color ='r', label ='aktywne') 
    plt.plot(hibernated, color ='g', label ='zahibernowane')
    plt.title("liczba osobników w czasie")
    plt.xlabel("Pokolenie")
    plt.ylabel("Liczba osobników")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"akt_hib_{mu}_{sigma}_{A}_{B}.png")
    plt.close()

    print(f"Liczba aktywnych i zahibernowanych zapisana jako akt_hib_{mu}_{sigma}_{A}_{B}.png")

    return pop.get_survived_hib(), pop.get_repeated_hib(), pop.get_total_hib(), np.mean(fitnesses), no_generation
        