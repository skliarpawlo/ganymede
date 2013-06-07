# coding: utf-8

from core import db
import time

class SearchForm :

    selectors = {
        # merge here
    }

    own_selectors = {
        "checkboxes" : {
            "has_photos" : "//*[@id='hasPhotos']",
            "new_building" : "//*[@id='newBuilding']",
            "without_fee" : "//*[@id='withoutFee']",
            "without_brokers" : "//*[@id='withoutBrokers']",
            "non_residential_fund" : "//*[@id='nonResidentialFund']",
            "near_subway" : "//*[@id='nearMetro']"
        }
    }

    @staticmethod
    def add_selectors( a, b, path=None ):
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    SearchForm.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass # same leaf value
                else:
                    raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

    def __init__(self, ff) :
        self.ff = ff
        self.add_selectors( self.selectors, SearchForm.own_selectors )

    def set_checkbox(self, id):
        x = self.ff.find_element_by_xpath( self.own_selectors['checkboxes'][ id ] )
        if not x.is_selected() :
            x.click()

    def unset_checkbox(self, id):
        x = self.ff.find_element_by_xpath( self.own_selectors['checkboxes'][ id ] )
        if x.is_selected() :
            x.click()

    def check_checkbox(self, id, must_be_checked=True):
        assert self.ff.find_element_by_xpath( self.checkboxes[ id ] ).is_selected() == must_be_checked, \
            u"Флаг '{id}' не в правильном состоянии".format( id )

    # price
    def set_price(self, _from, _to):
        pass

    def check_price(self, _from, _to):
        pass

    # area
    def set_area(self, _from=None, _to=None):
        pass

    def check_area(self, _from=None, _to=None):
        pass

    # area
    def set_rooms(self, _rooms):
        pass

    def check_rooms(self, _rooms):
        pass

    # submit
    def go(self):
        pass


