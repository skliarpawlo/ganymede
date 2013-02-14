## coding: utf-8
#
#from testlib import utils
#
#class NovostroykiMain( utils.PageTest ) :
#    "Главная страница новостроек"
#
#    url = u"novostroyki.lun.ua/"
#    title = u"Новостройки - ЛУН.ua"
#
#class PopularBlockLinks( utils.SubTest ) :
#    "Проверка правильности ссылок в блоке 'Популярные новостройки'"
#    __parent_test__ = "NovostroykiMain"
#
#    def run(self):
#        popularlink_xpath = '//*[@id="content"]/div[2]/div[2]/table/tbody/tr/td[1]/span/span/noindex/a'
#        href = self.webpage.find_element_by_xpath( popularlink_xpath ).get_attribute('href')
#        assert href.startswith( 'http://www.lun.ua/redirect?to=' ), 'link {0} go not through redirect'.format( href )
#        assert "utm_source=lun_ua" in href, 'utm_source=lun_ua not found for link {0}'.format( href )
#        assert "utm_medium=premium_catalog" in href, 'utm_medium=premium_catalog not found for link {0}'.format( href )
#        assert "utm_campaign=novostroyki_premium" in href, 'utm_campaign=novostroyki_premium not found for link {0}'.format( href )
#
#class NearMetroLink( utils.SubTest ) :
#    "Проверка ссылки 'возле метро'"
#    __parent_test__ = "NovostroykiMain"
#
#    def run(self):
#        popularlink_xpath = '//*[@id="third-part-second"]/div/div[2]/ul[1]/li[3]/a'
#        href = utils.url_unquote( self.webpage.find_element_by_xpath( popularlink_xpath ).get_attribute('href') )
#        expect = u'http://novostroyki.lun.ua/новостройки-возле-метро-l2'
#        assert href == expect, 'link {0} not correct, excpected: {1}'.format( href, expect )
