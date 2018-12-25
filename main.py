import math
import json
class Movie:  # фильм
    id = ''
    rate = ''

class Metrics: # метрика
    id = ''
    sim = ''

class User: # пользователь
    id = ''
    movies_rates = []
    sim_users = []
    avg_rate = ''

class SimUser:
    id = ''
    movies_rates = []
    sim = ''
    avg_rate = ''

Users = []
SimUsers = []
userId = int(input('Введите id пользователя, для которого требуется рассчитать оценки '))
for x in range(40):  # заполняем поле id
    Users.append(User())
    Users[x].id = x + 1

k = -1
b = []
file = open('data.csv')  # заполняем поле movies_rates (оценки пользователя)
for line in file: # построчно считываем файл
    if line.startswith('User'):
        k = k + 1
        line = line[8:-1]  # обрезаем слово User и его номер и символ перехода на новую строку
        b = line.split(',')
        Users[k].movies_rates = Users[k].movies_rates[:]
        for i in range(30):
            Users[k].movies_rates.append(Movie())
            Users[k].movies_rates[i].id = i+1
            Users[k].movies_rates[i].rate = b[i]

for i in range(40):  # преобразуем оценки в тип int и считаем среднее
    summ = 0
    d = 0
    for j in range(30):
        Users[i].movies_rates[j].rate = int(Users[i].movies_rates[j].rate)
        if Users[i].movies_rates[j].rate != -1:
            summ += Users[i].movies_rates[j].rate
            d = d+1
    Users[i].avg_rate = round(summ/d, 3)


for i in range(40): # составляем метрику сходства
    Users[i].sim_users = Users[i].sim_users[:]
    for j in range(40):
        s = 0
        sq1 = 0
        sq2 = 0
        for k in range(30):
            Users[i].sim_users.append(Metrics())
            Users[i].sim_users[j].id = j + 1
            if Users[i].movies_rates[k].rate != -1 and Users[j].movies_rates[k].rate != -1 and i!=j:
                 s += Users[i].movies_rates[k].rate * Users[j].movies_rates[k].rate
                 sq1 += math.pow(Users[i].movies_rates[k].rate, 2)
                 sq2 += math.pow(Users[j].movies_rates[k].rate, 2)
                 Users[i].sim_users[j].sim = round(s/(math.sqrt(sq1)*math.sqrt(sq2)), 3)
            else:
                 Users[i].sim_users[j].sim = 0

for k in range(40): # сортировка значений метрики
    for i in range(40):
        for j in range(40):
          if Users[k].sim_users[i].sim > Users[k].sim_users[j].sim:
              t = Users[k].sim_users[i]
              Users[k].sim_users[i] = Users[k].sim_users[j]
              Users[k].sim_users[j] = t

for k in range(7):
    SimUsers.append(SimUser())
    SimUsers[k].id = Users[userId-1].sim_users[k].id
    SimUsers[k].sim = Users[userId - 1].sim_users[k].sim
    for x in range(40):
        if Users[x].id == SimUsers[k].id:
            SimUsers[k].avg_rate = Users[x].avg_rate
            SimUsers[k].movies_rates = Users[x].movies_rates

exp_rate = []
counter = -1
for k in range(30): # расчет оценок
    summ1 = 0
    summ2 = 0
    if Users[userId -1].movies_rates[k].rate == -1:
       counter = counter + 1;
       exp_rate.append(Movie())
       exp_rate[counter].id = k + 1
       for n in range (7):
           summ1 += Users[userId -1].sim_users[n].sim * (SimUsers[n].movies_rates[k].rate - SimUsers[n].avg_rate)
           summ2 += Users[userId -1].sim_users[n].sim
       exp_rate[counter].rate = round( Users[userId - 1].avg_rate + summ1/summ2, 3)
result = []
place = []
for i in range(30):
    place.append(0);
file = open('context_place.csv')
for line in file: # построчно считываем файл
    if line.startswith('User'):
        k = k + 1
        line = line[8:-1]  # обрезаем слово User и его номер и символ перехода на новую строку
        b = line.split(',')
        for i in range(30):
           if b[i] == ' h':
               place[i] = place[i] + 1

day = []
for i in range(30):
    day.append(0);
file = open('context_day.csv')
for line in file: # построчно считываем файл
    if line.startswith('User'):
        k = k + 1
        line = line[8:-1]  # обрезаем слово User и его номер и символ перехода на новую строку
        b = line.split(',')
        for i in range(30):
           if b[i] == ' Sat' or b[i] ==' Sun':
               day[i] = day[i] + 1

RecMovies = []
for i in range(30):
    RecMovies.append(Movie())
    RecMovies[i].id = i+1
    RecMovies[i].rate = place[i] + day[i]

for k in range(30): # сортировка рекомендаций
    for i in range(30):
          if RecMovies[i].rate > RecMovies[k].rate:
              t = RecMovies[i]
              RecMovies[i] = RecMovies[k]
              RecMovies[k] = t

for k in range(30):
    for i in exp_rate:
      if RecMovies[k].id == i.id and i.rate > 2:
          RecMovie = i.id

print ('Рекомендуемый фильм ',RecMovie)
for k in exp_rate:
        result.append ({
        "film": k.id ,
        "rate ": k.rate})
        print('фильм ', k.id ,' оценка ' ,k.rate);
result.append({"recommend_film": RecMovie })
with open('result.json', 'w') as outfile:
        json.dump(result, outfile);