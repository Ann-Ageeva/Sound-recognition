&nbsp;
<center>


|  Согласовано                         | Утверждаю   |
|:----------------                     |:-------------|
|Доцент кафедры                        |Профессор кафедры
|ИАНИ ННГУ, к.ф.-м.н.                  |  ИАНИ ННГУ, к.ф.-м.н.              | 
|______________ С. Липкин              |______________ Н.В. Старостин       |
|"____" _______________ 2020 г. &nbsp; |"____" _______________ 2020 г.&nbsp;|

<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>

# Пояснительная записка 
**"Разработка алгоритма определения местоположения дрона"**

**научно-исследовательская работа** 

 **"DRONE SOUND DETECTION"**
 
 **(Шифр ПО "__________")**

 <p>&nbsp;</p>
 <p>&nbsp;</p>
 <p align="right">Ответственный исполнитель</p>
 <p align="right">_______________ Агеева А.</p>
 <p align="right">_______________ Ващук Н.</p>
 <p align="right">_______________ Мячев А.</p>
 <p>&nbsp;</p>
 <p>&nbsp;</p>
 <p>&nbsp;</p>
 <p>&nbsp;</p>
 
 Нижний Новгород 2020 г.
</center>

<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>


## Содержание

1. **Общее описание алгоритма**
	1. Назначение алгоритма
	2. Теоретическое описание алгоритма
2. **Реализация алгоритма**
	1. Описание компонентов алгоритма
	2. Детали реализации алгоритма
3. **Тестирование**
    1. Методы проведения тестирования
    2. Результаты тестирования
4. **Интеграция алгоритма с нейронной сетью**
5. **Листинг алгоритма**
6. **Библиографический список**
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>


## 1. Общее описание алгоритма
### 1.1 Назначение алгоритма
Разработанный алгоритм служит для определения местоположения дрона. Входные данные для алгоритма поступают в виде монофонических аудиофайлов с двух микрофонов в формате wav.Выходные данные алгоритма представляют собой угол от 0 до 180 градусов, рассчитанный относительно оси симметрии между двумя микрофонами.
### 1.2 Теоретическое описание алгоритма
Рассматривается система координат, связанная с парой микрофонов. Микрофоны расположены на одной оси (OX), на одинаковом расстоянии от центра оси. Система принимает звуковой сигнал, который расположен на расстоянии d1 от первого микрофона и на расстоянии d2 от второго. По показаниям микрофонов можно определить разность расстояний до источника звука. Геометрическое место точек, разность расстояний от которых до двух фиксированных точек равна константе - гипербола. 

Далее, с помощью уравнения гиперболы в декартовых координатах, вычисляется формула углового коэффициента асимптоты. 
Разность расстояний до источника звука в отсчётах вычисляется при помощи корреляционной функции. Смещение отсчёта, на котором достигается максимум корреляционной функции, от 0 принимается за разность расстояний в отсчетах. Перевод этого значения в метры осуществляется по формуле: a = pu/2F, где a - разность расстояний в метрах, p - разность расстояний в отсчётах, v = 330m - cкорость звука, F - частота дискретизации. 

Так как разность расстояний d не может превышать расстояния между микрофонами (2c), можно предположить,
что и максимум корреляционной функции будет находиться в ограниченном диапазоне [-L;L], где константа L зависит от расстояния между микрофонами. Таким образом,  корреляционная функция вычисляетс только для отсчётов из отрезка [-L;L].

Описанный алгоритм позволяет найти значение угла между осью, на которой расположены микрофоны, и прямой, соединяющей центр оси и источник звука. Угол лежит в диапозоне [-п/2;п/2]. Алгоритм не разделяет переднюю (относительно микрофонов) и заднюю полуплоскость, так как по рассмотренным измерениям невозможно однозначно восстановить угол.

## 2. Реализация алгоритма
### 2.1 Описание компонентов алгоритма
Алгоритм состоит из двух процедур:
1. *BaseAlg*
Процедура рассчитывает угол в градусах с помощью входных данных (аудиофайлов). Для расчета необходимо задать константные значения: диапозон маскимальной корреляции (maxRangeCor), скорость звука (u), частоту дискретизации (frequency) и расстояние между микрофонами (dist).
2. *difDist*
Процедура находит смещение сигнала между микрофонами относительно друг друга с помощью корреляции и входных данных (аудиофайлов). 
Дополнительно были использованы библиотеки: 
1. Librosa - для преобразования аудиофайлов из формата wav в numpyArray.
2. Numpy - для преобразования звуковой дорожки в ряд Фурье и некоторых математических операций.

### 2.2 Детали реализации алгоритма
Для настройки отладочной версии алгоритма необходимо наличие двух аудиофайлов в формате wav. Путь к ним следует указать в соответствующих переменных (*pathFirstMicro, pathSecondMicro*), а также скорректировать переменные *dist* (расстояние между микрофонами) и *frequency* (частота дискретизации).
Для настройки рабочей версии алгоритма необходимо также скорректировать переменные *dist* (расстояние между микрофонами) и *frequency* (частота дискретизации). Входные аудиофайлы передаются на вход нейронной сетью. 

