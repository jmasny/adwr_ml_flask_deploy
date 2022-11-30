# 'Deploy modelu ML na produkcji'
*Analiza danych w czasie rzeczywistym - SGH, zima 2022*

*Jan Masny*

Repozytorium to zawiera kod zadania zaliczeniowego z przedmiotu 'Analiza danych w czasie rzeczywistym'.
W kolejnych rozdziałach krok po kroku został przedstawiony proces przygotowania zbioru danych, zbudowania modelu ML,
postawienia aplikacji Flask oraz stworzenia obrazu Docker. Głównym celem zadania było przećwiczenie tzw. udostępniania
modelu 'na produkcję'.

Informacje zawarte w README.md służą jako dokumentacja projektu.

### 1. EDA - Eksploracyjna Analiza Danych

Budowę modelu ML rozpoczęto od znaleziona zbioru danych, który posłuży do zbudowania modelu.
Wybrano zbiór `diamonds.csv`, który zawiera prawie 54 tyś. rekordów dotyczących własności diamentów i ich teoretycznych
cen rynkowych. 
Źródło danych pobrano z popularnego Kaggle: [Diamonds Dataset](https://www.kaggle.com/datasets/shivam2503/diamonds)

Jeden rekord w zbiorze danych to jedna obserwacja diamentu zawierająca 10 atrybutów:
* "carat" - waga diamentu
* "cut" - jakoś przycięcia diamentu
* "color" - kolor diamentu
* "clarity" - czystość diamentu
* "depth" - relatywna głębokość diamentu
* "table" - relatywna szerokość diamentu
* "price" - cena diamentu
* "x" - długość diamentu
* "y" - szerokość diamentu
* "z" - wysokość diamentu

Zbiór ten klasycznie wymagał wstępnego przetworzenia i wykonania eksploracyjnej analizy danych, 
zanim posłużył jako dane wejściowe do modelu ML. Krótką EDA można zobaczyć w notebooku 
[eda.ipynb](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/eda.ipynb). W wyniku przygotowania danych uzyskano czysty zbiór danych `diamonds_cleaned.csv`
zawierający ok. 47,5 tyś rekordów. 

*Disclaimer - prawdziwość informacji zawartych w zbiorze danych nie była sprawdzana. Zgodność z rzeczywistością nie jest
głównym celem tego zadania. Zbiór ten należy traktować jako wyłącznie testowy tzw. 'do nauki'.*

### 2. Budowa modelu ML

Następnie stworzono jeden prosty model regresyjny, którego zadaniem jest predykcja ceny diamentu w zależności od jego
cech charakterystycznych. Posłużono się modelem RandomForrestRegressor zaimplementowanym w bibliotece `sklearn`.
Zbiór danych wejściowych podzielono w proporcji 70:30 na dane do nauki i do testów. Sprawdzono, że przygotowany model
osiąga bardzo dobry wynik metryki *R2 score* na danych testowych, która jest istotna w przypadku tworzenia modeli
regresyjnych. Wytrenowany model zapisano w pliku `modelRR.joblib` przy pomocy biblioteki `joblib`, aby mógł później
zostać wykorzystany przez aplikację hostującą model ML. Proces budowy i nauki modelu ML można znaleźć w pliku
[create_and_train_model.py](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/create_and_train_model.py)

*Disclaimer - stworzony model jest bardzo prosty i nie poświęcono wiele czasu na dobór najlepszych parametrów
modelu, ponieważ uzyskana dokładność predykcji była od razu zadowalająca. Celem głównym zadania jest udostępnienie
projektu 'na produkcję', a niekoniecznie optymalizacja działania samego modelu ML*

### 3. Przygotowanie Flask API

Do implementacji modelu ML zdecydowano się wykorzystać mikroframework `Flask`, który pozwala na tworzenie
aplikacji webowych wraz z uruchamianiem ich na swoim serwerze. 
Aplikacja posiada dwa adresy: stronę domową i endpoint do wykonywania zapytań API.

Na stronie domowej aplikacji umieszczonej pod domyślnym adresem `/` umieszczone zostały podstawowe informacje
dotyczące działania modelu ML oraz wykonywania zapytań API. Kod html strony domowej można znaleźć w pliku
[home.html](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/templates/home.html)

![Image](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/images/home.png)


Drugim funkcjonującym adresem aplikacji jest `api/predict` tzw. endpoint API. Przez podanie 6 parametrów w metodzie GET
zapytania HTTP można uzyskać przewidywaną przez model ML ceną diamentu. 
Poniżej znajdują się przykładowe zapytania do API:

* `/api/predict?&carat=0.37&cut=3&color=0&clarity=2&depth=59.2&table=61.0&volume=60.063`
* `/api/predict?&carat=2.0&cut=2&color=1&clarity=1&depth=63.5&table=58.0&volume=274.23`

W wyniku odpowiedzi aplikacja zwraca obiekt typu JSON zawierający predykcję wielkości ceny dla diamentu pod kluczem
`predicted_price`.

![Image](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/images/answer.png)

Tym sposobem model ML został umieszczony w aplikacji, która uruchamiana jest na serwerze. Dostęp do aplikacji 
odbywa się przez port `5010` serwera. Kod aplikacji znajduję się w pliku 
[app.py](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/app.py).

### 4. Opakowanie aplikacji w obraz Docker

Ostatnim elementem zadania było wykonanie konteneryzacji aplikacji w systemie Docker, tak aby aplikacja mogła być 
udostępniania i uruchomiana na innych hostach. W tym celu najpierw zapisano wszystkie
wykorzystywane w projekcie moduły Pythona do pliku `requirements.txt`. Aby, to zrobić należy wpisać w terminalu bash
(domyślny na macOS) polecenie:

`pip freeze > requirements.txt`

Następnie stworzono plik 
[Dockerfile](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/Dockerfile), który zawiera wszystkie polecenia
potrzebne do zbudowania obrazu Docker. Między innymi w pliku tym znajdują się polecenia, które:
- `FROM` - wskazują i instalują odpowiednią wersję Pythona w obrazie Docker
- `COPY` - kopiują lokalne skrypty do obrazu Docker
- `RUN` - uruchomiają właściwe skrypty, takie jak trening modelu ML
- `EXPOSE` - wskazują port do udostępnienia z poziomu kontenera Docker
- `CMD` - finalnie uruchamiają aplikację i serwer Flask

A zatem w celu zbudowania obrazu należy w terminalu uruchomić polecenie:

`docker build -t ml_flask_deploy .`

Obraz Docker z modelem ML znajdującym się w aplikacji Flask zostanie zapisany pod nazwą `ml_flask_deploy`. 
Aby uruchomić kontener Docker na podstawie stworzonego obrazu i móc cieszyć się działaniem modelu ML 
należy uruchomić polecenie:

`docker run -p 5050:5010 ml_flask_deploy`

Polecenie to uruchomi kontener, który połączy port 5010 kontenera z portem 5050 maszyny lokalnej. Od teraz po wejściu
na loopbackowy adres z portem 5050 na lokalnej maszynie umożliwiona jest interakcja z modelem ML zamkniętym w 
kontenerze Docker.

*Disclaimer - aby skorzystać z systemu Docker wymagana jest jego wcześniejsza instalacja na komputerze.*

### 5. Podsumowanie

Tym sposobem zrealizowany został deploy modelu ML 'na produkcję'. Poprzez umieszczenie modelu ML w aplikacji `Flask` i
późniejsze opakowanie jej w obraz `Docker` można w łatwy sposób udostępniać i uruchamiać aplikację na innych
środowiskach.

Jeśli chcesz przetestować działanie projektu na swojej maszynie, wystarczy że:
- pobierzesz projekt z tego repozytorium GitHub
- w miejscu, w którym znajdują się zapisane przez Ciebie pliki projektu uruchomisz polecenia `docker build` i 
`docker run` z parametrami opisanymi w podrozdziale *4. Opakowanie aplikacji w obraz Docker*.

**Enjoy!**

### 6. Bibliografia

##### Główna architektura
- S. Zając, Modelowanie dla Biznesu, Analityka w czasie rzeczywistym - Narzędzia informatyczne i biznesowe, 
Rozdział 4.1 - Środowisko produkcyjne z modelem ML, Oficyna Wydawnicza SGH, Warszawa 2022
- [Github: sebkaz/sklearn-flask-docker](https://github.com/sebkaz/sklearn-flask-docker)

##### EDA
- [Kaggle: Regression on diamonds dataset 95 score](https://www.kaggle.com/code/heeraldedhia/regression-on-diamonds-dataset-95-score/notebook)
- [Kaggle: Diamonds interactive eda for beginners](https://www.kaggle.com/code/godzill22/diamonds-interactive-eda-for-beginners#Categorical-features)
- [Kaggle: Diamond price prediction](https://www.kaggle.com/code/karnikakapoor/diamond-price-prediction)

##### Budowa modelu ML
- [TowardsDataScience: Random Forest Regression](https://towardsdatascience.com/random-forest-regression-5f605132d19d)

##### Przygotowanie Flask API
- [Flask Mega Tutorial: APIs](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis)

##### Opakowanie aplikacji w obraz Docker
- [TomasBeuzen: ML deploy model](https://github.com/TomasBeuzen/machine-learning-tutorials/blob/master/ml-deploy-model/deploy-with-flask.ipynb)
- [Medium: Machine Learning Model Deployment in Docker using Flask](https://medium.com/swlh/machine-learning-model-deployment-in-docker-using-flask-d77f6cb551d6)
