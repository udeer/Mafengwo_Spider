import pandas as pd
from pyecharts import Bar,Grid,Geo


class MaFengWoData(object):
    def __init__(self):
        self.city_base = pd.read_excel('city_base.xls')
        self.city_food = pd.read_excel('city_food.xls')
        self.city_jd = pd.read_excel('city_jd.xls')

    def get_data(self):
        self.city_base.sort_values('cy_count', ascending=False, inplace=True)
        attra = self.city_base['city_name'][0:15]
        v1a = self.city_base['cy_count'][0:15]
        bar1 = Bar("餐饮类标签排名")
        bar1.add("餐饮类标签分数", attra, v1a, is_stack=True, xaxis_rotate=30)

        self.city_base.sort_values('jd_count', ascending=False, inplace=True)
        attrb = self.city_base['city_name'][0:15]
        v1b = self.city_base['jd_count'][0:15]
        bar2 = Bar("景点类标签排名", title_top="30%")
        bar2.add("景点类标签分数", attrb, v1b, legend_top="30%", is_stack=True, xaxis_rotate=30)

        self.city_base.sort_values('gw_yl_count', ascending=False, inplace=True)
        attrc = self.city_base['city_name'][0:15]
        v1c = self.city_base['gw_yl_count'][0:15]
        bar3 = Bar("休闲类标签排名", title_top="67.5%")
        bar3.add("休闲类标签分数", attrc, v1c, legend_top="67.5%", is_stack=True, xaxis_rotate=30)
        return bar1,bar2,bar3

    def render(self):
        bar1,bar2,bar3=self.get_data()
        grid = Grid(height=800)
        grid.add(bar1, grid_bottom="75%")
        grid.add(bar2, grid_bottom="37.5%", grid_top="37.5%")
        grid.add(bar3, grid_top="75%")
        grid.render('城市分类标签.html')

        self.city_base.sort_values('total_city_yj', ascending=False, inplace=True)
        attr = self.city_base['city_name'][0:10]
        v1 = self.city_base['total_city_yj'][0:10]
        bar = Bar("游记总数量TOP10")
        bar.add("游记总数", attr, v1, is_stack=True)
        bar.render('游记总数量TOP10.html')

        self.city_food.sort_values('food_count', ascending=False, inplace=True)
        attr_food = self.city_food['food'][0:15]
        # print(attr_food)
        v1_food = self.city_food['food_count'][0:15]
        bar_food = Bar('热门食物排名')
        bar_food.add('热门食物', attr_food, v1_food, is_stack=True, interval=0, xaxis_rotate=30, yaxix_min=4.2,
                     is_splitline_show=False)
        bar_food.render('热门食物.html')

        self.city_jd.sort_values('jd_count', ascending=False, inplace=True)
        attr_f = self.city_jd['jd'][0:15]
        v1_f = self.city_jd['jd_count'][0:15]
        bar_f = Bar('热门景点排名')
        bar_f.add('热门景点', attr_f, v1_f, is_stack=True, interval=0, xaxis_rotate=30, yaxix_min=4.2,
                  is_splitline_show=False)
        bar_f.render('热门景点.html')

        # 按照各个城市游记数量获得全国旅行目的地热力图
        # pycharts中的Geo绘制中国地图，在图中显示各个地区的旅游热度
        data = [(self.city_base['city_name'][i], self.city_base['total_city_yj'][i]) for i in range(0, self.city_base.shape[0])]
        geo = Geo('全国城市旅游热力图', title_color="#fff",
                  title_pos="center", width=1200,
                  height=600, background_color='#404a59')
        while True:
            try:
                attr, value = geo.cast(data)
                geo.add("", attr, value, visual_range=[0, 15000], visual_text_color="#fff", symbol_size=15,
                        is_visualmap=True, is_roam=False)
            except ValueError as e:
                e = str(e)
                e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名
                for i in range(0, len(data)):
                    if e in data[i]:
                        data.pop(i)
                        break
            else:
                break
        geo.render('蚂蜂窝游记热力图.html')


# if __name__=='__main__':
#     object=MaFengWoData()
#     object.view_data()