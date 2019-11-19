
def checklink_access(data):
    import requests
    import urllib.request
    import urllib.parse
    import time
    import sys
    import pymongo
    conn = pymongo.MongoClient('localhost', 27017)
#    conn = pymongo.MongoClient('mongo', 27017)
    db = conn['robots_txt_parcer']
    coll = db['links']


    db_input_link = '' 
    db_robots_txt_link = '' 
    db_status_to_fetcher = ''
    db_last_visit_time = ''
    db_cash_robots_txt = ''


    start_time = time.time()


    # целевая переменная нашего парсера robots.txt вернуть ответ TRUE or FALSE в фетчер по полученной ссылке
    robot_txt_result = '-'

    # в этом месте должен быть код gRPC server посылающего запрос к gRPC server блока 'ML блок' 
    # на получение каноникализированной ссылки


    # зона ссылок для тестирования

    # input_url = 'https://habr.com/ru/post/467607/'
    # input_url = 'http://qaru.site/questions/16012/split-strings-with-multiple-delimiters'
    # input_url = 'https://e.mail.ru/messages/inbox/'
    # input_url = 'https://yandex.ru/ugcpub/cabinet'
    # input_url = 'https://yandex.ru/blog/AAA?tag=AA'
    # input_url = 'http://www.google/'
    # input_url = 
    # input_url = 
    # input_url = 
    # input_url = 
    input_url = data


    db_input_link = input_url



    # из полученной ссылки выделяем корневой каталог с доменом и добавляем к нему окончание '/robots.txt'
    x = urllib.parse.urlparse(input_url)[0]
    y = urllib.parse.urlparse(input_url)[1]
    url_box = x + '://' + y + '/robots.txt' 
    url_box 

    db_robots_txt_link = url_box



    # в данноме месте тестим сигнал ссылки к robots.txt. 
    # и все ответы отличные от '200' воспринимаем как False. Даем фетчеру ответ не ходить по этой ссылке
    # т.к. мы не смогли понять правила работы с сайтом
    # и поскольку robots.txt не скачали то по данной ссылке завершаем задачу этого парсера.

    # так же в ходе разработки столкнулся с тем что вылетает ошибка при попытке подключиться к файлу robots.txt
    # например к сайту google.com. В ходе попытки код обваливался.
    # поставил в данном месте связку try-except и в случае 'обавала кода' передаем в целевую 
    # переменную 'robot_txt_result' 'False'

        
    try:
        test_channel = str(requests.get(url_box))[-5:-2]
        if test_channel != '200':
            robot_txt_result = 'False' 
        elif test_channel == '200':
            try:
                robots_txt = urllib.request.urlopen(url_box).read()
                robots_txt = robots_txt.decode('utf-8')
                robots_txt_2 = robots_txt.split('\n')
                robots_txt_2
            except Exception:
                robot_txt_result = 'False'
    except Exception:
        robot_txt_result = 'False'
        
    if robot_txt_result == 'False':
        db_status_to_fetcher = robot_txt_result
        db_cash_robots_txt = 'NaN'
        row_for_db = {'db_input_link':db_input_link, 
                  'db_robots_txt_link':db_robots_txt_link,
                  'db_status_to_fetcher': db_status_to_fetcher,
                  'db_cash_robots_txt':db_cash_robots_txt 
                 }
        coll.save(row_for_db)
        
        result = robot_txt_result
        return result
   
    
    elif robot_txt_result == '-':
        robot_list = []
        counter = -1
        for i in range(len(robots_txt_2)):
            robots_txt_3 = robots_txt_2[i].split(' ')[0]
            if robots_txt_3 == 'User-agent:' or robots_txt_3 == 'User-Agent:': 
                robot_list.append([('User-agent;',robots_txt_2[i].split(' ')[1]),['Crawl-delay:'],['Allow:'],['Disallow:']])
                counter += 1
            elif robots_txt_3 == 'Crawl-delay:':
                robot_list[counter][1].append(robots_txt_2[i].split(' ')[1])
            elif robots_txt_3 == 'Allow:':
                robot_list[counter][2].append(robots_txt_2[i].split(' ')[1])
            elif robots_txt_3 == 'Disallow:':
                robot_list[counter][3].append(robots_txt_2[i].split(' ')[1])
            else:
                continue
    
    
        # перебираем роли что удалось получить в robots.txt
        # если есть подходящая роль для нас то записываем ее в rules_list
        
        rules_list = []
        for i in range(len(robot_list)):
            if robot_list[i][0][1] == '*':
                rules_list = robot_list[i]
            else:
                continue
            
        # если подходящую роль не нашли то по умолчанию считаем что для нас запретов нет
        if len(rules_list) == 0:
            robot_txt_result = 'True'
               
        if robot_txt_result == 'True':
            db_status_to_fetcher = robot_txt_result
            db_cash_robots_txt = robots_txt 
            
            row_for_db = {'db_input_link':db_input_link, 
                      'db_robots_txt_link':db_robots_txt_link,
                      'db_status_to_fetcher': db_status_to_fetcher,
                      'db_cash_robots_txt':db_cash_robots_txt 
                     }
            coll.save(row_for_db)
            # код для добавления значения 0 в Crawl-fвlay для тех случаев когда 
            #  данное значение в robots.txt не было указано.
            if len(rules_list[1]) == 1:
                rules_list[1].append('0')
                
            result = robot_txt_result
            return result
            
       
        elif robot_txt_result == '-':
        
        
            # далее проверить нашу ссылку полученную на входе с доступной моделью поведения
            # и в случае если найдет подходящюю роль, то пропустит исходну ссылку дальше
            # если же не найдет, то "условно считаем что запретов нет и делаем целевую переменную True"
        
        
        
            # задумка в том чтобы сначала разделить правила на те что содержат спец символы и те что не содержат
            # далее те что содержат спец символы разделить правило по спец символам
            # сложить полученые части в список
            # по полученным частям проверить где в нашей ссылке есть указаные части (индексы этих частей). 
            # далее проверяем чтобы в случае если один более коротки паттерн вошел в соства другого
            # более длинного паттерна, выявляем и удаляем 
            # В итоге получаем два списка в котором учтен порядок частей шаблона с порядком символов в ссылке
            # На финальном шаге проверяем наличие маски паттерна правила с полученным итоговым списком положений
            # паттернов в нашей ссылке
        
        
            # функция которая проверяет наличие спец символов в правиле и распределяет на списки с символом и без
            def check_or_not_check (list_with_rules,t):
                check_list = []
                simple_list = []
                for i in range(len(list_with_rules[t])):
                    checker_1 = list_with_rules[t][i].split('*')
                    checker_2 = list_with_rules[t][i].split('?')
                    if len(checker_1) > 1 or len(checker_2) > 1:
                        check_list.append(list_with_rules[t][i])
                    else:
                        simple_list.append(list_with_rules[t][i])
                return(check_list, simple_list)
        
        
            # проверяем наличие спец символов в правилах allow и выделяем в отдельный список
            check_allow = check_or_not_check(rules_list,2)[0]
            simple_allow = check_or_not_check(rules_list,2)[1]
        
            # проверяем наличие спец символов в правилах disallow и выделяем в отдельный список
            check_disallow = check_or_not_check(rules_list,3)[0]
            simple_disallow = check_or_not_check(rules_list,3)[1]
        
        
        
            # функция в которой разбираю ссылки со спецсимволами на части
            # проверяю есть в нашей ссылке все полученные части после разбивки
            # проверяю все ли полученные части в том порядке в котором они в правиле есть ли они в таком же порядке в ссылке
        
            def spec_symbol_checker(list_of_check,t):
                # list_of_check это список с правилами, t позиция в этом списке (далее подставляется итератором)
                # делаю копию ссылки. 
                link = input_url
                # ========================================================
                
                
                # поэлементо делаем присвоение рабочей переменной и запускаем дальше в работу
                cc = list_of_check[t]
                # ========================================================
        
        
                # разбиваю правило на части по '*'
                clean = cc
                clean = clean.split('*')
                # ========================================================
        
                # в данном блоке выполняю первую проверку правила а именно:
                # проверяю все части правила, разбитого по '*' на наличие в исходной ссылке
                # если все части фигурируют в ссылке то первая проверка пройдена   
                len_clean_check = 0
                for i in range (len(clean)):
                    if clean[i] in link:
                        len_clean_check += 1
                    else:
                        continue
                
                temp_marker_1 = 0
                if len_clean_check < len(clean):
                    temp_marker_1 = -1
                else:
                    temp_marker_1 = 1
                # ========================================================
        
        
                # Разбиваю ссылки на части. в качестве сплита использую элементы правила
                # считаю длинну каждого кусочка и тем самым узнаю положение паттерна из правила в ссылке
                link_list = []
                marker_list = []
                for i in range (len(clean)):
                    if clean[i] == '/' or clean[i] == '':
                        continue
                    else:
                        link_2 = link
                        link_2 = link_2.split(clean[i])
                        link_list.append(link_2)
                        marker_list.append(clean[i])
                # ========================================================
        
        
        
                # суммирую длинны интервалов и записываю в отдельный список. 
                # получиться список с реальным стартовым положением паттернов правил
                # так же в цикле в виде дробной части с емкостью от 1 до 99 элементов
                # добавил к какой части паттерна правила относиться позиция элемента в ссылке
                position = []
                for j in range (len(link_list)):
                    posi = 0
                    order_marker = ((j+1)/100)
                    for i in range (len(link_list[j])):
                        posi += len(link_list[j][i]) + order_marker
                        position.append(float('{:.2f}'.format(posi+1)))
                        posi += len(marker_list[j]) - order_marker
        
                    if position[-1] > len(link):
                        position.remove(position[-1])   
        
                position.sort()
                # ========================================================
        
        
                # получил список в котором указаны номера паттернов в том же порядке что расположения паттернов в ссылке
                fin_order_list = []
                for i in range(len(position)):
                    fin_order_list.append((round((position[i]-int(position[i]))*100))-1)
                # ========================================================
        
        
                # скопировал для дальнейшей работы список с position
                # завел два пустых списка в которые буду складывать перемаркированные значения номеров позиций и паттернов
                position_2 = position
                out_list_position = []
                out_fin_order = []
                bag = 0
                for i in range (len(position_2)):
                    temp_1 = float(len(marker_list[fin_order_list[i]])-1)
                    temp_2 = 0
                    if i == len(position_2)-1:
                        out_list_position.append(position_2[i])
                        out_fin_order.append(fin_order_list[i])
                    else:
                        temp_2 = position_2[i] + temp_1
                        if temp_2 > position_2[i+1]:
                            out_list_position.append(position_2[i])
                            out_fin_order.append(fin_order_list[i])
                            bag = 1000
                        else:
                            out_list_position.append(position_2[i]+ bag)
                            out_fin_order.append(fin_order_list[i]+ bag) 
                            bag = 0
                # ========================================================
        
        
                # очистил список от задвоенных включений
                out_fin_order_2 = []
                for i in range(len(out_fin_order)):
                    if out_fin_order[i] > 999:
                        continue
                    else:
                        out_fin_order_2.append((round((out_list_position[i]-int(out_list_position[i]))*100))-1)
                out_fin_order_2
                # ========================================================
        
        
                # собрал список с номерами паттернов чтобы использовать как маску
                mask_list = []
                for i in range (len(marker_list)):
                    mask_list.append(i)
                # ========================================================
        
        
                # делаю окно размером mask_list. прохожусь этим окном по выходному списку номеров паттернов в out_fin_order
                # и проверяю есть ли в моем выходном списке порядок значений соответствующих маске.
                decision_1 = 0
                for i in range (len(out_fin_order_2)-(len(mask_list)-1)):
                    window_1 = out_fin_order_2[i:(len(mask_list))+i]
                    if window_1 == mask_list:
                        decision_1 +=  1
                    else:
                        decision_1 = decision_1
            #     if decision_1 > 0:
            #         print(True)
            #     else:
            #         print(False)
                # ========================================================
                fin_decision = decision_1 * temp_marker_1
                
                return fin_decision
        
        
        
            # проверяю простой список разрешений (в котором не было спец символов) 
            # в результате проверки получаю список кортежей в которых проверяемое условие и положение в ссылке
            # в случае если в ссылке нет то возвращает значени '-1'
            true_simple_allow = []
            for i in range (len(simple_allow)):
                index = input_url.find(simple_allow[i])
                
                if index > 0:
                    true_simple_allow.append(simple_allow[i])
                else:
                    continue
            #    true_simple_allow
        
        
        
            # проверяю простой список запретов (в котором не было спец символов)
            # в результате проверки получаю список кортежей в которых проверяемое условие и положение в ссылке
            # в случае если в ссылке нет то возвращает значени '-1'
            true_simple_disallow = []
            for i in range (len(simple_disallow)):
                index = input_url.find(simple_disallow[i])
                if index > 0:
                    true_simple_disallow.append(simple_disallow[i])
                else:
                    continue
            #    true_simple_disallow
        
        
            true_check_disallow = []
            for i in range (len(check_disallow)):
                check_result = spec_symbol_checker(check_disallow,i)
                if check_result > 0:
                    true_check_disallow.append(check_disallow[i])
                else:
                    continue
        
            #    true_check_disallow
        
        
            transition_list = []
            for i in range (len(true_check_disallow)):
                tt = len(true_check_disallow[i]),'d', true_check_disallow[i]
                transition_list.append(tt)
            #    transition_list
        
        
            true_check_allow = []
            for i in range (len(check_allow)):
                check_result = spec_symbol_checker(check_allow,i)
                if check_result > 0:
                    true_check_allow.append((True,check_allow[i]))
                    print(check_result)
                else:
                    continue
            #    true_check_allow
        
        
            # функция с помощью которой создаю кортеж. В кортеже указываю длинну правила, принадлежность к правилу и само правило
            def build_decision_list (store_list, checked_list, type_of_rule):
                for i in range (len(checked_list)):
                    if type_of_rule == 1:
                        temp_3 = len(checked_list[i]),'a', checked_list[i]
                        store_list.append(temp_3)
                    elif type_of_rule == 0:
                        temp_3 = len(checked_list[i]),'d', checked_list[i]
                        store_list.append(temp_3)
                return store_list
        
        
            # создал пустой список в который последовательно складываю обработанные результаты проверки правил
            decision_list = []
            build_decision_list(decision_list, true_simple_disallow, 0)
            build_decision_list(decision_list, true_simple_allow, 1)
            build_decision_list(decision_list, true_check_disallow, 0)
            build_decision_list(decision_list, true_check_allow, 1)
        
            # сортирую полученный список по убыванию, по длинне правила
            decision_list.sort(reverse=True)
            #       decision_list
        
        
            error_marker = 0 
            if len(decision_list) == 0:
                robot_txt_result = 'True'
            else:
                if decision_list[0][1] == 'a':
                    robot_txt_result = 'True'
                elif decision_list[0][1] == 'f':
                    robot_txt_result = 'False'
                else:
                    robot_txt_result = 'False'
                    error_marker += 1 
        
        
            # Поставил как временную заглушку exit. В данном месте нужно будет поставить какой-то прерыватель 
            # которые будет проверять наличие значения целевой переменной и при наличии значения по это целевой переменной
            # отправлять ответ клиенту и останавливать выполнение кода
            #    if robot_txt_result == False or True:
            #        print('Done, send it:' ,robot_txt_result)
                
            db_status_to_fetcher = robot_txt_result
            db_cash_robots_txt = robots_txt
        
        
            row_for_db = {'db_input_link':db_input_link, 
                          'db_robots_txt_link':db_robots_txt_link,
                          'db_status_to_fetcher': db_status_to_fetcher,
                          'db_cash_robots_txt':db_cash_robots_txt 
                         }
            coll.save(row_for_db)
        
        
            finish_time = time.time()
            work_time = finish_time - start_time
            result = robot_txt_result
            return result
 


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def checklink_crwdelay(data):
    import requests
    import urllib.request
    import urllib.parse
    import pymongo
    import time
    import math
    
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['robots_txt_parcer']
    coll = db['links']
    coll2 = db['last_visit']

    input_url = data
    db_input_link = input_url


    # из полученной ссылки выделяем корневой каталог с доменом и добавляем к нему окончание '/robots.txt'
    x = urllib.parse.urlparse(input_url)[0]
    y = urllib.parse.urlparse(input_url)[1]
    url_box = x + '://' + y + '/robots.txt' 
    url_box 

    db_robots_txt_link = url_box

    robot_txt_result = '-'

    try:
        test_channel = str(requests.get(url_box))[-5:-2]
        if test_channel != '200':
            robot_txt_result = 'False' 
        elif test_channel == '200':
            try:
                robots_txt = urllib.request.urlopen(url_box).read()
                robots_txt = robots_txt.decode('utf-8')
                robots_txt_2 = robots_txt.split('\n')
                robots_txt_2
            except Exception:
                robot_txt_result = 'False'
    except Exception:
        robot_txt_result = 'False'
   
    if robot_txt_result == 'False':
        result = '0'
        return result
        
    elif robot_txt_result == '-':
        robot_list = []
        counter = -1
        for i in range(len(robots_txt_2)):
            robots_txt_3 = robots_txt_2[i].split(' ')[0]
            if robots_txt_3 == 'User-agent:' or robots_txt_3 == 'User-Agent:': 
                robot_list.append([('User-agent;',robots_txt_2[i].split(' ')[1]),['Crawl-delay:'],
                                   ['Allow:'],['Disallow:']])
                counter += 1
            elif robots_txt_3 == 'Crawl-delay:':
                robot_list[counter][1].append(robots_txt_2[i].split(' ')[1])
            elif robots_txt_3 == 'Allow:':
                robot_list[counter][2].append(robots_txt_2[i].split(' ')[1])
            elif robots_txt_3 == 'Disallow:':
                robot_list[counter][3].append(robots_txt_2[i].split(' ')[1])
            else:
                continue
    
    
        # выбираем роль доступную нашему боту
        rules_list = []
        for i in range(len(robot_list)):
            if robot_list[i][0][1] == '*':
                rules_list = robot_list[i]
            else:
                continue
    
        if len(rules_list[1]) == 1:
            rules_list[1].append('0')
            
        last_visit = time.time()
        
        if coll2.find({"db_robots_txt_link": url_box }).count() > 0:
            prev = list(coll2.find({'db_robots_txt_link':url_box}))
            diff = last_visit - prev[0].get('last_visit')

        else:
            coll2.save({'db_robots_txt_link':url_box,'last_visit':last_visit})
            diff = int(rules_list[1][1])
            
        if diff < int(rules_list[1][1]):
            time_sleep = math.ceil(int(rules_list[1][1]) - diff)
        else:
            time_sleep =  0
        
        result = str(time_sleep)

    last_visit =  last_visit + time_sleep - 0.01          
    coll2.update({'db_robots_txt_link':url_box},{'db_robots_txt_link':url_box, 'last_visit':last_visit})

    return result

print(checklink_access('http://qaru.site/questions/16012/split-strings-with-multiple-delimiters'))
print(checklink_crwdelay('http://qaru.site/questions/16012/split-strings-with-multiple-delimiters'))

