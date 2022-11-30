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

Do udostępnienia modelu 'na produkcję' zdecydowano się wykorzystać mikroframework `Flask`, który pozwala na tworzenie
aplikacji webowych wraz z uruchamianiem ich na swoim serwerze. Kod aplikacji znajduję się w pliku 
[app.py](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/app.py).
Aplikacja posiada dwa adresy: stronę domową i endpoint do wykonywania zapytań API.

Na stronie domowej `home.html` umieszczonej pod domyślnym adresem `/` umieszczone zostały podstawowe odnośnie działania
modelu ML oraz wykonywania zapytań API. Kod html strony domowej można znaleźć w pliku
[home.html](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/templates/home.html)
![Image](https://github.com/jmasny/adwr_ml_flask_deploy/blob/main/images/home.png)


Drugim funkcjonującym adresem aplikacji jest `api/predict` tzw. endpoint API. Przez podanie 6 parametrów w metodzie GET
można uzyskać odpowiedź w formacie json z 

- opis strony tytulowej
- opis dzialania api

### 4. Opakowanie aplikacji w kontener Docker
- opis
TO DO

### 5. Uruchomienie i przykładowe call do API 
index carat  cut  color  clarity  depth  table      volume
31404   0.37    3      0        2   59.2   61.0   60.060360
30058   0.31    4      1        4   60.1   59.0   50.993712
6365    1.01    2      0        1   63.5   58.0  163.670904
32482   0.41    4      1        2   60.8   57.0   66.627360
16865   1.52    1      0        2   63.3   56.0  246.195642

### jak uruchomić ten projekt

### Bibliografia

##### Główne informacje
- S. Zając, Modelowanie dla Biznesu, Analityka w czasie rzeczywistym - Narzędzia informatyczne i biznesowe, 
Rodział 4.1 - Środowisko produkcyjne z modelem ML, Oficyna Wydawnicza SGH, Warszawa 2022
- [Github: sebkaz/sklearn-flask-docker](https://github.com/sebkaz/sklearn-flask-docker)

##### EDA
- [Kaggle: Regression on diamonds dataset 95 score](https://www.kaggle.com/code/heeraldedhia/regression-on-diamonds-dataset-95-score/notebook)
- [Kaggle: Diamonds interactive eda for beginners](https://www.kaggle.com/code/godzill22/diamonds-interactive-eda-for-beginners#Categorical-features)
- [Kaggle: Diamond price prediction](https://www.kaggle.com/code/karnikakapoor/diamond-price-prediction)

##### Budowa modelu ML
- [TowardsDataScience: Random Forest Regression](https://towardsdatascience.com/random-forest-regression-5f605132d19d)
- https://thecleverprogrammer.com/2021/06/22/r2-score-in-machine-learning/

### tymczasowe linki
https://github.com/TomasBeuzen/machine-learning-tutorials/blob/master/ml-deploy-model/deploy-with-flask.ipynb
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers
https://medium.com/swlh/machine-learning-model-deployment-in-docker-using-flask-d77f6cb551d6