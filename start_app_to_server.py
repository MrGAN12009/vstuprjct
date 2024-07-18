phone_number = '89999'


flag = True

if len(phone_number) == 11 and phone_number[0] == '8':
    print(1)
elif len(phone_number) == 12 and phone_number[0:2] == '+7':
    print(2)
else:
    print("Неправильно введён номер.")
    flag == False