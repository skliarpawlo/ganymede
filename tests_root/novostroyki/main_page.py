# coding: utf-8

from testlib import utils

class NovostroykiMain( utils.PageTest ) :
    test_id = 2

    url = u"novostroyki.lun.ua/"
    title = u"Новостройки - ЛУН.ua"

class PopularBlockLinks( utils.SubTest ) :

    def run(self):
        popularlink_xpath = '//*[@id="content"]/div[2]/div[2]/table/tbody/tr/td[1]/span/span/noindex/a'
        href = self.webpage.find_element_by_xpath( popularlink_xpath ).get_attribute('href')
        assert href.startswith( 'http://www.lun.ua/redirect?to=' ), 'link {0} go not through redirect'.format( href )
        assert "utm_source=lun_ua" in href, 'utm_source=lun_ua not found for link {0}'.format( href )
        assert "utm_medium=premium_catalog" in href, 'utm_medium=premium_catalog not found for link {0}'.format( href )
        assert "utm_campaign=novostroyki_premium" in href, 'utm_campaign=novostroyki_premium not found for link {0}'.format( href )
