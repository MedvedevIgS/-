import os
import sqlite3
os.chdir('c:\\Medvedev\\НИР\\')




def menu1(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2):
    """Функция реализующая вывод таблиц из БД"""
    menu1v=input('\n1) vuzkart\n2) vuzstat\nВыберете таблицу для вывода: ')
    while True:
        if menu1v.isnumeric() and int(menu1v)<=2 and int(menu1v)>0:
            break
        else:
            menu1v=input('Пожалуйста введите цифру от 1 до 2: ')
    if menu1v=='1':
        g=''
        for i in range(len(Shead1)):
            t=str(Shead1[i])
            k=0
            while True:
                if len(t)<16-k:
                    t+='  '
                    k+=1
                else:
                    break
            g=g+t+'\t'
        print(g)
        for i in range(len(tabl1)):
            g=''
            for j in range(len(tabl1[i])):
                if len(str(tabl1[i][j]))>=16:
                    g=g+str(tabl1[i][j][:13])+'...\t'
                else:
                    t=str(tabl1[i][j])
                    k=0
                    while True:
                        if len(t)<16-k:
                            t+='  '
                            k+=1
                        else:
                            break
                    g=g+t+'\t'
            print(g)
    elif menu1v=='2':
        g=''
        for i in range(len(Shead2)):
            g=g+str(Shead2[i])+'\t'
        print(g)
        for i in range(len(tabl2)):
            g=''
            for j in range(len(tabl2[i])):
                g=g+str(tabl2[i][j])+'\t'
            print(g)
    return mainmenu(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)





def menu2(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2):
    """Функция составляющая и отображающая на экране перечень полных наименований вузов, в которых
    количество студентов больше или равно введеному пороговому значению"""
    con = sqlite3.connect(Namebd)
    cur = con.cursor()
    sql="SELECT stud FROM vuzstat"
    data = cur.execute(sql).fetchall()
    cur.close()
    con.close()
    minbord=min(data)[0]
    maxbord=max(data)[0]
    print('Введите пороговое значение количества студентов в вузе\nМинимальное количество студентов '+str(minbord)+'\nМаксимальное количество студентов '+str(maxbord))
    bord=input('Пороговое значение: ')
    while True:
        if bord.isnumeric():
            break
        else:
            bord=input('Введите число: ')
    while True:
        bord=int(bord)
        if bord>maxbord or bord<minbord:
            bord=input('Введенное число не должно быть больше максимального значения\nи не должно быть меньше минимального значения\nПопробуйте ещё раз: ')
        else:
            break
    con = sqlite3.connect(Namebd)
    cur = con.cursor()
    sql="SELECT a.z1 FROM vuzkart as a, vuzstat as b ON a.codvuz=b.codvuz WHERE b.stud>={}".format(bord)
    data = cur.execute(sql).fetchall()
    cur.close()
    con.close()
    print('\nПеречень вузов, удовлетворяющих заданное условие\n')
    for i in range(len(data)):
        print(data[i][0])
    return mainmenu(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)





    

def menu3(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2):
    """Функция реализующая рассчет и представление в виде таблицы распределения
    процента преподавателей-профессоров, по статусам вузов"""
    con = sqlite3.connect(Namebd)
    cur = con.cursor()
    sql = 'SELECT a.status FROM vuzkart as a,vuzstat as b ON a.codvuz=b.codvuz'
    data = cur.execute(sql).fetchall()
    cur.close()
    con.close()
    data=list(set(data))
    S1=0
    S2=0
    print('\nПорядковый номер\tСтатус          \tКоличество преподователей\tКоличество профессоров\tПроцент от oбщего числа')
    for i in range(len(data)):
        con = sqlite3.connect(Namebd)
        cur = con.cursor()
        sql = 'SELECT b.PPS FROM vuzkart as a,vuzstat as b ON a.codvuz=b.codvuz WHERE a.status="{}"' .format(data[i][0])
        pps=cur.execute(sql).fetchall()
        sql = 'SELECT b.PR FROM vuzkart as a,vuzstat as b ON a.codvuz=b.codvuz WHERE a.status="{}"' .format(data[i][0])
        pr=cur.execute(sql).fetchall()
        cur.close()
        con.close()
        allpps=0
        for j in range(len(pps)):
            allpps+=pps[j][0]
        allpr=0
        for j in range(len(pr)):
            allpr+=pr[j][0]
        print(str(i+1)+'                                \t'+str(data[i][0])+'\t'+str(allpps)+'                                        \t'+str(allpr)+'                                  \t'+str(round((allpr/allpps)*100,3))+'%')
        S1+=allpps
        S2+=allpr
    print('                                  \tИтог               \t'+str(S1)+'                                        \t'+str(S2)+'                                  \t'+str(round((S2/S1)*100,3))+'%')
    return mainmenu(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)
    
    





def mainmenu(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2):
    """Главное меню программы"""
    print('\n1) Отображение БД в виде таблицы\n2) Выбрать пороговое значение количества студентов\n3) Рассчитать и представить в виде таблицы распределение процента преподавателей-профессоров, по статусам вузов\n4) Завершение работы')
    menuv=input('\nВыберете функцию (введите соответствующее число): ')
    while True:
        if menuv.isnumeric() and int(menuv)<=4 and int(menuv)>0:
            break
        else:
            menuv=input('Пожалуйста введите цифру от 1 до 4: ')
    if menuv=='1':
        menu1(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)
    elif menuv=='2':
        menu2(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)
    elif menuv=='3':
        menu3(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)
    elif menuv=='4':
        return(print('\nКонец работы'))




Namebd=input('Введите имя БД с которой собираетесь работать: ')

while True:
    if os.path.isfile(Namebd):
        break
    else:
        Namebd=input('Такого файла не существует! Введите другое имя: ')

con = sqlite3.connect(Namebd)
cur = con.cursor()



Ntabl1=cur.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table'").fetchall()[2][0]
cur.execute('SELECT * FROM {}'.format(Ntabl1))

Shead1 = tuple(description[0] for description in cur.description)
sql = 'SELECT * FROM {}'.format(Ntabl1)
tabl1 = cur.execute(sql).fetchall()




Ntabl2=cur.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table'").fetchall()[1][0]
cur.execute('SELECT * FROM {}'.format(Ntabl2))

Shead2 = tuple(description[0] for description in cur.description)
sql = 'SELECT * FROM {}'.format(Ntabl2)
tabl2 = cur.execute(sql).fetchall()



cur.close()
con.close()

mainmenu(tabl1,Ntabl1,Namebd,Shead1, tabl2, Ntabl2, Shead2)
