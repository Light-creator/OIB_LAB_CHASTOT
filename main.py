from itertools import groupby


class CHistory:

    def __init__(self, str):
        self.lstHistory = [str]

    def back(self):
        self.lstHistory.pop()

    def get_last_update(self):
        return self.lstHistory[-1]

    def update(self, new_str):
        self.lstHistory.append(new_str)


class Crypto:

    def __init__(self, str):
        self.sStart = str.upper()
        self.objHistory = CHistory(str)
        self.sCrypto = str.upper()
        self.nCount = len(str.strip())
        self.hashTable= {}
        self.lstUse = []
        self.hashUpdateChar = {}
        self.st = 'оеаинтсрвлкмдпуязыбьъгчйхёжшюцщэф'
        self.hashSt2 = {
            'о' : 0.09,
            'и' : 0.072,
            'е' : 0.062,
            'а' : 0.062,
            'н' : 0.053,
            'т' : 0.053,
            'р' : 0.045,
            'с' : 0.040,
            'в' : 0.038,
            'л' : 0.035,
            'к' : 0.028,
            'м' : 0.026,
            'д' : 0.025,
            'п' : 0.023,
            'у' : 0.021,
            'я' : 0.018,
            'ы' : 0.016,
            'ь' : 0.014,
            'г' : 0.013,
            'з' : 0.016,
            'б' : 0.014,
            'ч' : 0.013,
            'й' : 0.012,
            'х' : 0.009,
            'ё' : 0.008,
            'ж' : 0.007,
            'ш' : 0.006,
            'ю' : 0.006,
            'ц' : 0.003,
            'щ' : 0.003,
            'э' : 0.003,
            'ф' : 0.002,
            'ъ' : 0.001,
        }

    # Группировка слов по кол-ву букв в слове
    def n_words(self):
        sNew = self.sCrypto
        for c in '.|/,!*&?:;`@#$%^()…—-': 
            sNew = sNew.replace(c, '')

        lst = sNew.split()

        hashGroups = {}
        for sWord in lst:
            if len(sWord) in hashGroups: 
                hashGroups[len(sWord)] += [sWord]
            else:
                hashGroups[len(sWord)] = [sWord]

        self.print_hashGroups(hashGroups)   

    # Группировка слов по кол-ву нерасшифрованных букв в слове
    def n_characters(self):
        sNew = self.sCrypto
        for c in '.|/,!*&?:;`@#$%^()…—-': 
            sNew = sNew.replace(c, '')

        lst = sNew.split()

        hashGroups = {}
        for sWord in lst:
            count = 0
            for c in sWord:
                if c.upper() == c: count += 1
            
            if count != 0:
                if count in hashGroups:
                    hashGroups[count] += [sWord]
                else:
                    hashGroups[count] = [sWord]

        self.print_hashGroups(hashGroups)   


    # Возврат по истории
    def rendo_history(self):
        self.objHistory.back()
        self.sCrypto = self.objHistory.get_last_update()
        self.lstUse.pop()
        self.lstUse.pop()

    # Замена букв
    def change_c(self):
        x = input("Введите букву, которую хотите заменить: ")
        y = input("Введите букву, на которую хотите заменить: ")
        self.sCrypto = self.sCrypto.replace(x.strip(), y.strip().lower())
        self.objHistory.update(self.sCrypto)
        self.lstUse += [x, y]
        self.print_crypto()

    # Предлагаемые замены
    def change_variant(self):
        #print(self.hashTable)
        i = 0
        lstCheck = []
        for key in self.hashTable:
            m = 10
            for keyCh in self.hashSt2:
                val = self.hashTable[key]
                valCh = self.hashSt2[keyCh]
                dVal = abs(val-valCh)
                if keyCh not in lstCheck:
                    if m > dVal: 
                        self.hashUpdateChar[key] = keyCh
                        m = dVal
                    elif m == dVal: self.hashUpdateChar[key] = keyCh
            lstCheck += [self.hashUpdateChar[key]]
            
        for key in self.hashTable:
            if key not in self.hashUpdateChar:
                self.hashUpdateChar[key] = self.st[i]
            i += 1
            
        


    # Анализ частоты букв
    def chastot_analys(self):
        for c in self.sStart.strip():
            if c == ' ' or c in '.|/,!*&?:;`@#$%^()…—«» -': continue

            if c in self.hashTable: self.hashTable[c] += 1
            else: self.hashTable[c] = 1

        for key in self.hashTable:
            self.hashTable[key] = self.hashTable[key] / self.nCount

        self.hashTable = dict(sorted(self.hashTable.items(), key=lambda item: item[1], reverse=True))

    # Автоматическая замена
    def auto_crypto(self):
        ss = self.sStart
        for key in self.hashUpdateChar:
            flag = 0
            val = self.hashUpdateChar[key]
            if val not in self.lstUse and key not in self.lstUse:
                flag = 1
                self.lstUse += [val, key]
                self.sCrypto = self.sCrypto.replace(key, val)
                
        self.lstUse = list(set(self.lstUse)) 
        self.objHistory.update(self.sCrypto)
        self.print_crypto()


    # Принты:

    def print_hashGroups(self, hashGroups):
        print('---------------------------\n')
        for key in sorted(hashGroups):
            print(f"{key} => {hashGroups[key]}")
        print('\n---------------------------')
        input()

    # Отображение криптограммы
    def print_crypto(self):
        print('---------------------------\n')
        print('Криптограмма на данный момент:\n')
        print(self.sCrypto)
        print('\n---------------------------')
        input()

    def print_chastot_analys(self):
        print('---------------------------\n')
        print('Частотный Анализ:\n')
        for key in self.hashTable:
            print(f'{key} => {self.hashTable[key]:9.4f}')
        print('\n---------------------------')
        input()

    def print_change_variant(self):
        print('---------------------------\n')
        print('Предлагаемые замены:\n')
        for key in self.hashTable:
            print(f"{key} => {self.hashUpdateChar[key]}")
        print('\n---------------------------')
        input()




