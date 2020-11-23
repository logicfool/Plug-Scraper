from .core import *

class Myntra():
    def __init__(self,*args):
        if args:
            self.url = args[0]
        else:
            raise Exception(NameError,"URL NOT PASSED")
        self.api_url = 'https://www.myntra.com/gateway/v2/search'
        self.api_url =  self.api_url+self.url.replace(get_domain_info(self.url)['full'],'')
        self.headers = {
    'Host': 'www.myntra.com',
'Connection': 'keep-alive',
'DNT': '1',
'x-meta-app': 'channel=web',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
'X-myntraweb': 'Yes',
'x-location-context': 'pincode=110019;source=IP',
'Content-Type': 'application/json',
'X-Sec-Clge-Req-Type': 'ajax',
'Accept': 'application/json',
'x-myntra-app': 'deviceID=d09a1093-08a7-4f9d-863d-f667deae7b39;customerID=;reqChannel=web;',
'X-Requested-With': 'browser',
'x-myntra-network': 'yes',
'app': 'web',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Referer': 'https://www.myntra.com/men-topwear?p=3&rf=Discount%20Range%3A70.0_100.0_70.0%20TO%20100.0&sort=price_asc',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9'}
        self.headers['Referer']  = self.url


    def cleanify_price(self,price):
        intt = ''
        price = str(price)
        a = price.split('-')[0]
        price = a
        for i in price:
            
            try:
                if i == '-':
                    intt = intt+' - '
                if i == '.':
                    intt = intt+i    
                else:
                    ii = int(i)
                    intt = intt+i
            except:
                pass
        #p2 = float(str(round(intt, 2)))
        intt = float(intt)
        return intt

    def perc_calc(self,real_price,deal_price):
        real_price = self.cleanify_price(real_price)
        deal_price = self.cleanify_price(deal_price)
        original = float(real_price)
        deal = float(deal_price)
        total_off = float(original - deal)
        p = (1 - deal / original) * 100
        p2 = float(str(round(p, 2)))
        return (str(p2)+' % Off',p2,total_off)

    def gen_headers(self):
      h = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.44','Mozilla/5.0 (X11; CrOS x86_64 13099.19.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.33 Safari/537.36']
      hh = random.choice(h)
      h = {'User-Agent':hh}
      return h

    def get_search_page(self):
      res = r().get(self.url,headers = self.gen_headers())
      self.html = res.html
      pattern = re.compile('var pageStateData = (.*?);')
      pattern1 = re.compile('window.__myx = (.*)')
      soup = BeautifulSoup(res.text, "lxml")
      scripts = soup.find_all('script')
      if scripts:
        for script in scripts:
          if pattern1.match(str(script.string)):
              self.data = pattern1.match(str(script.string))
              self.stock = json.loads(self.data.groups()[0])
              data = self.stock
      else:
        scripts = False
      if scripts:
        try:
          all_results = data['searchData']['results']['products']
          results = []
          for item in all_results:
            result = mydict({})
            result.land_url = item['landingPageUrl']
            result.product_id = item['productId']
            result.name = item['productName']
            result.rating = int(item['rating'])
            result.no_of_reviews = item['ratingCount']
            result.dicsount = item['discount']
            result.brand = item['brand']
            result.image = item['searchImage']
            result.image_Set = item['images']
            result.gender = item['gender']
            result.primary_color = item['primaryColour']
            result.category = item['category']
            print(result.category)
            result.real_price = self.cleanify_price(item['mrp'])
            deal_price = item['price']
            if deal_price:
              print('SUb level 1')
              result.deal_price = self.cleanify_price(deal_price)
              result.saving = self.perc_calc(result.real_price,result.deal_price)
              result.saving_num = result.saving[1]
              result.saving = result.saving[0]
              print('Exits')
            else:
              result.deal_price = None
              result.saving = None
              result.saving_num = None
            results.append(result)
          return results

        except:
          return None
      else:
        return None


    def get_results(self):
        res = r().get(self.api_url,headers=self.headers)
        return res

    



''''
plugs = pickle.load(open(plugs_db_loc,'rb'))
plugs['myntra'] = Myntra
plug = pickle.dump(plugs,open(plugs_db_loc,'wb'))
'''

'''
plug_file = open(plugs_db_loc,'rb')
plugs = pickle.load(plug_file)
plug_file.close()
plugs['myntra'] = 'Myntra'
plug_file = open(plugs_db_loc,'wb')
pickle.dump(plug_file,plugs)
plug_file.close()'''
print("Myntra Loaded")
