# Biologia systemów, Projekt 1, Geometryczny Model Fishera

W repozytorium znajdują się pliki z kodem źródłowym, będącym modyfikacją podstawowego kodu z Geometrycznym Modelem Fishera (tak, aby uwzględniał nasze rozszerzenia: hibernacje i sinusoidalne zmiany optymalnego fenotypu), wykresy obrazujące uzyskane wyniki oraz raport w pliku Raport.pdf. 

Większość plików z rozszerzeniem .py jest analogicznych do tych z podstawowego modelu, z tą różnicą, ze uwzględnia nasze rozszerzenia i zapamiętywanie interesujących nas danych. 
Plik run_simulation.py zawiera funkcję, która przeprowadza pojedynczą symulację. Uruchomienie go jako __main__ będzie skutkowało włączeniem symulacji z wszystkimi parametrami z takimi wartościami jak w config.py. Pliki z tej symulacji podpisane są config_simulation.
Plik main.py uruchamia wiele symulacji i tworzy heatmapy obrazujące różne zachowanie populacji przy zmianie dwóch parametrów.

Folder gif zawiera gify przebiegu pojedynczych symulacji.
Folder frames zawiera foldery z kolejnymi klatkami pojedynczych symulacji.
Folder aktywne vs hibernowane zawiera wykresy zmiany liczby osoników aktywnych i zahibernowanych w czasie dla pojedynczej symulacji.
Folder hibernacje zawiera wykresy liczby zahibernowanych osobników w zależnośći od optymalnego fenotypu dla pojedynczej symulacji.
Jeżeli jakiś plik dotyczy pojedynczej symulacji, jest on podpisany wartościami parametrów, jakie w naszym modelu były zmieniane w formacie: nazwapliku_{mu}_{mu_h}_{sigma}_{A}_{B}, gdzie mu to prawdopodobieństwo mutacji, mu_h to prawdopodobieństwo hibernacji, sigma to siła selekcji, A to okres zmiany amplitudy, B to współczynnik okresu zmiany amplitudy (B=2pi/T, gdzie T to okres).

Plik mu_vs_sigma.png zawiera heatmapę średniej wartości fitness dla zmieniającego się parametru mu i sigma.
Plik muh_vs_sigma.png zawiera heatmapę średniej wartości fitness dla zmieniającego się parametru mu_h i sigma.
Plik mu_vs_A.png zawiera heatmapę liczby hibernacji podzieloną przez liczbę pokoleń, któym udało się przetrać dla zmieniającego się parametru mu i A.
Plik mu_vs_A_gen.png zawiera heatmapę liczby pokoleń, któym udało się przetrać dla zmieniającego się parametru mu i A.
Plik A_vs_B_widerange.png zawiera heatmapę liczby przeżytych hibernacji podzieloną przez liczbę wszystkich hibernacji zmieniającego się parametru A i B. Na jego podstawie zdecydowano o stworzeniu pliku A_vs_B_narrowrange.png z innymi zakresami parametrów A i B. Ten plik uzyskano przy pomocy skryptu AB_plot.py.


Folder streamlit_pojedyncza_symulacja zawiera pliki, dzięki którym można uruchomić pojedynczą symulację w programie streamlit, wybierając parametry za pomocą suwaków. 