def main():
    #str = input("Enter crypto_str: ")
    str = 'Лсйрупдсбннб - юуп уйр дпмпгпмпнлй, лпупсба тптупйу йи лпспулпдп хсбднёоуб ибщйхспгбоопдп уёлтуб. Пвьшоп щйхс, йтрпмэифёньк ема щйхспгбойа уёлтуб, ептубупшоп рспту, шупвь лсйрупдсбннф нпзоп вьмп сбидбебуэ гсфшофя. Шбтуп йтрпмэифяута ибнёоаяъйё щйхсь, г лпупсьц лбзеба вфлгб ибнёоаёута есфдпк вфлгпк ймй чйхспк. Шупвь сёщйуэ дпмпгпмпнлф, офзоп гпттубопгйуэ псйдйобмэофя оберйтэ. Цпуа лпдеб-уп пой йтрпмэипгбмйтэ г впмёё тёсэёиоьц рсймпзёойац, тёкшбт пой г птопгопн рёшбубяута ема сбигмёшёойа г дбиёубц й зфсобмбц. Ема тпиебойа лсйрупдсбнн йопдеб йтрпмэифяута есфдйё уйрь лмбттйшётлйц щйхспг. Рсйнёспн агмаёута лойзоьк щйхс, г лпупспн лойдб ймй тубуэа йтрпмэифяута ема щйхспгбойа тппвъёойа.'
    objCrypto = Crypto(str)
    objCrypto.chastot_analys()
    objCrypto.change_variant()
    x = 0
    while x != 9:
        print('---------------------------\n')
        print('1. Заменить букву')
        print('2. Отображение криптограммы на данный момент')
        print('3. Отображение частотного анализа')
        print('4. Отображение предлагаемых замен')
        print('5. Откат истории')
        print('6. Вывод сгруппированных слов по кол-ву букв')
        print('7. Вывод сгруппированных слов по кол-ву нерасшифрованных букв')
        print('8. Автоматическая замена')
        print('9. Выход')
        print('\n')
        x = input("Введите действие: ")
        print('\n---------------------------')
        
        if x == '1': 
            objCrypto.change_c()
            continue
        elif x == '2': objCrypto.print_crypto()
        elif x == '3': objCrypto.print_chastot_analys()
        elif x == '4': objCrypto.print_change_variant()
        elif x == '5': objCrypto.rendo_history()
        elif x == '6': objCrypto.n_words()
        elif x == '7': objCrypto.n_characters()
        elif x == '8': objCrypto.auto_crypto()
        elif x == '9': break
        else: 
            print('Некорректный ввод!')
            continue




if __name__ == "__main__":
    main()