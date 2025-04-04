import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from run_simulation import run_simulation
import config

surv_hib_map=[] # lista do przechowywania liczby przeżytych hibernacji (do heatmapy)

B_lin = np.linspace(0.1, 1, 5)  # Przykładowe wartości B
A_lin = np.linspace(0.1, 1, 5)  # Przykładowe wartości A

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
ax=sns.heatmap(surv_hib_map, yticklabels=np.round(A_lin, 2), xticklabels=np.round(B_lin, 2), annot=True)
ax.invert_yaxis()

plt.ylabel("Amplituda optimum (A)")
plt.xlabel("Współczynnik okresu optimum (B)")
plt.title("Wpływ amplitudy i okresu na przeżywalność hibernacji")
plt.tight_layout()
plt.savefig("A_vs_B.png")
plt.close()

print("Heatmapa zapisana jako A_vs_B_narrowrange.png")