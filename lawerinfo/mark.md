## 问题及解决办法

### 问题1：Cookie失效问题，一直返回412
学校门户网站都采用了反爬虫机制，导致通过代码请求接口时候，Cookie过期时间很短，很容易失效，导致返回的页面的body只是一个js文件，无法获取正常数据。通过selenium方法可以获取最新的Cookie，原理是selenium调动本地的浏览器插件，通过浏览器访问后获取Cookie值，方法是获取浏览器对应版本的插件，然后放到Python运行环境的Scripts目录下面，在代码里调用即可。


### 问题2：使用selenium后，仍然无法绕过反爬虫机制

反爬虫机制能够监测出是否使用selenium，所以仍然识别为爬虫。解决办法是使用stealth.min.js文件防止selenium被检测。

        stealth.min.js文件来源于puppeteer，有开发者给 puppeteer 写了一套插件，叫做puppeteer-extra。其中，就有一个插件叫做puppeteer-extra-plugin-stealth专门用来让 puppeteer 隐藏模拟浏览器的指纹特征。

        python开发者就需要把其中的隐藏特征的脚本提取出来，做成一个 js 文件。然后让 Selenium 或者 Pyppeteer 在打开任意网页之前，先运行一下这个 js 文件里面的内容。


运行代码：
    
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--headless")
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0  Safari/537.36')

    driver = webdriver.Chrome(options=option)

    with open('stealth.min.js') as f:
        js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
    })

    driver.get("https://law.sysu.edu.cn/library/books?page=1")
    cookie_list = driver.get_cookies()

运行之后能够顺利绕过，返回状态码200，顺利获取数据。


### 问题3：BeautifulSoup解析页面，找到tbody标签，子标签有很多空白标签，遍历时候有问题

判断子标签是否是tr标签，如果是tr标签才进行处理。