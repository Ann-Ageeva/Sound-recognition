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
	2. Входные данные
	3. Выходные данные
2. **Описание модулей и процедур**
	1. Описание процедур
	2. Сторонние библиотеки
3. **Настройка отладочной версии алгоритма**
4. **Настройка рабочей версии алгоритма**
5. **Интеграция рабочей версии программы с нейронной сетью**
6. **Текст алгоритма**
7. **Библиографический список**
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>


## 1. Общее описание алгоритма
### 1.1 Назначение алгоритма
Разработанный алгоритм служит для определения местоположения дрона.
### 1.2 Входные данные
Входные данные для алгоритма поступают в виде монофонических аудиофайлов с двух микрофонов в формате wav.
### 1.3 Выходные данные
Выходные данные алгоритма представляют собой угол от 0 до 180 градусов, рассчитанный относительно оси симметрии между двумя микрофонами.
## 2. Описание модулей и процедур
### 2.1 Описание процедур
Алгоритм состоит из двух процедур:
1. *BaseAlg*
Процедура рассчитывает угол в градусах с помощью входных данных (аудиофайлов). Для расчета необходимо задать константные значения: диапозон маскимальной корреляции (maxRangeCor), скорость звука (u), частоту дискретизации (frequency) и расстояние между микрофонами (dist).
2. *difDist*
Процедура находит смещение сигнала между микрофонами относительно друг друга с помощью корреляции и входных данных (аудиофайлов). 
### 2.2 Сторонние библиотеки
Дополнительно были использованы библиотеки: 
1. Librosa - для преобразования аудиофайлов из формата wav в numpyArray.
2. Numpy - для преобразования звуковой дорожки в ряд Фурье и некоторых математических операций.
## 3. Настройка отладочной версии алгоритма
Для настройки отладочной версии алгоритма необходимо наличие двух аудиофайлов в формате wav. Путь к ним следует указать в соответствующих переменных (*pathFirstMicro, pathSecondMicro*), а также скорректировать переменные *dist* (расстояние между микрофонами) и *frequency* (частота дискретизации).
## 4. Настройка рабочей версии алгоритма
Для настройки рабочей версии алгоритма необходимо скорректировать переменные *dist* (расстояние между микрофонами) и *frequency* (частота дискретизации). 
## 5. Интеграция рабочей версии программы с нейронной сетью
Предполагается интеграция алгоритма с нейронной сетью. При обнаружении объекта нейронной сетью, отрезок аудиофайла, на котором был обнаружен объект, отправляется в качестве входных данных алгоритму для дальнейшего определения его местоположения.
## 6. Текст алгоритма

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

## 7. Библиографический список
1. Техническое задание на научно-исследовательскую работу “DRONE SOUND DETECTED”
2. Теоритическое описание алгоритма: https://docviewer.yandex.ru/view/333208841/?page=5&*=sqN366GGengnhYN3QJIzL2EEibR7InVybCI6Imh0dHA6Ly9zZS5tYXRoLnNwYnUucnUvU0UvWWVhcmx5UHJvamVjdHMvc3ByaW5nLTIwMTUvMzQ0LzM0NC1Nb2lzZWVua28tcmVwb3J0LnBkZiIsInRpdGxlIjoiMzQ0LU1vaXNlZW5rby1yZXBvcnQucGRmIiwibm9pZnJhbWUiOnRydWUsInVpZCI6IjMzMzIwODg0MSIsInRzIjoxNTg4NTMwMTMyODgwLCJ5dSI6IjU4NTMyMjQ1MTU1MDU4NzQ4OCIsInNlcnBQYXJhbXMiOiJsYW5nPXJ1JnRtPTE1ODI3MDU2NjMmdGxkPXJ1Jm5hbWU9MzQ0LU1vaXNlZW5rby1yZXBvcnQucGRmJnRleHQ9JUQwJUJFJUQwJUJGJUQxJTgwJUQwJUI1JUQwJUI0JUQwJUI1JUQwJUJCJUQwJUI1JUQwJUJEJUQwJUI4JUQwJUI1KyVEMCVCRCVEMCVCMCVEMCVCRiVEMSU4MCVEMCVCMCVEMCVCMiVEMCVCQiVEMCVCNSVEMCVCRCVEMCVCOCVEMSU4RislRDAlQjglRDElODElRDElODIlRDAlQkUlRDElODclRDAlQkQlRDAlQjglRDAlQkElRDAlQjArJUQwJUI3JUQwJUIyJUQxJTgzJUQwJUJBJUQwJUIwJnVybD1odHRwJTNBLy9zZS5tYXRoLnNwYnUucnUvU0UvWWVhcmx5UHJvamVjdHMvc3ByaW5nLTIwMTUvMzQ0LzM0NC1Nb2lzZWVua28tcmVwb3J0LnBkZiZscj00NyZtaW1lPXBkZiZsMTBuPXJ1JnNpZ249YjVhMGUyMDFlOTQ4Mjk5YzFkYWYxMTliNzZiOTY5YmYma2V5bm89MCJ9&lang=ru