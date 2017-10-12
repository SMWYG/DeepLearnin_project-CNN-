#os.listdir(path) 파일목록 리스트로 전달
#os.chdir(path) 작업 디렉토리 변경



from os import rename, listdir, chdir
import time

chdir('C:\\Users\\dahan\\Desktop\\image\\flower\\') #작업 디렉토리가 현재 작업중인 파이썬 파일이 있는 위치로 되어 있으므로 변경 필요
files = listdir('C:\\Users\\dahan\\Desktop\\image\\flower\\')
file_num = 1
count = 0
tmp=[]


for file in files:
    tmp.append(int(file.split('.')[0]))

tmp.sort()

for i in tmp:
    tmp[count] = str(i)+'.jpg'
    count += 1

files=tmp

for file_name in files:
    new_name = str(file_num) + '.jpg'
    rename(file_name, new_name)
    file_num += 1


print('파일 이름이 모두 변경되었습니다.')