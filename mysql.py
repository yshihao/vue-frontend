import pymysql
import time
def init():
    host = "localhost"
    user = "root"
    passwd = "18717902963"
    database = "mytest"
    charset = "utf8mb4"
    conn = pymysql.connect(host=host,user=user,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql = "CREATE DATABASE IF NOT exists mytest2"
    cursor.execute(sql)
    sql2 = "use mytest2"
    cursor.execute(sql2)
    cursor.close()
    return conn

def gentables(conn):
    cursor = conn.cursor()
    sql3 = '''CREATE table if not exists users(
                    id int(11) NOT NULL AUTO_INCREMENT,
                    name varchar(255) NOT NULL,
                    password varchar(255) NOT NULL,
                    PRIMARY KEY(id)
                    ) ENGINE=InnoDB '''
    sql4 = '''create table  if not exists logs(
        logtime timestamp not null default current_timestamp,
        uid int(11) not null,
        type varchar(255) not null,
        dc varchar(255) not null,
        vlanid varchar(255),
        phy varchar(255),
        ip varchar(255) ,
        primary key(logtime)
        )
    '''
    sql5 = '''create table if not exists graphs(
        vlanid varchar(255) not null,
        node1 varchar(255) not null,
        node2 varchar(255) not null,
        primary key(vlanid,node1,node2)
    )
    '''
    sql6 = '''create table  if not exists infos(
        uid int(11) not null,
        dc varchar(255) not null,
        vlanid varchar(255) ,
        phy varchar(255),
        dockerid varchar(255),
        dockerimage varchar(255),
        dockername varchar(255),
        dockercommand varchar(255),
        dockercreatetime timestamp default current_timestamp
        )
    '''
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)



    cursor.close()
def updatelog(conn):
    cursor = conn.cursor()
   # sql1 = "insert into logs(uid,type,dc,vlanid,phy) values(1,'adddocker','dc1','vlan1','phy1')"
    sql2 = "insert into logs(uid,type,dc,phy) values(1,'adddocker','dc2','phy2')"

    #cursor.execute(sql1)
    cursor.execute(sql2)

    conn.commit()
    cursor.close()

def updates(conn):
    cursor = conn.cursor()
    #sql1 = "insert into users(name,password) values('admin','123456')"
    sql1 = "insert into users(name,password) values('admin2','123456')"
    sql2 = "insert into users(name,password) values('admin3','123456')"
    sql3 = "insert into infos(uid,dc,vlanid,phy,dockerid,dockerimage,dockername,dockercommand)\
        values(1,'dc1','vlan1','phy1','dockerid1','centos','myfirstdocker','/bin/bash')"
    sql4 = "insert into infos(uid,dc,vlanid,phy,dockerid,dockerimage,dockername,dockercommand)\
        values(1,'dc2','vlan2','phy4','dockerid2','ubuntu','myseconddocker','/bin/bash2')"
    sql5 = "insert into infos(uid,dc,vlanid,phy,dockerid,dockerimage,dockername,dockercommand)\
        values(2,'dc3','vlan4','phy2','dockerid5','centos','mythirddocker','/bin/bash')"
    sql6 = "insert into infos(uid,dc,vlanid,phy,dockerid,dockerimage,dockername,dockercommand)\
        values(2,'dc4','vlan6','phy3','dockerid44','ubuntu','myfouthdocker','/bin/bash2')"
    cursor.execute(sql1)
    cursor.execute(sql2)   
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)
    
    conn.commit()
    cursor.close()
def updates2(conn):
    cursor = conn.cursor()
    #sql1 = "insert into users(name,password) values('admin','123456')"
    sql1 = "insert into users(name,password) values('admin4','123456')"
    sql2 = "insert into users(name,password) values('admin5','123456')"
    sql3 = "insert into infos(uid,dc,vlanid,phy,dockerid,dockerimage,dockername,dockercommand)\
        values(1,'dc1','vlan1','phy2','dockerid1234','centoss','mydocker567','/bin/bashs/')"
    sql4 = "insert into infos(uid,dc,vlanid,phy,dockerid,dockerimage,dockername,dockercommand)\
        values(1,'dc1','vlan1','phy3','dockerid234','ubuntuuu','myseconddocker234','/bin/bash2/sdf')"

    cursor.execute(sql1)
    cursor.execute(sql2)   
    cursor.execute(sql3)
    cursor.execute(sql4)
    
    conn.commit()
    cursor.close()
def query(conn):
    uid = 1
    phy = "phy1"
    sql1 = "select dockerid,dockerimage,dockername,dockercommand,dockercreatetime from infos where uid=%s and phy=%s"
    cursor = conn.cursor()
    cursor.execute(sql1,[uid,phy])
    results = (cursor.fetchall())
    alldocker = []
    if results:
        for i in range(len(results)):
            docker = {
            'id': str(results[i][0]),
            'image': str(results[i][1]),
            'name': str(results[i][2]),
            'command': str(results[i][3]),
            'created': str(results[i][4])
            }
            alldocker.append(docker)
    cursor.close()       
    #print(type(results[0]))
    print(alldocker)

if __name__ == "__main__":
    conn = init()
    #gentables(conn)
    
    updates2(conn)
    #updatelog(conn)
    #query(conn)
    conn.close()
