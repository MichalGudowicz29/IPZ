# IPZ - nowa grupa 

Zasady pracy z repo: 
1. Branch `main` na kazdym etapie pracy powinień być w pełni działający, gotowy do przedstawienia postępów.
2. Branch `dev` odpowiada za rozwój aplikacji, zmiany będą mergowane z główną gałęzią dopiero po testach i sprawdzeniu. 


```bash
git clone https://github.com/MichalGudowicz29/IPZ.git
```

Foldery: 

src - główny folder z kodem

docs - dokumentacja kodu & raporty 


### Instrukcja pracy z GitHubem:

1. Github służy jako główne miejsce przechowywania plików 
	1. Github posiada najnowszą wersję projektu
2. Gałąź `main` odpowiada za przechowywanie wersji projektu, która jest najnowsza ale w pełni FUNKCJONALNA i przetestowana. Funkcja main odpowiada za aspekt prezentacji postępów w razie potrzeby. 
3. Gałąź `dev` służy do rozwoju kodu, testowania oraz eksperymentowania a po przetestowaniu nowych funkcjonalności i uznania je za sprawdzone i gotowe do połączenia, następuje merge z gałęzią główną.


Pierwsza styczność:
Wchodzimy w terminal wpisujemy:
```bash
git clone https://github.com/MichalGudowicz29/IPZ.git
```
Następnie:
```bash
cd IPZ
```
Jesteśmy w folderze IPZ, wraz z najnowszym kodem. 
Następnie schodzimy z głównej gałęzi na gałąź rozwoju kodu:
```bash
git checkout dev
```


Ważne: 
Gdy siadamy do robienia czegokolwiek, pierwsza komenda jaka wykonamy to: 
```bash
git pull origin dev
```
ważne - wykonujemy ten pull będąc na gałęzi  dev

Następnie możemy uruchomić ten folder w Visual Studio Code lub edytorze według preferencji i rozpocząć prace nad kodem. 


Co jakiś czas, najlepiej po wykonaniu cześci zadania, zrobieniu zmiany, zrobieniu funkcji - zaleca się wykonać: 
```bash
git add .
git commit -m "Opis zmian"
```
Sam commit to checkpoint pracy nad kodem, pozwala to rozbić wielki push z wieloma zmianami na małe części podczas sprawdzania kodu oraz zarządzania wersją. WAŻNE - sam commit nie powoduje zmian w repozytorium publicznym.

Gdy uznamy że zadanie jest skończone robimy:
```bash
git push -u origin dev
```
Co popchnie nasze zmiany do publicznego repozytorium.
