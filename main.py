from mafengwo.mfw_spider import MaFengWo
from mafengwo.mfw_render import MaFengWoData


if __name__=='__main__':
    mfw=MaFengWo()
    mfw.start()
    data=MaFengWoData()
    data.render()
    #mfw.get_city_info('南京',10684)