class CallistoSearchForm( SearchForm ) :
    "форма поиска в выдаче"

    own_selectors = {
        "submit" : "//*[@id='s-go']",
        "realty_contract" : {
            "input" : '//*[@id="s-form"]//div[@class="input-pseudoselect for-items-nowrap"]',
            "check" : {
                u"аренда квартир" : '//*[@id="s-form"]//a[@contract="2" and @realty="1"]',
                u"аренда офисов" : '//*[@id="s-form"]//a[@contract="2" and @realty="5"]',
                u"аренда комнат" : '//*[@id="s-form"]//a[@contract="2" and @realty="20"]',
                u"продажа квартир" : '//*[@id="s-form"]//a[@contract="1" and @realty="1"]',
                u"продажа офисов" : '//*[@id="s-form"]//a[@contract="1" and @realty="5"]',
                u"посуточная аренда" : '//*[@id="s-form"]//a[@contract="6" and @realty="1"]'
            }
        },
        "rooms" : {
            "input" : "//*[@id='rnumber']",
            "check" : {
                1 : "//*[@id='r1']",
                2 : "//*[@id='r2']",
                3 : "//*[@id='r3']",
                4 : "//*[@id='r4']",
                5 : "//*[@id='r5']"
            }
        },
        "area" : {
            "input" : "//*[@id='atext']",
            "from" : '//*[@id="square"]//input[@name="generalAreaMin"]',
            "to" : '//*[@id="square"]//input[@name="generalAreaMax"]'
        },
        "price" : {
            "input" : "//*[@id='ptext']",
            "from" : '//*[@id="price"]//input[@name="priceMin"]',
            "to" : '//*[@id="price"]//input[@name="priceMax"]'
        },
        "geo" : {
            "parts" : {
                "districts" : "//*[@id='ch-district']",
                "street" : "//*[@id='ch-street']",
                "address" : "//*[@id='ch-address']",
                "subway" : "//*[@id='ch-subway']"
            },
            "inputs" : {
                "districts" : "//*[@id='dtext']",
                "street" : "//*[@id='s-street']//input[@class='ac_input']",
                "address" : "//*[@id='address']",
                "subway" : {
                    "select" : "//*[@id='stext']",
                    "distance" : "//*[@id='distance']"
                }
            },
            "districts" : { }, # to be initialized from db
            "subway" : {}, # to be initialized from db
            "subway_distance" : {
                 250 : '//*[@id="distance"]//div[@data-value="250"]',
                 500 : '//*[@id="distance"]//div[@data-value="500"]',
                 750 : '//*[@id="distance"]//div[@data-value="750"]',
                 1000 : '//*[@id="distance"]//div[@data-value="1000"]',
                 2000 : '//*[@id="distance"]//div[@data-value="2000"]'
            }
        },
    }

    def __init__(self, ff, city_id):
        SearchForm.__init__( self, ff )

        res = db.execute(
            """
               SELECT district_id, nominative
               FROM geo_districts
               WHERE city_id={city}
            """.format( city=city_id )
        ).fetchall()
        for x in res :
            self.own_selectors[ 'geo' ][ 'districts' ][ x[ 1 ] ] = "//*[@id='d{id}']".format( id = x[ 0 ] )

        res = db.execute(
            """
               SELECT microdistrict_id, nominative
               FROM geo_microdistricts
               WHERE city_id={city}
            """.format( city=city_id )
        ).fetchall()
        for x in res :
            self.own_selectors[ 'geo' ][ 'districts' ][ x[ 1 ] ] = "//*[@id='m{id}']".format( id = x[ 0 ] )

        res = db.execute(
            """
               SELECT subway_station_id, nominative
               FROM subway_stations
               WHERE city_id={city}
            """.format( city=city_id )
        ).fetchall()
        for x in res :
            self.own_selectors[ 'geo' ][ 'subway' ][ x[ 1 ] ] = "//*[@id='s{id}']".format( id = x[ 0 ] )

        self.add_selectors( self.selectors, self.own_selectors )

    def _set_select(self, key, check):
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()
        for c in check :
            self.ff.find_element_by_xpath( self.own_selectors[ key ][ "check" ][ c ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()

    def _check_select(self, key, check):
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()
        for c in check :
            assert self.ff.find_element_by_xpath( self.own_selectors[ key ][ "check" ][ c ] ).is_selected(),\
            u"В селекте {0} не выбран {1}, хотя выбирался при заполнении формы".format( key, c )
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()

    def _set_from_to(self, key, _from=None, _to=None):
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()
        if not _from is None :
            el = self.ff.find_element_by_xpath( self.own_selectors[ key ][ "from" ] )
            el.click()
            el.clear()
            el.send_keys( _from )
        if not _to is None :
            el = self.ff.find_element_by_xpath( self.own_selectors[ key ][ "to" ] )
            el.click()
            el.clear()
            el.send_keys( _to )
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()

    def _check_from_to(self, key, _from=None, _to=None):
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()
        if not _from is None :
            from_xpath = self.own_selectors[ key ][ "from" ]
            val = self.ff.find_element_by_xpath( from_xpath ).get_attribute( "value" )
            assert val == str(_from), \
                u"Значение {0} не соответвует введенному, {1} != {2}".format(
                    key,
                    val,
                    _from
                )
        if not _to is None :
            to_xpath = self.own_selectors[ key ][ "to" ]
            val = self.ff.find_element_by_xpath( to_xpath ).get_attribute( "value" )
            assert val == str(_to), \
                u"Значение {0} не соответвует введенному, {1} != {2}".format(
                    key,
                    val,
                    _to
                )
        self.ff.find_element_by_xpath( self.own_selectors[ key ][ "input" ] ).click()

    # area
    def set_area(self, _from=None, _to=None):
        self._set_from_to( "area", _from, _to )

    def check_area(self, _from=None, _to=None):
        self._check_from_to( "area", _from, _to )

    # price
    def set_price(self, _from=None, _to=None):
        self._set_from_to( "price", _from, _to )

    def check_price(self, _from, _to):
        self._check_from_to( "price", _from, _to )

    # rooms
    def set_rooms(self, _rooms):
        self._set_select( "rooms", _rooms )

    def check_rooms(self, _rooms):
        self._check_select( "rooms", _rooms )

    # contract/realty
    def contract_realty(self, contract_realty):
        self.ff.find_element_by_xpath( self.own_selectors[ "realty_contract" ][ "input" ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ "realty_contract" ][ "check" ][ contract_realty ] ).click()

    # submit
    def go(self):
        self.ff.find_element_by_xpath( self.own_selectors[ "submit" ] ).click()

    # geo

    # districts
    def set_districts(self, districts) :
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "parts" ][ "districts" ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "districts" ] ).click()
        for d in districts :
            self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "districts" ][ d ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "districts" ] ).click()

    def check_districts(self, districts) :
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "parts" ][ "districts" ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "districts" ] ).click()
        try :
            for d in districts :
                assert self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "districts" ][ d ] ).is_selected(),\
                    u"Район по '{0}' не выбран, хотя был при заполнении формы".format( d )
        finally:
            self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "districts" ] ).click()

    # street
    def set_street(self, texts):
        self.ff.find_element_by_xpath( self.own_selectors['geo']['parts']['street'] ).click()
        click_all( self.ff, "//*[@id='default-value-input']" )

        input = self.ff.find_element_by_xpath( self.own_selectors['geo']['inputs']['street'] )
        input.click()
        input.clear()

        for t in texts :
            input.send_keys( t )
            time.sleep( 2 )

    #address
    def set_address(self, texts):
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "parts" ][ "address" ] ).click()
        click_all( self.ff, "//*[@id='default-value-input']" )
        inp = self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "address" ] )
        inp.click()
        inp.clear()
        for t in texts :
            inp.send_keys( t )
            time.sleep( 2 )

        return inp.get_attribute("value")

    def check_address(self, check):
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "parts" ][ "address" ] ).click()
        inp = self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "address" ] )
        inp.click()
        assert inp.get_attribute("value") == check, \
            u"Поле адреса заполнено не верно {0} != {1}".format( inp.get_attribute("value"), check )

    #metro
    def set_subway(self, subways, distance = None) :
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "parts" ][ "subway" ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "subway" ][ "select" ] ).click()
        for s in subways :
            self.ff.execute_script( "$(document.evaluate(\"{0}\", document, null, XPathResult.ANY_TYPE, null).iterateNext()).click();".format(
                self.own_selectors[ "geo" ][ "subway" ][ s ]
            ) )
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "subway" ][ "select" ] ).click()

        if not distance is None :
            self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "subway" ][ "distance" ] ).click()
            self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "subway_distance" ][ distance ] ).click()

    def check_subway(self, subways, distance = None) :
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "parts" ][ "subway" ] ).click()
        self.ff.find_element_by_xpath( self.own_selectors[ "geo" ][ "inputs" ][ "subway" ][ "select" ] ).click()
        for s in subways :
            res = self.ff.execute_script( "return document.evaluate(\"{0}\", document, null, XPathResult.ANY_TYPE, null).iterateNext().checked;".format(
                self.own_selectors[ "geo" ][ "subway" ][ s ]
            ) )
            assert res == True, u"Станция метро c '{0}', не отмечена, хотя выбиралась при заполнении формы".format( s )


## util functions
def click_all( ff, elems ) :
    if type(elems) == list :
        for elem in elems :
            try :
                ff.find_element_by_xpath( elem ).click()
            except :
                pass
    else :
        try :
            ff.find_element_by_xpath( elems ).click()
        except :
            pass

