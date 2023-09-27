import sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fpdf import FPDF

#getting main aguments from terminal
args={}
for i in range(1,len(sys.argv),2):
    args[sys.argv[i]] = sys.argv[i+1]


options = webdriver.FirefoxOptions()
#options.add_argument("-headless")


#request the search web page
driver = webdriver.Firefox(options=options)
driver.get('https://www.zumper.com/')


#find the search box
searchBox = driver.find_element(By.XPATH, '//*[@id="autocomplete-search-input__short-term"]')


#filling the search box
searchBox.send_keys(args['-addr'])
time.sleep(0.5)
searchBox.send_keys(Keys.ENTER)


#css selectors
bedroomsNumSelctor = {'studio':'.css-m5jdfx',
                      '1':'.css-nvpoa5',
                      '2':'.css-1a8tkzh > div:nth-child(2) > div:nth-child(1) > button:nth-child(3)',
                      '3':'.css-1a8tkzh > div:nth-child(2) > div:nth-child(1) > button:nth-child(4)',
                      '4+':'.css-1a8tkzh > div:nth-child(2) > div:nth-child(1) > button:nth-child(5)'
}

bathroomsNumSelctor = {'1':'.css-1jm8wsg > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)',
                       '2':'button.css-1a0me3v:nth-child(2)',
                       '3':'button.css-1a0me3v:nth-child(3)',
                       '4':'button.css-1a0me3v:nth-child(4)',
                       '+5':'button.css-1a0me3v:nth-child(5)'
}


#long and short term
if args['-term'] == 'short':
    while True:
        try:
            shtermbtn = driver.find_element(By.CSS_SELECTOR, "button.css-1ramhdv-button:nth-child(1)")
            shtermbtn.click()
            break
        except:
            pass


else:
    while True:
        try:
            ltermbtn = driver.find_element(By.CSS_SELECTOR, "button.css-1ramhdv-button:nth-child(1)")
            ltermbtn.click()
            break
        except:
            pass
    while True:
        try:
            #choosing bedroom number
            bdroomNumElem = driver.find_element(By.CSS_SELECTOR, bedroomsNumSelctor[args['-bedrooms']])
            bdroomNumElem.click()

            #choosing bathroom number
            bathroomNumElem = driver.find_element(By.CSS_SELECTOR, bathroomsNumSelctor[args['-bathrooms']])
            bathroomNumElem.click()
            break
        except:
            pass

    #click next
    while True:
        try:
            nextbtn = driver.find_element(By.CSS_SELECTOR, '.css-1sfb2c5-button-medium-primarybutton')
            nextbtn.click()
            break
        except:
            pass
    #budget
    while True:
        try:
            bdget = driver.find_element(By.CSS_SELECTOR, '#price')
            bdget.clear()
            bdget.send_keys(args['-budget'])
            break
        except:
            pass
    
    #click search
    while True:
        try:
            srchbtn = driver.find_element(By.XPATH, '/html/body/div[18]/div[4]/div/section/div/div[3]/button')
            srchbtn.click()
            break
        except:
            pass


class House:

    def __init__(self, addr, link, price, images):
        self.addr = addr
        self.link = link
        self.price = price
        self.images = images




houses = []

#number of offers
while True:
        try:
            offersNum = int(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[3]').text[12:14])
            print(offersNum)
            break
        except:
            pass


#getting House instances attributes
i, k = 1, offersNum
while i <= k:
    #getting an offer element
    offer = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[{i}]')

    #offer element class vrification
    if(offer.get_attribute('class'))!='css-8a605h':

        print(offer.get_attribute('class'))
        k += 1
        i += 1
        
    else:
        print(f'scarping house number : {i}')
        while True:
            try:
                #getting attributes from offer element
                addr = offer.find_element(By.XPATH, './/section/div/div[2]/div[1]/div[2]/div[1]/a').text +'\n'+ offer.find_element(By.XPATH, 'section/div/div[2]/div[1]/div[2]/div[1]/div[1]/p').text
                link = offer.find_element(By.XPATH, './/section/div/div[2]/div[1]/div[2]/div[1]/a').get_attribute('href')
                price = offer.find_element(By.XPATH, './/section/div/div[2]/div[1]/div[2]/div[2]/div[2]/p').text
                break
            except:
                pass
            
        images = []
        for j in range(1,5):
            try:
                images.append(offer.find_element(By.XPATH, f'.//section/div/div[1]/div[1]/div[1]/img[{j}]').get_attribute('src'))
            except:
                pass

        
        houses.append(House(addr, link, price, images))

        i += 1


#adding results to a PDF file
pdf = FPDF()
pdf.set_font('Times')
i=1
for house in houses:
    print(f'storing house number : {i} to a pdf file...')
    pdf.add_page()
    pdf.write(h=32, txt=house.addr, link=house.link)
    pdf.write(h=32, txt='\nPrice: '+ house.price + '/Month')
    if len(house.images) >= 1:
        pdf.image(name=house.images[0],x=25,y=115,h=75,w=75)
    if len(house.images) >= 2:
        pdf.image(name=house.images[1],x=110,y=115,h=75,w=75)
    if len(house.images) >= 3:
        pdf.image(name=house.images[2],x=25,y=200,h=75,w=75)
    if len(house.images) >= 4:
        pdf.image(name=house.images[3],x=110,y=200,h=75,w=75)
    i+=1

print('Done!')


pdf.output("pdf-with-image.pdf")

driver.close()
