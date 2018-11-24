# temp
username = 'asdd'
secret = '123'
file = open('Userform', 'r') 
js = file.read()
dic = json.loads(js) 
dic2 = {
    'user'+str(len(dic)):{
                'name': username,
                'password': secret
    }
}
dic.update(dic2)

for i in range(4):
    print(dic['user'+str(i)])

print('\n\n')
length = len(dic)

file.close()

listd = dict.values(dic)
print(str(dic['user'+ str(0)]['name'])