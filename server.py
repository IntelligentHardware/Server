import socket
import os,sys
import bd
import sql_manage as sql
os.chdir(os.path.dirname(sys.argv[0]))

def info_recv(Pi_socket):  #接收来自Pi的请求信息
    info = Pi_socket.recv(1024).decode('utf-8')
    if info:  #判断是否掉线
        if info == 'data':
            print('receive data')  #发送反馈 准备接收
            Pi_socket.send('ACK'.encode('utf-8'))
            data_recv(Pi_socket)
        elif info == 'image':
            print('receive image')
            Pi_socket.send('ACK'.encode('utf-8'))
            image_recv(Pi_socket)
        return True
    else:
        Pi_socket.close()
        return False

def data_recv(Pi_socket):  #接收传感器数据
    data_str = Pi_socket.recv(1024)   
    with open('data.txt', 'wb') as data:
        data.write(data_str)
    print('data接收完成')
    sql.data_in(data_str.decode('utf-8'))

def image_recv(Pi_socket):  #接收图像
    length = int.from_bytes(Pi_socket.recv(4), byteorder = 'big')
    print('数据长度:%d' % (length))
    direction = int.from_bytes(Pi_socket.recv(1), byteorder = 'big')
    print('方向为：', direction)
    image_data = b''
    cur_len = 0
    while cur_len < length:  #分多次接收
        data = Pi_socket.recv(1024)
        image_data += data
        cur_len += len(data)
    with open('result.jpg', 'wb') as image:
        image.write(image_data)
    #print('识别结果：%s' % bd.image_detect(image_data))
    name = bd.image_detect(image_data)
    
    print('image接收完成')
    print(direction,name)

    #将物品信息存入数据库
    if direction == 1:
        sql.item_in(name)
    #从数据库删除物品
    elif direction == 0:
        sql.item_out(name)


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 9000))

    server_socket.listen(128)
    print('等待连接')
    while True:
        Pi_socket, Pi_socket_addr = server_socket.accept()  #与Pi链接
        temp = True
        print('连接成功:%s' % (str(Pi_socket_addr)))
        while temp:
            temp = info_recv(Pi_socket)
'''
    image_recv(Pi_socket)
    while True:
        data = Pi_socket.recv(1027).decode('utf-8')
        print(data)
'''
if __name__ == '__main__':
    main()