## 3. Тестирование
### 3.1 Методы проведения тестирования
Для проведения начального тестирования необходимо записать тестовые аудиофайлы. Для этого два микрофона располагаются на одной оси и направляются в одну сторону. Чтобы получить корректные тестовые данные, различимые для алгоритма, следует выполнить несколько условий:
- существенное расстояние между микрофонами (не менее двух метров)
- отсутствие вблизи объектов, отражающих звуковые волны.
Таким образом, с соблюдением условий записываются два моно-аудиофайла в формате wav с помощью двухканальной аудиокарты и подаются на вход алгоритму. 

### 3.2 Результаты тестирования
Положительным результатом тестирования будет определение алгоритмом угла, близкого к значению реального тестового угла местоположения дрона. 

## 4. Интеграция алгоритма с нейронной сетью
Предполагается интеграция алгоритма с нейронной сетью. При обнаружении объекта нейронной сетью, отрезок аудиофайла, на котором был обнаружен объект, отправляется в качестве входных данных алгоритму для дальнейшего определения его местоположения.
## 5. Листинг алгоритма

import math as m

import numpy

from numpy.fft import rfft

import librosa

pathFirstMicro = ""

pathSecondMicro = ""


def baseAlg():
	
	maxRangeCor = 5500  # Диапозон маскимальной корреляции

    u = 330  # Скорость звука

    frequency = 22000  # Частота дискретизации

    dist = 100  # Расстояние между микрофонами

    angles = list()

    if difDist(maxRangeCor) > 0:
        angles.append(m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist)))
        angles.append(
            360 - m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist))
        )

    angles.append(180 - m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist)))
    angles.append(180 + m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist)))

    return angles


def difDist(l):

	x, sr = librosa.load(pathFirstMicro)
    leftSignalFurie = rfft(x)
    x, sr = librosa.load(pathSecondMicro)
    rightSignalFurie = rfft(x)
    best = 0
    dist = 0

    for i in range(1, l):
        corrCoeff = numpy.corrcoef(leftSignalFurie(i, l + i), rightSignalFurie(0, l))[
            0, 1
        ]
        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(1, l):
        corrCoeff = numpy.corrcoef(leftSignalFurie(0, l), rightSignalFurie(i, l + i))[
            0, 1
        ]
        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist


angles = baseAlg()
<p>&nbsp;</p>
<p>&nbsp;</p>

## 6. Библиографический список
1. Техническое задание на научно-исследовательскую работу “DRONE SOUND DETECTED”
2. Теоритическое описание алгоритма: https://docviewer.yandex.ru/view/333208841/?page=5&*=sqN366GGengnhYN3QJIzL2EEibR7InVybCI6Imh0dHA6Ly9zZS5tYXRoLnNwYnUucnUvU0UvWWVhcmx5UHJvamVjdHMvc3ByaW5nLTIwMTUvMzQ0LzM0NC1Nb2lzZWVua28tcmVwb3J0LnBkZiIsInRpdGxlIjoiMzQ0LU1vaXNlZW5rby1yZXBvcnQucGRmIiwibm9pZnJhbWUiOnRydWUsInVpZCI6IjMzMzIwODg0MSIsInRzIjoxNTg4NTMwMTMyODgwLCJ5dSI6IjU4NTMyMjQ1MTU1MDU4NzQ4OCIsInNlcnBQYXJhbXMiOiJsYW5nPXJ1JnRtPTE1ODI3MDU2NjMmdGxkPXJ1Jm5hbWU9MzQ0LU1vaXNlZW5rby1yZXBvcnQucGRmJnRleHQ9JUQwJUJFJUQwJUJGJUQxJTgwJUQwJUI1JUQwJUI0JUQwJUI1JUQwJUJCJUQwJUI1JUQwJUJEJUQwJUI4JUQwJUI1KyVEMCVCRCVEMCVCMCVEMCVCRiVEMSU4MCVEMCVCMCVEMCVCMiVEMCVCQiVEMCVCNSVEMCVCRCVEMCVCOCVEMSU4RislRDAlQjglRDElODElRDElODIlRDAlQkUlRDElODclRDAlQkQlRDAlQjglRDAlQkElRDAlQjArJUQwJUI3JUQwJUIyJUQxJTgzJUQwJUJBJUQwJUIwJnVybD1odHRwJTNBLy9zZS5tYXRoLnNwYnUucnUvU0UvWWVhcmx5UHJvamVjdHMvc3ByaW5nLTIwMTUvMzQ0LzM0NC1Nb2lzZWVua28tcmVwb3J0LnBkZiZscj00NyZtaW1lPXBkZiZsMTBuPXJ1JnNpZ249YjVhMGUyMDFlOTQ4Mjk5YzFkYWYxMTliNzZiOTY5YmYma2V5bm89MCJ9&lang=ru