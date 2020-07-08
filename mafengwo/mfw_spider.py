import os
import time
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
from pyecharts import Bar, Geo,Grid


class MaFengWo(object):
    def __init__(self):
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.date = time.strftime("%Y-%m-%d",time.localtime())
        print(self.date)

    #解析URL内容方法
    def get_url_content(self,url):
        re_object=request.Request(url,headers=self.headers)
        html=urlopen(re_object)
        bs_object=BeautifulSoup(html.read(),'html.parser')
        return bs_object

    #获得城市信息方法
    def get_city_info(self,city_name,city_code):
        city_base_info =self.handle_city_base(city_name, city_code)
        print(city_base_info)
        city_jd_info =self.get_city_jd(city_name, city_code)
        city_jd_info['city_name'] = city_name
        city_jd_info['total_city_yj'] = city_base_info['total_city_yj']
        print(city_jd_info)
        try:
            city_food_info =self.get_city_food(city_name, city_code)
            city_food_info['city_name'] = city_name
            city_food_info['total_city_yj'] = city_base_info['total_city_yj']
            print(city_food_info)
        except:
            city_food_info = pd.DataFrame()
        return city_base_info, city_food_info, city_jd_info

    #处理城市基本信息方法
    def handle_city_base(self,city_name,city_code):
        # 解析行程页面
        url='http://www.mafengwo.cn/xc/'+str(city_code)+'/'
        bs_object=self.get_url_content(url)
        node=bs_object.find('div',{'class':'m-tags'}).find('div',{'class':'bd'}).find_all('a')
        tag_node = bs_object.find('div', {'class': 'm-tags'}).find('div', {'class': 'bd'}).find_all('em')
        tag_count=[int(k.text) for k in tag_node]#标签总数量
        href=[k.attrs['href'][1:3] for k in node]
        all_count=sum([tag_count[i] for i in range(0,len(tag_count))])
        jd_count=sum([tag_count[i] for i in range(0,len(tag_count)) if href[i]=='jd'])#景点类标签排名
        cy_count=sum([tag_count[i] for i in range(0,len(tag_count)) if href[i]=='cy'])#餐饮类标签排名
        gw_yl_count=sum([tag_count[i] for i in range(0,len(tag_count)) if href[i] in ['gw', 'yl']])#购物娱乐类标签排名
        #游记
        url = 'http://www.mafengwo.cn/yj/' + str(city_code) + '/2-0-1.html '
        bs_object=self.get_url_content(url)
        total_city_yj=int(bs_object.find('span',{'class':'count'}).find_all('span')[1].text)
        return {'city_name': city_name, 'all_count': all_count, 'jd_count': jd_count,
                'cy_count': cy_count, 'gw_yl_count': gw_yl_count,'total_city_yj': total_city_yj}

    #获得城市餐饮方法
    def get_city_food(self,city_name,city_code):
        url = 'http://www.mafengwo.cn/cy/' + str(city_code) + '/gonglve.html'
        bs_object=self.get_url_content(url)
        node=bs_object.find('ol',{'class':'list-rank'}).find_all('h3')
        all_food = [k.text for k in node]
        #print(all_food)
        food_name = []
        for food in all_food:
            food_na = city_name + '-' + food
            food_name.append(food_na)
        food_count=[int(k.text) for k in bs_object.find('ol',{'class':'list-rank'}).find_all('span',{'class':'trend'})]
        return pd.DataFrame({'food':food_name[0:len(food_count)],'food_count':food_count})

    #获得城市景点方法
    def get_city_jd(self,city_name,city_code):
        url='http://www.mafengwo.cn/jd/'+str(city_code)+'/gonglve.html'
        bs_object=self.get_url_content(url)
        node=bs_object.find('div',{'class':'row-top5'}).find_all('h3')
        all_jd=[k.text.split('\n')[2] for k in node]
        jd_name=[]
        for jd in all_jd:
            food_na=city_name+'-'+jd
            jd_name.append(food_na)
        node=bs_object.find_all('span',{'class':'rev-total'})
        jd_count=[int(k.text.replace(' 条点评','')) for k in node]
        #print(jd_count)
        return pd.DataFrame({'jd':jd_name[0:len(jd_count)],'jd_count': jd_count})

    #程序启动
    def start(self):
        city_list = pd.read_excel('D:\mafengwo_spider\城市编号.xlsx')
        print(city_list)
        city_base = pd.DataFrame()
        city_food = pd.DataFrame()
        city_jd = pd.DataFrame()
        for i in range(0, city_list.shape[0]):
            try:
                k = city_list.iloc[i]
                city_base_info, city_food_info, city_jd_info =self.get_city_info(k['city_name'], k['city_code'])
                city_base = city_base.append(city_base_info, ignore_index=True)

                city_food = pd.concat([city_food, city_food_info], ignore_index=True)

                city_jd = pd.concat([city_jd, city_jd_info], ignore_index=True)

                print('正确:' + k['city_name'])
                print(i)
                time.sleep(3)
            except:
                print('错误:' + k['city_name'])
                print(i)
                continue
        writer = pd.ExcelWriter('city_base.xls')
        city_base.to_excel(writer, sheet_name='city_base', startcol=0, index=False)
        writer.save()
        writer_fd = pd.ExcelWriter('city_food.xls')
        city_food.to_excel(writer_fd, sheet_name='city_food', startcol=0, index=False)
        writer_fd.save()
        writer_jd = pd.ExcelWriter('city_jd.xls')
        city_jd.to_excel(writer_jd, sheet_name='city_jd', startcol=0, index=False)
        writer_jd.save()


# if __name__=='__main__':
#     mfw = MaFengWo()
#     mfw.start()
#     #mfw.get_city_info('南京',10684)



