import pymysql
import datetime
'''
添加物品步骤
1.获取数据库物品总数目
2.id=总数目+1 INSERT

删除物品步骤
1.获取目标物品id
2.删除目标id
3.id大于目标物品id进行-1操作
'''


url_dict = {'苹果':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/apple.png',
            '柠檬':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/lemon.png',
            '葡萄':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/grape.png',
            '香蕉':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/banana.png',
            '桃子':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/peach.png',
            '水蜜桃':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/peach.png',
            '西瓜':'https://raw.githubusercontent.com/IntelligentHardware/front/master/icons/watermelon.png',
            'default':'https://github.com/IntelligentHardware/front/blob/master/icons/broccoli.png'}

def connect():  #建立数据库连接
    conn = pymysql.connect(
        host = '124.71.225.45',
        port = 3306,
        user = 'yiping',
        passwd = 'xiaobing+1s',
        db = 'recipes'
    )
    cur = conn.cursor()
    return conn,cur

def item_count():  #获取物品总数目
    conn,cur = connect()
    sql = """SELECT * from items_items"""  
    cur.execute(sql)
    ret = cur.fetchall()
    conn.close()
    return len(ret)

def item_in(name):
    if name in url_dict.keys():
        date_begin = datetime.datetime.now()  #获取时间
        date_end = date_begin + datetime.timedelta(days = +3)  
        num = item_count()
        conn, cur = connect()  #连接数据库
        
        start_date = date_begin.strftime('%Y-%m-%d')
        end_date = date_end.strftime('%Y-%m-%d')
        duration = 30
        if name in url_dict.keys():
            url = url_dict[name]
        else:
            url = url_dict['default']
#        sql = "insert into items_items(id,name,start_date,end_date,duration,image_url) values (%d,'%s','%s','%s',%d,'%s')" % \
#            (id,name,start_date,end_date,duration,url)
        sql = "insert into items_items(name,start_date,end_date,duration,image_url) values ('%s','%s','%s',%d,'%s')" % \
            (name,start_date,end_date,duration,url)
        cur.execute(sql)
        conn.commit()

        conn.close()

def item_out(name):
    
    try:
        conn, cur = connect()
        sql = "select id from items_items where name='%s'" % (name)
        cur.execute(sql)
        ret = cur.fetchone()
        id = ret[0]  #获取删除目标的id
        sql = "delete from items_items where id=%d" % (id)
        cur.execute(sql)
        conn.commit()
        #更新剩余id
        #sql = "update items_items set id = id-1 where id>%d" % (id)
        #cur.execute(sql)
        conn.commit()

        conn.close()
    except:
        print('删除失败')

def data_in(data):
    conn, cur = connect()
    sql = "update data_data set data='%s' where id=0" % (data)
    cur.execute(sql)
    conn.commit()
    conn.close()

def item(name):
    conn, cur = connect()
    
    cur.execute('select * from items_items')
    ret = cur.fetchall()
    temp = True
    for i in ret:
        #print(i[1])
        if name == i[1]:
            temp = False
    if temp:
        item_in(name)
    else:
        item_out(name)
#rint(item_count())
#item_out('柠檬')
#data_in('30 30')
#item_in('苹果')
#item('苹果')


