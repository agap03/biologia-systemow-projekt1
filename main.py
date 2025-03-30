import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from run_simulation import run_simulation
import config


fitness_map=[] # lista do heat mapy fitnessu

mutation_rates = np.linspace(0.05, 0.9, 5)  # Przykładowe wartości mutacji
selection_strengths = np.linspace(0.1, 2, 5)  # Przykładowe wartości selekcji

for i in mutation_rates:
    mu=round(i, 2)
    fitnesses_current=[] # średnie fitness przy zmianie tylko sigma
    for j in selection_strengths:
        sigma=round(j, 2)

        _, _, _, fitnesses, _= run_simulation(
                        config.N,
                        mu,
                        config.mu_c,
                        config.xi,
                        sigma,
                        config.threshold,
                        config.hibernation_thresh,
                        config.h_p,
                        config.mu_h,
                        config.A,
                        config.B,
                        config.max_generations,
                    )
        fitnesses_current.append(fitnesses) 
    fitness_map.append(fitnesses_current) #  drugi wymiar to zmiana sigmy


plt.figure(figsize=(6, 6))
ax=sns.heatmap(fitness_map, xticklabels=np.round(mutation_rates, 2), yticklabels=np.round(selection_strengths, 2), annot=True)
ax.invert_yaxis()

plt.xlabel("Współczynnik mutacji (μ)")
plt.ylabel("Siła selekcji (ω²)")
plt.title("Wpływ mutacji i selekcji na adaptację populacji (fitness)")
plt.tight_layout()
plt.savefig("mu_vs_sigma.png")
plt.close()

print("Heatmapa zapisana jako mu_vs_sigma.png")
print("----------------------Pierwsza część zakończona-------------------------")


hibernation_map=[] # lista do przechowywania liczby hibernacji (do heatmapy)
generation_map=[] # lista do liczby przeżytych pokoleń

mutation_rates = np.linspace(0.05, 0.9, 5)  # Przykładowe wartości mutacji
A_lin = np.linspace(0.1, 3, 5)  # Przykładowe wartości selekcji

for i in mutation_rates:
    mu=round(i, 2)
    hib_current=[] # liczba wszystkich mutacji/ liczba przeżytych pokoleń
    gen_current=[]
    for j in A_lin:
        A=round(j, 2)

        _, _, no_hib, _, no_gen= run_simulation(
                        config.N,
                        mu,
                        config.mu_c,
                        config.xi,
                        config.sigma,
                        config.threshold,
                        config.hibernation_thresh,
                        config.h_p,
                        config.mu_h,
                        A,
                        config.B,
                        config.max_generations,
                    )
        hib_current.append(no_hib/no_gen)
        gen_current.append(no_gen) 
    hibernation_map.append(hib_current)
    generation_map.append(gen_current)


plt.figure(figsize=(6, 6))
ax=sns.heatmap(hibernation_map, xticklabels=np.round(mutation_rates, 2), yticklabels=np.round(A_lin, 2), annot=True)
ax.invert_yaxis()

plt.xlabel("Współczynnik mutacji (μ)")
plt.ylabel("Amplituda optimum (A)")
plt.title("Wpływ mutacji i amplitudy na liczbę hibernacji")
plt.tight_layout()
plt.savefig("mu_vs_A.png")
plt.close()

print("Heatmapa zapisana jako mu_vs_A.png")

plt.figure(figsize=(6, 6))
ax=sns.heatmap(generation_map, xticklabels=np.round(mutation_rates, 2), yticklabels=np.round(A_lin, 2), annot=True, fmt=".0f")
ax.invert_yaxis()

plt.xlabel("Współczynnik mutacji (μ)")
plt.ylabel("Amplituda optimum (A)")
plt.title("Wpływ mutacji i amplitudy na przeżywalność populacji")
plt.tight_layout()
plt.savefig("mu_vs_A_gen.png")
plt.close()

print("Heatmapa zapisana jako mu_vs_A_gen.png")
print("----------------------Druga część zakończona-------------------------")


surv_hib_map=[] # lista do przechowywania liczby przeżytych hibernacji (do heatmapy)

B_lin = np.linspace(0.1, 2, 5)  # Przykładowe wartości B
A_lin = np.linspace(0.1, 3, 5)  # Przykładowe wartości A

for i in A_lin:
    A=round(i, 2)
    surv_current=[] # liczba przeżytych hibernacji/ liczba wszystkich hibernacji
    for j in B_lin:
        B=round(j, 2)

        surv_hib, _, no_hib, _, _= run_simulation(
                        config.N,
                        config.mu,
                        config.mu_c,
                        config.xi,
                        config.sigma,
                        config.threshold,
                        config.hibernation_thresh,
                        config.h_p,
                        config.mu_h,
                        A,
                        B,
                        config.max_generations,
                    )
        if(no_hib!=0):
            surv_current.append(surv_hib/no_hib) 
        else:
            surv_current.append(-1)
    surv_hib_map.append(surv_current)


plt.figure(figsize=(6, 6))
ax=sns.heatmap(surv_hib_map, xticklabels=np.round(A_lin, 2), yticklabels=np.round(B_lin, 2), annot=True)
ax.invert_yaxis()

plt.xlabel("Amplituda optimum (A)")
plt.ylabel("Współczynnik okresu optimum (B)")
plt.title("Wpływ amplitudy i okresu na przeżywalność hibernacji")
plt.tight_layout()
plt.savefig("A_vs_B.png")
plt.close()

print("Heatmapa zapisana jako A_vs_B.png")
print("----------------------Trzecia część zakończona-------------------------")
print("Koniec programu!")