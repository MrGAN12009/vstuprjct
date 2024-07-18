# import requests
#
# url = 'http://192.168.0.163:8000'
# data = {"volk":"pidor"}
# x = requests.post(url, data)
#
# print(x)

data = {"231413421": "daniil", "128": "ann", "14234": "sdf", "89898": "lera1", "123123123123": "123123123123", "12": "123"}

import xlsxwriter
workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Hello world')
k = 0
for i in data.keys():
    worksheet.write(k, 0, data[i])
    worksheet.write(k, 1, i)
    k += 1


workbook.close()
