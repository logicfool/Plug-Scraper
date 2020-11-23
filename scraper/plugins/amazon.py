from .core import *



#gp/offer-listing left
#tip add i=todays-deals in amazon search and it will show you only todays deals !


class Amazon():
    def __init__(self,*args):
        if args:
            url = args[0]
            self.args = args
            self.url = url
            self.request = self.get_source_of_page(self.url)
            self.url = self.request.url
            self.html = self.request.content
            #.raw_info.browse_node_info.browse_nodes[0].ancestor.ancestor.ancestor.context_free_name
            #-------------------------------------------
            #For Search Pages! i.e Urls have '/s?k=query'
            self.soup = BeautifulSoup(self.html,'lxml')
            self.tree = html.fromstring(self.request.content)
            self.results = []
        else:
            ''
    
    def get_source_of_page(self):
        url = self.url
        proxies = {}
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        #time.sleep(10)
        header = Headerss(browser="chrome",os="win",headers=False)
        h = header.generate()
        headers['user-agent'] = h['User-Agent'] 
        working = r().get(url,headers = h,timeout=10)
        return working


    def currency_finder(self):
        url = self.url
        tld = tldextract.extract(url).suffix
        dom_dict = {'in':'₹','com.br':'R$','ca':'$','com':'$','com.mx':'$','cn':'¥','jp':'￥','sg':'S$','ae':'AED','fr':'€','de':'€','it':'€','nl':'€','es':'€','se':'kr','co.uk':'£','com.au':'$'}
        currency = dom_dict[tld]
        return currency

        '''def integerify_price(price):
            intt = ''
            for i in price:
                try:
                    if i == '.':
                        intt = intt+i    
                    else:
                        ii = int(i)
                        intt = intt+i
                except:
                    pass
            #p2 = float(str(round(intt, 2)))
            p2 = float(intt)
            return p2'''
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
        
    def get_prod_asin(self,url1):
        #a = re.search('/dp/(.*?)/',url)
        #b = re.search('/dp/(.*?)')
        url = url1
        aa = url.split('?')
        aa = aa[0]
        aa = aa.split('/')
        asin = None
        asi_num = ''
        num = 0
        for nn in aa:
            if nn == 'dp':
                asi_num = num + 1
            elif nn == 'gp':
                asi_num = num + 2
            else:
                num = num+1
        asin = aa[asi_num]
        return asin
    

    def get_product_details(self,*urls):
        if self.args:
            pass
        else:
            return 'No Url passed!'
        soup = self.soup
        try:
            name = soup.find('span',{'id':'productTitle'}).text.strip()
        except:
            self.results['error'] = 404
            return ''
        asin = self.get_prod_asin(self.url)
        hasdeal = soup.findAll('span',{'class':'priceBlockStrikePriceString'})
        currency = self.currency_finder()
        check_image = soup.find('div',{'id':'imgTagWrapperId'})
        category = soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")
        url = self.url
        if category:
            li = category[0].findAll('li')
            category = []
            if li:
                for lii in li:
                    textt = lii.text.strip()
                    if textt == '›':
                        pass
                    else:
                        category.append(textt)
            else:
                category = []
        else:
            category = []
        
        if check_image:
            try:
                image = check_image.find('img')['data-old-hires']
            except:
                image = 'https://lh3.googleusercontent.com/proxy/G0EdAWaCo8LCRP3pxnYOHLuR0iaz3lnP4ci9WRzX_8rbKSctgDgYR1cFJppqAJBA_L_Q0399JeR1OpTBvOVDxKPHmBCxknfPKXBBgPvbg5wbYXKZEAgc8jSiM5c2WuKXnx9YXEe4aU24T1lYAke3JF2KsDw-1Ak'
            image_set = []
            try:
                aa = check_image.find('img')['data-a-dynamic-image']
                aa = aa.split('{')[1].split('}')[0].split(',"')
                for bb in aa:
                    cc = bb.split('":')[0].replace('"','')
                    dd = bb.split('":')[1]
                    dd = dd.replace('[','')
                    dd = dd.replace(']','')
                    bb = [cc,dd]
                    image_set.append(bb)
            except:
                image_set = []
        else:
            image = 'https://lh3.googleusercontent.com/proxy/G0EdAWaCo8LCRP3pxnYOHLuR0iaz3lnP4ci9WRzX_8rbKSctgDgYR1cFJppqAJBA_L_Q0399JeR1OpTBvOVDxKPHmBCxknfPKXBBgPvbg5wbYXKZEAgc8jSiM5c2WuKXnx9YXEe4aU24T1lYAke3JF2KsDw-1Ak'
            image_set = []
            
        if hasdeal:
            real_price = self.cleanify_price(hasdeal[0].text)
            hasdeal = True
            deal_price_1 = soup.find('span',{'id':'priceblock_dealprice'})
            deal_price_2 = soup.find('span',{'id':'priceblock_saleprice'})
            deal_price_3 = soup.find('span',{'id':'priceblock_ourprice'})
            if deal_price_1:
                deal_price = self.cleanify_price(deal_price_1.text)
            elif deal_price_2:
                deal_price = self.cleanify_price(deal_price_2.text)
            elif deal_price_3:
                deal_price = self.cleanify_price(deal_price_3.text)
            else:
                deal_price = None
            try:
                saving = self.perc_calc(real_price,deal_price)
                saving_num = saving[1]
                saving = saving[0]
            except:
                try:
                    saving = soup.find('td',{'class':'priceBlockSavingsString'}).text
                    saving = saving.replace('\n','')
                    saving = saving.split()[-1]
                    saving = saving_num = int(self.cleanify_price(saving))
                    saving = f'{saving}% Off'
                except:
                    saving = None
                    saving_num = None
        else:
            hasdeal = False
            real_price = self.cleanify_price(soup.find('span',{'id':'priceblock_ourprice'}).text)
            deal_price = None
            saving = None
            saving_num = None
        #coupon = soup.find('div',attrs = {'class':'vpcApplyCoupon'})
        coupon = soup.select('.vpcApplyCoupon span.a-label')
        try:
            coupon = coupon[0].text.strip()
            coupon = coupon.replace('\n','')
            coupon = coupon.replace('Apply ','')
        except IndexError:
            coupon = None
        try:
            deal_type =  re.search('"dealType" : "(.*?)"',str(soup))
            deal_type = deal_type[1]
            if deal_type == 'LIGHTNING_DEAL':
                deal_type = 'Lightning Deal'
            elif deal_type == 'DEAL_OF_THE_DAY':
                deal_type = 'Deal Of The Day'
            else:
                deal_type = deal_type
        except:
            deal_type = None
        rating = soup.find('i',{'data-hook':'average-star-rating'})
        try:
            rating = rating.text.strip()
            no_of_reviews1 = soup.find('span',{'class':'acrCustomerReviewText'})
            no_of_reviews2 = soup.find('span',{'id':'acrCustomerReviewText'})
            if no_of_reviews1:
                no_of_reviews = no_of_reviews1.text.strip()
                no_of_reviews = int(no_of_reviews.split()[0].replace(',',''))
            elif no_of_reviews2:
                no_of_reviews = no_of_reviews2.text.strip()
                no_of_reviews = int(no_of_reviews.split()[0].replace(',',''))
            else:
                no_of_reviews = None
        except TypeError:
            rating = None
            no_of_reviews = None
        features = soup.find('div',{'id':'feature-bullets'})
        try:
            ul = features.find('ul')
            features = []
            if ul:
                li = ul.findAll('li')
                for lis in li:
                    lis = lis.text.strip()
                    features.append(lis)
            else:
                features = []
        except TypeError:
            features = []
        offers = soup.find('div',{'data-feature-name':"sopp"})
        try:
            ul = offers.find('ul')
            offers = []
            if ul:
                li = ul.findAll('li')
                bad_text = ['Click here','Check eligibility here',"Here's how",'Sign up for free','See ']
                for lis in li:
                    lii = lis.findAll('a')
                    lis = lis.text.strip()
                    lis = lis.replace('\n','')
                    for bad_text1 in bad_text:
                            bad_text1 = bad_text1.strip()
                            try:
                                lis = re.findall(f"(.*?){bad_text1}",lis,re.DOTALL)[0].strip()
                            except:
                                pass
                    '''try:
                        li1 = re.findall("(.*?)Here's",lis,re.DOTALL)[0].strip()
                    except:
                        li1 = "" ''' 
                    offers.append(lis)
            else:
                offers = []
        except:
            offers = []
        
        try:
            available = soup.select('#availability')[0].strip()
            available = available.lower()
            if 'out' in available:
                available = False
            elif available == '':
                available = True
        #except TypeError:
        except:
            available = True
        else:
            available = available
        ends_in = soup.find('span',text = re.compile(r'Ends in'))
        try:
            ends_in = ends_in.get_text().strip()
        except:
            ends_in = None
        results = {}
        results['asin'] = asin
        results['url'] = url
        results['name'] = name
        results['image'] = image
        results['image_set'] = image_set
        results['categories'] = category
        results['currency'] = currency
        results['is_deal'] = hasdeal
        results['deal_price'] = deal_price
        results['real_price'] = real_price
        results['savings'] = saving
        results['saving_num'] = saving_num
        results['ratings'] = rating
        results['deal_type'] = deal_type
        results['no_of_reviews'] = no_of_reviews
        results['available'] = available
        results['features'] = features
        results['offers'] = offers
        results['coupon'] = coupon
        results['ends_in'] = ends_in
        self.results.append(mydict(results))
        
    def get_search_query(self):
        if self.args:
            pass
        else:
            return 'No Url passed!'
        soup = self.soup
        get_results = soup.findAll('div',{'data-component-type':"s-search-result"})
        #cc = open('results.txt','w').close()
        cc = open('results.txt','a')
        url_info = get_domain_info(self.url)
        for i in get_results:
            url = i.find('a',{'class':'a-link-normal'})['href'].strip()
            url = url_info['full']+url
            try:
                asin = re.search('data-asin="(.*?)"',str(i))[1]
            except:
                print('Erorrororororor')
                return False
            name  = i.find('span',{'class':'a-text-normal'}).text
            rating  = i.find('a',{'class':'a-popover-trigger'})
            try:
                rating = rating.text
            except:
                rating = None
            try:
                imgurl = i.find('img',{'class':'s-image'})['src']
            except:
                imgurl = None
            try:
                deal_type = i.findAll('span',{'class':'a-badge-text'})
                deal_type1 = ''
                if deal_type:
                    for deals_type in deal_type:
                        textt = deals_type.text
                        if '%' in textt:
                            pass
                        else:
                            deal_type1 = deal_type1+textt
                    deal_type = deal_type1.strip()
                else:
                    deal_type = None
            except:
                deal_type = None
            mrp = i.findAll('span',{'class':'a-price'})
            currency_symbol = self.currency_finder()
            if mrp:
                try:
                    hasdeal = mrp[1]
                    hasdeal = True
                except:
                    hasdeal  = False
                if hasdeal:
                    deal_price = self.cleanify_price(mrp[0].find('span',{'class':'a-offscreen'}).text.strip())
                    real_price = self.cleanify_price(mrp[1].find('span',{'class':'a-offscreen'}).text.strip())
                    try:
                        saving = self.perc_calc(real_price,deal_price)
                        saving_num = saving[1]
                        saving  = saving[0]
                    except:
                        try:
                            saving = i.find('div',{'class':"a-row a-size-base a-color-base"}).find('span',{'dir':'auto'}).text
                            saving_num = self.cleanify_price(saving)    
                        except:
                            saving = saving_num =  None
                else:
                    real_price = self.cleanify_price(mrp[0].find('span',{'class':'a-offscreen'}).text.strip())
                    deal_price = None
                    saving = saving_num =  None
            else:
                real_price = None
                deal_price = None
                saving = saving_num = None
            result = {}
            result['asin'] = asin
            result['url'] = url
            result['name'] = name
            result['image'] = imgurl
            if mrp:
                if hasdeal:
                    result['is_deal'] = True
                    result['deal_price'] = deal_price
                    result['real_price'] = real_price
                    result['saving'] = saving
                    result['currency'] = currency_symbol
                else:
                    result['is_deal'] = False
                    result['currency'] = currency_symbol
                    result['real_price'] = real_price
                    result['deal_price'] = None
                    result['saving'] = False
            else:
                result['is_deal'] = False
                result['currency'] = None
                result['deal_price'] = None
                result['real_price'] = None
                result['saving'] = None
            result['rating']  = rating
            result['deal_type'] = deal_type
            result['saving_num'] = saving_num
            self.results.append(mydict(result))

    #----------------------------------------------------------------

    #----------------------------------------------------------------
    #For deal pages that have '/deal/{}' in url


    def get_deal_query(self):
        if self.args:
            pass
        else:
            return 'No Url passed!'
        soup = self.soup
        get_results = soup.find('div',{'id':'octopus-dlp-asin-stream'})
        ul = get_results.find('ul',{'class':'a-unordered-list'})
        all_list = ul.findAll('li')
        main_title = soup.find('h1',{'role':'heading'}).text.strip()
        url_info = get_domain_info(self.url)
        for ii in all_list:
            url1 = ii.find('a',{'class':'a-link-normal'})['href']
            url = url_info['full']+url1
            asin = self.get_prod_asin(url)
            name = ii.find('span',{'class':'a-size-base a-color-base'}).text.strip()
            imgurl = ii.find('img',{'class':'octopus-dlp-asin-image'})['src']
            try:
                star = ii.find('i',{'class':'a-icon-star-mini'})['class'][2].replace('a-star-mini-','')
                rating = star.replace('-','.')
            except:
                rating = None
            try:
                deal_type = ii.find('span',{'class':'oct-acs-pc-badge'}).text
            except:
                deal_type = None
            hasdeal  = ii.find('span',{'class':'octopus-widget-strike-through-price'})
            if hasdeal:
                deal_price = self.cleanify_price(ii.find('span',{'class':'octopus-widget-price'}).text.lower())
                currency_symbol = self.currency_finder()
                #currency_symbol = 'Rs'
                deal_price = int(deal_price)
                real_price = self.cleanify_price(ii.find('span',{'class':'octopus-widget-strike-through-price'}).text)
            else:
                currency_symbol = self.currency_finder()
                real_price = self.cleanify_price(ii.find('span',{'class':'octopus-widget-price'}).text.lower())
                deal_price = None
            try:
                saving = self.perc_calc(real_price,deal_price)
                saving_num = saving[1]
                saving  = saving[0]
            except:
                try:
                    saving = ii.find('span',{'class':'octopus-widget-price-saving-percentage'}).text.strip()
                    saving = saving.replace('(','')
                    saving = saving.replace(')','')
                    saving_num = self.cleanify_price(saving)        
                except:
                    saving = saving_num = None
                    
            result = {}
            result['main_title'] = main_title
            result['url'] = url
            result['asin'] = asin
            result['name'] = name
            result['image'] = imgurl
            result['currency'] = currency_symbol
            result['deal_price'] = deal_price
            result['real_price'] = real_price
            result['rating'] = rating
            result['saving'] = saving
            result['saving_num'] = saving_num
            result['deal_type'] = deal_type
            result['is_deal'] = True
            self.results.append(mydict(result))
        
    def get_store_pages(self):
        self.request.html.render()
        ul = self.request.html.find('ul')
        try:
            nnn = ''
            nn = 0
            for ull in ul:
                ull = str(ull)
                if 'style__grid' in ull:
                    nnn = nn
                else:
                    nn = nn+1
            if nnn:
                ul = ul[nnn]
            else:
                self.results.append({'Error':404111})
                return ''
        except:
            self.results.append({'Error':404111})
            return ''
        url_info = get_domain_info(self.url)
        if ul:
            ul = ul.html
            self.soup = BeautifulSoup(ul,'lxml')
            li11 = self.soup.findAll('li')
            self.li = li11
            print(len(li11))
            for lii in li11:
                try:
                    name = lii.select('a[class*="style__title"]')[0].text.strip()
                    url = lii.select('a[class*="style__title"]')[0]['href']
                    url = url_info['full']+url
                    asin = self.get_prod_asin(url)
                except:
                    self.results.append({'Error':4041})
                    return ''
                img = lii.select('div[class*="style__image_"]')
                if img:
                    img = img[0].find('img')['src']
                else:
                    img = 'https://lh3.googleusercontent.com/proxy/G0EdAWaCo8LCRP3pxnYOHLuR0iaz3lnP4ci9WRzX_8rbKSctgDgYR1cFJppqAJBA_L_Q0399JeR1OpTBvOVDxKPHmBCxknfPKXBBgPvbg5wbYXKZEAgc8jSiM5c2WuKXnx9YXEe4aU24T1lYAke3JF2KsDw-1Ak'
                rating = lii.select('i[class*="style__stars"]')[0].text.strip()
                no_of_reviews = int(self.cleanify_price(lii.select('span[class*="style__reviewCount"]')[0].text.strip()))
                currency = lii.select('span[class*="style__currency"]')[0].text.strip()
                try:
                    hasdeal = lii.select('span[class*="style__strikePrice"]')[0]
                    print('Has deal!!!\n\n--')
                    deal_price = self.cleanify_price(lii.select('span[class*="style__buyPrice"]')[0].text.strip())
                    print(f'Deal Price : {deal_price}\n--')
                    real_price = self.cleanify_price(hasdeal.text.strip())
                    print(f'real Price : {real_price}\n--')
                    print('\n\n----------------------------------------------------')
                    hasdeal = True
                    saving = self.perc_calc(real_price,deal_price)
                    saving_num = saving[1]
                    saving = saving[0]
                except:
                    hasdeal = False
                    real_price = self.cleanify_price(lii.select('span[class*="style__buyPrice"]')[0].text.strip())
                    deal_price = None
                    saving = None
                    saving_num = None
                try:
                    deal_type = lii.select('div[class*="dealHeader_"')[0].text.strip()
                    deal_type = deal_type.replace('\xa0',' ')
                except:
                    deal_type = None
                results = {}
                results['asin'] = asin
                results['url'] = url
                results['name'] = name
                results['image'] = img
                results['is_deal'] = hasdeal
                results['currency'] = currency
                results['deal_price'] = None
                results['real_price'] = real_price
                results['saving'] = saving
                results['saving_num'] = saving_num
                results['rating'] = rating
                results['no_of_reviews'] = no_of_reviews
                results['deal_type'] = deal_type
                self.results.append(mydict(results))
        else:
            self.results.append('Error:404')

    #For rest pages That I dont know how they work!
    def get_hybrid_query(self):
        soup = self.soup
        hybrid_type1 = soup.find('div',{'id':'search-results'})
        if hybrid_type1:
            ul = hybrid_type1.find('ul')
            if ul:
                li1 = ul.findAll('li',{'class':'s-result-item'})
                if li1:
                    for lists in li1:
                        asin = lists['data-asin']
                        img = lists.find('img')['src']
                        name = lists.find('h2',{'class':'s-access-title'}).text
                        '''try:
                            mrp = deal_price = lists.find('span',{'class':'s-price'})
                            mrp = True
                        except:
                            mrp = False'''
                        try:
                            real_price = lists.find('span',{'class':'a-text-strike'})
                            if real_price:
                                hasdeal = True
                            else:
                                hasdeal = False
                        except:
                            hasdeal = False
                        if hasdeal:
                            #print('HAsdeal')
                            try:
                                deal_price = self.cleanify_price(lists.find('span',{'class':'s-price'}).text)
                                #deal_price = deal_price.strip()
                            except:
                                deal_price = None
                            #print(deal_price)
                            #deal_price = deal_price.strip()
                            #deal_price = deal_price.replace('\xa0','')
                            #deal_price = deal_price.strip()
                            try:
                                real_price = self.cleanify_price(lists.find('span',{'class':'a-text-strike'}).text)
                            except:
                                real_price = None
                            currency_symbol = self.currency_finder()
                            is_deal = True
                            try:
                                try:
                                    saving = self.self.perc_calc(real_price,deal_price)
                                    saving_num = saving[1]
                                    saving  = saving[0]
                                except:
                                    saving = lists.findAll('span',{'class':'a-color-price'})[2].text.strip()
                                    saving_num = self.cleanify_price(saving)
                            except:
                                saving = saving_num =  None

                        else:
                            real_price = self.cleanify_price(lists.find('span',{'class':'s-price'}).text)
                            #print(real_price)
                            #real_price = real_price.replace('\xa0','') #INR symbol
                            #real_price = real_price.strip()
                            deal_price = None
                            currency_symbol = self.currency_finder()
                            saving = None
                            is_deal = False
                        try:
                            deal_type = lists.find('span',{'class':'a-badge-text'}).text.strip()
                        except:
                            deal_type = None
                        try:
                            rating = lists.find('span',{'class':'a-icon-alt'}).text
                        except:
                            rating = None
                        result = {}
                        result['asin'] = asin
                        result['name'] = name
                        result['image'] = img
                        result['deal_price'] = deal_price
                        result['real_price'] = real_price
                        result['rating'] = rating
                        result['saving'] = saving
                        result['deal_type'] = deal_type
                        result['is_deal'] = is_deal
                        result['currency'] = currency_symbol
                        result['saving_num'] = saving_num
                        self.results.append(mydict(result))
                else:
                    pass
        else:
            pass
    def get_result(self):
        url = self.url
        if ('/dp' in url) or ('/gp/product' in url):
            self.get_product_details()
        elif '/stores' in url:
            self.get_store_pages()
        elif '/s' in url:
            self.get_search_query()
            if self.results == []:
                self.get_hybrid_query()
        elif '/deal' in url:
            self.get_deal_query()
        else:
            self.get_hybrid_query()
        return self.results

#Another Not implimented way to store plugin data so scraper can access it

'''
plugs = pickle.load(open(plugs_db_loc,'rb'))
plugs['amazon'] = Amazon
plug = pickle.dump(plugs,open(plugs_db_loc,'wb'))


plug_file = open(plugs_db_loc,'rb')
plugs = pickle.load(plug_file)
plug_file.close()
plugs['amazon'] = 'Amazon'
plug_file = open(plugs_db_loc,'wb')
pickle.dump(plug_file,plugs)
plug_file.close()'''
print("Amazon Loaded")
