# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class Dribbble1Pipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymysql

from scrapy.conf import settings



# 下面是将爬取到的信息插入到MySQL数据库中
class Dribbble1Pipeline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        # sql="insert into 表名 (字段) values(%s,%s,%s,%s,%s)" % (item['']...)

        # 创三个表，一个图片集表（图片集的名字和链接），一个图片链接表，一个设计师表，图片链接表和图片集表还要建一个对应关系（这个图片属于哪个图片集）

        # sql1 = "insert into behance_imgLink(img_url) values(%s)"
        # params1 = (item["Li_img_list"])
        #
        # sql2 = "insert into behance_picSet(design_name,set_name) values(%s,%s)"
        # params2 = (item["Li_designer"],item["Li_name"])
        # print(parten)
        # print(res)
        # print(new_img_urls)
        try:
            print("insert into dribbble_imgLink (designer,like_count,watch_count,talk_count,img_info,img_name,img_tag,img_url,img_date) values({},{},{},{},{},{},{},{},{})".format(item['designer'], item['like_count'], item['watch_count'], item['talk_count'], item['img_info'], item['img_name'], item['img_tag'], item['img_url'], item['img_date']))
            cue.execute("insert into dribbble_imgLink (designer,like_count,watch_count,talk_count,img_info,img_name,img_tag,img_url,img_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (item['designer'], item['like_count'], item['watch_count'], item['talk_count'], item['img_info'], item['img_name'], item['img_tag'], item['img_url'], item['img_date']))

            # cue.execute("insert into behance_picSet (design_name,set_name,set_url,set_tag,set_info) values(%s,%s,%s,%s,%s)",
            #             (item['designer'], item['name'], item['setList'], item['img_tags'], item['img_info']))

            # 测试语句
            print("insert success")
        except Exception as e:
            print('Insert error:', e)
            con.rollback()  # 回滚
        else:
            con.commit()  # 提交
        con.close()  # 关闭
        return item
