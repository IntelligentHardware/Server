from aip import AipImageClassify
import os,sys

os.chdir(os.path.dirname(sys.argv[0]))

APP_ID = '*'
API_KEY = '*'
SECRET_KEY = '*'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def image_detect(image):
    return client.advancedGeneral(image)['result'][0]['keyword']

def food_detect(image):
    return client.ingredient(image)['result'][0]['name']

def main():
    image = get_file_content('lemon.jpg')
    print(client.advancedGeneral(image))
    print(client.ingredient(image))

if __name__ == '__main__':
    main()


