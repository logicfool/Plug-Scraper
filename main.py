from scraper import * #Load all plugins and core module

url = 'https://www.amazon.in/Rugged-Extra-Tough-Unbreakable-Braided/dp/B0789LZTCJ/ref=gbps_img_s-5_2299_ebed5fcf?smid=A14CZOWI0VEHLG&pf_rd_p=f3aaeb13-62aa-445b-aeff-6ddd854a2299&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=XTK3MJN5HF2JW8RR57XB'

result = scrap_data(url)

#print(result)

#You can try it in terminal load it and in between change module add plugins and use reload_plugins function and it will start reflecting

url1 = 'https://www.amazon.in/l/22429860031/ref=gbps_img_s-5_859c_21d97e9f?smid=A23AODI1X2CEAE&pf_rd_p=daa47517-5bef-4e97-b82e-ec3e7d37859c&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=B3JFQDYNJ5SFH7BCBCG6'

result1 = scrap_data(url)
