# Github Stats

Проект для извлечения статистики из репозитория github.

## Сбор

### Варианты сбора статистики

1. Запрос по заданному периоду из дат. Период представляет собой начальную дату и дату окончания. Статистика собирает данные репозитория с минимальным периодом в один месяц, отсчитывая диапазон, начиная с первой даты.
2. Запрос по тэгам релизов указанного репозитория. Собирается статистика репозитория с каждого релиза от его создания до даты следующего релиза. Если релиз является последним, то до текущей даты. Затем выполняется сравнение статистики релизов, начиная с самого раннего.

**Время сбора зависит от размера (количество pr, issues, stars, forks) репозитория*

## Рекомендации

1. Python v3.6 или выше
2. OpenCV v3.4.3 или выше
3. [PyGithub](https://github.com/PyGithub/PyGithub)
4. [Google Drive API v3](https://developers.google.com/drive/api/v3/quickstart/python)

## Использование

### Подключение

`python github_stat.py -u [github-username] -pw [github-password] -r [github-repo] -p [period] -ocv [export_opencv] -csv [export_csv] -gdoc [export_gdoc]`

Где:
 - `[github-repo]` - github репозиторий.
 - `[github-username]` - логин или токен пользователя.
 - `[github-password]` - пароль (если указан токен, то пароль не требуется).
 - `[period]` - период (начальная и конечная даты, либо тэги релизов репозитория).
 - `[export_opencv]` - сохраняет статистику с помощью OpenCV в файл с раширением yml (также вся статистика переводится в матрицу, которая также записывается в файл.
 - `[export_csv]` - записывает статистику в формат csv.
 - `[export_gdoc]` - записывает статистику в облако Google Drive.

**Внимание: логин (токен) и/или пароль обязательны, так как github предоставляет статистику только авторизованным пользователям.*

## Пример

### Вариант 1. Dates

#### using username + password

```
python github_stats.py -u golubevdmi -pw GITHUB_PASSWORD -r pygithub/pygithub -p 2019.01.01 2019.12.01 -ocv -csv -gdoc
```

#### or user token

```
python github_stats.py -u GITHUB_TOKEN -r pygithub/pygithub -p 2019.01.01 2019.12.01 -ocv -csv -gdoc
```

<details>
 <summary>Вывод статистики за 2019 год (репо pygithub/pygithub):</summary>

```
Parsed dates:
         2019-01-01  -  2019-02-01
         2019-02-01  -  2019-03-01
         2019-03-01  -  2019-04-01
         2019-04-01  -  2019-05-01
         2019-05-01  -  2019-06-01
         2019-06-01  -  2019-07-01
         2019-07-01  -  2019-08-01
         2019-08-01  -  2019-09-01
         2019-09-01  -  2019-10-01
         2019-10-01  -  2019-11-01
         2019-11-01  -  2019-12-01
         2019-12-01  -  2020-01-01
>> get metric: 2019-01-01  -  2019-02-01
>> get metric: 2019-02-01  -  2019-03-01
>> get metric: 2019-03-01  -  2019-04-01
>> get metric: 2019-04-01  -  2019-05-01
>> get metric: 2019-05-01  -  2019-06-01
>> get metric: 2019-06-01  -  2019-07-01
>> get metric: 2019-07-01  -  2019-08-01
>> get metric: 2019-08-01  -  2019-09-01
>> get metric: 2019-09-01  -  2019-10-01
>> get metric: 2019-10-01  -  2019-11-01
>> get metric: 2019-11-01  -  2019-12-01
>> get metric: 2019-12-01  -  2020-01-01

Period: 2019.01.01 2019.02.01
Tag:
        PullR:          all: 41         open: 23        opened: 17      closed: 7       merged: 4
        Issues:         all: 98         open: 68        opened: 29      closed: 19
        Stars:          all: 2294       Stars snapshot: 2226    Stars per period: 69
        Forks:          all: 743        Forks snapshot: 716     Forks per period: 27
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.02.01 2019.03.01
Tag:
        PullR:          all: 41         open: 33        opened: 8       closed: 11      merged: 5
        Issues:         all: 101        open: 77        opened: 24      closed: 25
        Stars:          all: 2364       Stars snapshot: 2294    Stars per period: 71
        Forks:          all: 766        Forks snapshot: 743     Forks per period: 25
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.03.01 2019.04.01
Tag:
        PullR:          all: 39         open: 30        opened: 9       closed: 18      merged: 5
        Issues:         all: 98         open: 75        opened: 23      closed: 20
        Stars:          all: 2433       Stars snapshot: 2364    Stars per period: 74
        Forks:          all: 794        Forks snapshot: 766     Forks per period: 30
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.04.01 2019.05.01
Tag:
        PullR:          all: 35         open: 21        opened: 9       closed: 18      merged: 5
        Issues:         all: 113        open: 78        opened: 29      closed: 32
        Stars:          all: 2529       Stars snapshot: 2433    Stars per period: 97
        Forks:          all: 823        Forks snapshot: 794     Forks per period: 31
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.05.01 2019.06.01
Tag:
        PullR:          all: 24         open: 17        opened: 7       closed: 5       merged: 4
        Issues:         all: 107        open: 79        opened: 28      closed: 21
        Stars:          all: 2582       Stars snapshot: 2529    Stars per period: 56
        Forks:          all: 850        Forks snapshot: 823     Forks per period: 28
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.06.01 2019.07.01
Tag:
        PullR:          all: 31         open: 18        opened: 13      closed: 13      merged: 9
        Issues:         all: 112        open: 84        opened: 28      closed: 32
        Stars:          all: 2652       Stars snapshot: 2582    Stars per period: 71
        Forks:          all: 877        Forks snapshot: 850     Forks per period: 27
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.07.01 2019.08.01
Tag:
        PullR:          all: 34         open: 17        opened: 17      closed: 18      merged: 10
        Issues:         all: 108        open: 79        opened: 29      closed: 33
        Stars:          all: 2719       Stars snapshot: 2652    Stars per period: 70
        Forks:          all: 901        Forks snapshot: 877     Forks per period: 27
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.08.01 2019.09.01
Tag:
        PullR:          all: 26         open: 16        opened: 10      closed: 16      merged: 10
        Issues:         all: 101        open: 75        opened: 25      closed: 41
        Stars:          all: 2779       Stars snapshot: 2719    Stars per period: 63
        Forks:          all: 919        Forks snapshot: 901     Forks per period: 18
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.09.01 2019.10.01
Tag:
        PullR:          all: 21         open: 9         opened: 11      closed: 12      merged: 8
        Issues:         all: 83         open: 58        opened: 24      closed: 27
        Stars:          all: 2879       Stars snapshot: 2779    Stars per period: 102
        Forks:          all: 943        Forks snapshot: 919     Forks per period: 25
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.10.01 2019.11.01
Tag:
        PullR:          all: 10         open: 9         opened: 1       closed: 0       merged: 0
        Issues:         all: 61         open: 55        opened: 5       closed: 1
        Stars:          all: 2883       Stars snapshot: 2879    Stars per period: 8
        Forks:          all: 945        Forks snapshot: 943     Forks per period: 3
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.11.01 2019.12.01
Tag:
        PullR:          all: 10         open: 10        opened: 0       closed: 0       merged: 0
        Issues:         all: 60         open: 60        opened: 0       closed: 0
        Stars:          all: 2883       Stars snapshot: 2883    Stars per period: 0
        Forks:          all: 945        Forks snapshot: 945     Forks per period: 0
        Traffic:        Visitors unique: -1     Cloners unique: -1

Period: 2019.12.01 2020.01.01
Tag:
        PullR:          all: 10         open: 10        opened: 0       closed: 0       merged: 0
        Issues:         all: 60         open: 60        opened: 0       closed: 0
        Stars:          all: 2883       Stars snapshot: 2883    Stars per period: 0
        Forks:          all: 945        Forks snapshot: 945     Forks per period: 0
        Traffic:        Visitors unique: -1     Cloners unique: -1
```
</details>

### Вариант 2. Releases tags

#### using username + password

```
python github_stats.py -u golubevdmi -pw GITHUB_PASSWORD -r pygithub/pygithub -p v1.43.8 v1.43.7 v1.40a3 v1.39 -ocv -csv -gdoc
```

#### or user token

```
python github_stats.py -u GITHUB_TOKEN -r pygithub/pygithub -p v1.43.8 v1.43.7 v1.40a3 v1.39 -ocv -csv -gdoc
```

<details>
 <summary>Вывод статистики по тэгам v1.43.8 v1.43.7 v1.40a3 v1.39 (репо pygithub/pygithub):</summary>

```
Parsed dates:
         2018-04-10  -  2018-04-17 v1.39
         2018-04-26  -  2018-06-26 v1.40a3
         2019-04-16  -  2019-07-20 v1.43.7
         2019-07-20  -  2019-10-03 v1.43.8
>> get metric: 2018-04-10  -  2018-04-17
>> get metric: 2018-04-26  -  2018-06-26
>> get metric: 2019-04-16  -  2019-07-20
>> get metric: 2019-07-20  -  2019-10-03

Period: 2018.04.10 2018.06.26
Tag: v1.39_v1.40a3
        PullR:          all: 38         open: -5        opened: 22      closed: 12      merged: 9
        Issues:         all: -22        open: -13       opened: 46      closed: 37
        Stars:          all: 124        Stars snapshot: 23      Stars per period: 101
        Forks:          all: 50         Forks snapshot: 13      Forks per period: 37
        Traffic:        Visitors unique: 0      Cloners unique: 0

Period: 2018.04.26 2019.07.20
Tag: v1.40a3_v1.43.7
        PullR:          all: 13         open: -15       opened: 9       closed: 12      merged: 7
        Issues:         all: -32        open: -33       opened: 28      closed: 29
        Stars:          all: 843        Stars snapshot: 734     Stars per period: 109
        Forks:          all: 289        Forks snapshot: 240     Forks per period: 49
        Traffic:        Visitors unique: 0      Cloners unique: 0

Period: 2019.04.16 2019.10.03
Tag: v1.43.7_v1.43.8
        PullR:          all: -15        open: 3         opened: -12     closed: -3      merged: -3
        Issues:         all: 19         open: 2         opened: -24     closed: -7
        Stars:          all: 196        Stars snapshot: 221     Stars per period: -25
        Forks:          all: 51         Forks snapshot: 92      Forks per period: -41
        Traffic:        Visitors unique: 0      Cloners unique: 0

```
</details>

### export opencv format

Выполняется с помощью команды `-ocv` или `--export_opencv`. Конечный файл сохраняется под именем `[period_dates_or_tags].yml`
Пример выходного файла, полученного с репозитория [PyGithub пользователя PyGithub](https://github.com/PyGithub/PyGithub), можно увидеть в папке [doc](docs/)

### export csv

Выполняется с помощью команды `-csv` или `--export_csv`. Конечный файл сохраняется под именем `[period_dates_or_tags].csv`
Пример выходного файла, полученного с репозитория [PyGithub пользователя PyGithub](https://github.com/PyGithub/PyGithub), можно увидеть в папке [doc](docs/)

### export google docs

Выполняется с помощью команды `-gdoc` или `--export_gdoc`. Загружает сгенерированный файл .csv в облако. Требует авторизацию и разрешение на запись. [Пример выходного файла](https://drive.google.com/open?id=1m424wFSBnwKlGnT45dE3Dhe4zjBIWEqI), полученного со статистики репозитория [pcapplusplus пользователя seladb](https://github.com/seladb/pcapplusplus).


## Примечания

**Количество уникальных посетителей и людей, загрузивших репозиторий, доступно только автору или соавторам репозитория. Данная статистика может быть получена только за последние две недели*
