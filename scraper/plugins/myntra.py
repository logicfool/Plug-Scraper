from .core import *

class Myntra():
    def __init__(self,*args):
        if args:
            self.url = args[0]
        else:
            raise Exception(NameError,"URL NOT PASSED")
        self.all_results = []

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

    def get_results(self):
      res = r().get(self.url,headers = self.gen_headers())
      self.html = res.html
      pattern = re.compile('var pageStateData = (.*?);')
      pattern1 = re.compile('window.__myx = (.*)')
      soup = BeautifulSoup(res.text, "lxml")
      scripts = soup.find_all('script')
      self.all_results = []
      if scripts:
        for script in scripts:
          if pattern1.match(str(script.string)):
              self.data = pattern1.match(str(script.string))
              self.stock = json.loads(self.data.groups()[0])
              self.data = self.stock
      else:
        scripts = False
      if scripts:
        try:
          self.results = self.data['searchData']['results']['products']
          result = mydict({})
          domain = get_domain_info(self.url)
          for item in self.results:
            result = mydict({})
            result.url = domain.full+'/'+item['landingPageUrl']
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
            real_price = item['mrp']
            deal_price = item['price']
            if real_price == deal_price:
              result.real_price = self.cleanify_price(real_price)
              result.deal_price = None
              result.is_deal = False
              result.saving = None
              result.saving_num = None
            else:
              result.real_price = self.cleanify_price(real_price)
              result.deal_price = self.cleanify_price(deal_price)
              result.is_deal = True
              result.saving = self.perc_calc(real_price,deal_price)
              result.saving_num = result.saving[1]
              result.saving = result.saving[0]
            self.all_results.append(result)
          return self.all_results

        except:
          try:
            self.results = self.data['pdpData']
            result = self.results
            results = mydict({})
            results.product_id = result['id']
            results.name = result['name']
            price = result['price']
            real_price = price['mrp']
            deal_price = price['discounted']
            if real_price == deal_price:
              results.real_price = self.cleanify_price(real_price)
              results.deal_price = None
              results.is_deal = False
              results.saving = None
              results.saving_num = None
            else:
              results.real_price = self.cleanify_price(real_price)
              results.deal_price = self.cleanify_price(deal_price)
              results.is_deal = True
              results.saving = self.perc_calc(real_price,deal_price)
              results.saving_num = results.saving[1]
              results.saving = results.saving[0]
            analytics = result['analytics']
            results.category = analytics['masterCategory']
            results.sub_category  = analytics['subCategory']
            results.type = analytics['articleType']
            results.extra_info = result['articleAttributes']
            results.offers = result['discounts']
            results.extra_offers = result['offers']
            self.all_results.append(results)
            return self.all_results
          except:
            return self.all_results

      else:
        return self.all_results
        

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
