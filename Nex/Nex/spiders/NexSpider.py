import scrapy
import json 
import time

from ..NexItem import NexItem

from DrissionPage import ChromiumPage
from urllib.parse import urlencode
    

class NexspiderSpider(scrapy.Spider):
    """
    主要运行逻辑
    """
    
    name = "Nex" 
    allowed_domains = ["www.zhipin.com"] 

    def __init__(self,salary:int = 0 ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 初始化 DrissionPage 的 ChromiumPage 驱动
        # 这会启动一个由 DrissionPage 控制的浏览器实例。
        self.driver = ChromiumPage()
        
        # 滚动配置
        self.scroll_num = 10        # 滚动10次
        self.scroll_time_wait = 10  # 滚动完成之后的停摆时间
        self.scroll_lenth = 2000    # 1000 进行滚动
        self.salary:int             # 整数
        # 查询语句配置
        if salary == 0:
            self.salary = 0
        else:
            self.salary = int(salary) + 401
        
        # 记录驱动已初始化的日志信息。
        # self.logger 是 Scrapy 内置的日志记录机制。
        self.logger.info(" >>> DrissionPage 驱动已初始化。")
        
        self.logger.info(" >>> 正在处理筛选条件 ")
        
    def start_requests(self):
        """
        处理特定的 API 接口
        """
        
        # 工资查询
        if self.salary == 401:
            target_api_keyword = "/wapi/zpgeek/pc/recommend/job/list.json"
        else :
            params = {'salary': self.salary}
            target_api_keyword = f"/wapi/zpgeek/pc/recommend/job/list.json?{urlencode(params)}"

        # target_api_keyword = "/wapi/zpgeek/pc/recommend/job/list.json"
        
        self.logger.info(f" >>> 开始监听包含以下内容的请求: {target_api_keyword}")
        
        # 启动 DrissionPage 监听器。它将监控网络流量中
        # URL 包含 'target_api_keyword' 的请求。
        # 注意：listen.start() 不直接返回捕获的数据；
        # 它只是启动监听过程。
        self.driver.listen.start(target_api_keyword)

        # ————————————————————————————— 触发 API 请求 ———————————————————————————————
        # 定义要导航到的初始 URL。这个页面的加载（或页面上的交互）
        # 预计会触发我们正在监听的 API 调用。
        initial_page_url = 'https://www.zhipin.com/web/geek/jobs' 
        if self.salary-401:
            initial_page_url = f'https://www.zhipin.com/web/geek/jobs?city=101210100&salary={self.salary}'

        # 记录驱动即将访问的 URL
        self.logger.info(f" >>> 驱动正在访问 URL: {initial_page_url} 访问的json文件是{target_api_keyword}")
        self.driver.get(initial_page_url)
        self.driver.wait.load_start()
        
        self.logger.info(" >>> 滚动搜索")
        
        for i in range(self.scroll_num):
            
            # 日志输出
            self.logger.info(" >>> 开始进行滚动")
            
            # 进行滚动
            self.driver.scroll(self.scroll_lenth)
            
            # 等待数据加载
            self.logger.info(" >>> 等待记载")
            time.sleep(self.scroll_time_wait)
            
            # 等待滚动后监听的新请求
            self.logger.info(" >>> 等待新请求")
            
            try:
                # 等待监听器捕获与 'target_api_keyword' 匹配的请求。
                # 'timeout=20' 表示它将最多等待 20 秒。
                # 如果成功，'captured_details' 将是一个 DrissionPage 的 PacketDetails 对象，
                # 如果超时或未找到匹配请求，则为 None。
                captured_details = self.driver.listen.wait( timeout = 20 )
                
                # TODO: 这里判断一下 是不是出现了一个标签

            # 检查是否成功捕获到请求并且该请求有响应体。
                if captured_details and captured_details.response:
                    self.logger.info(f" >>> 已捕获目标 API 请求: {captured_details.url}")
                
                    api_response_object = captured_details.response.body

                    # 生成一个 Scrapy 请求，将捕获到的数据传递给一个解析方法
                    # 我们使用 'initial_page_url' 作为此 Scrapy 请求的 URL
                    # 但它也可以是 'captured_details.url' 或一个占位符 URL
                    # 实际数据通过 'meta' 字典传递。
                    yield scrapy.Request(
                        url=initial_page_url, 
                        callback=self.parse_api_data,                   # 指定回调方法
                        meta={'api_data_object': api_response_object},  # 传递捕获到的数据
                        dont_filter=True                                # 即使 URL 已被访问过，也允许此请求
                    )
                
                else:
                    self.logger.warning(" >>>warning 监听器未捕获到目标 API 请求或响应为空 ")
                    yield scrapy.Request(
                        url=initial_page_url, 
                        callback=self.parse_page_fallback, 
                        meta={'drission_html': self.driver.html},       # 传递当前页面的 HTML
                        dont_filter=True
                    )
                    
                    self.logger.info("无最新的消息！")
                    break;
            
            except RuntimeError as e:
                self.logger.error(f" >>>err listen.wait() 期间发生错误: {e}")
                
                yield scrapy.Request(
                    url = initial_page_url, 
                    callback=self.parse_page_fallback, 
                    meta={'drission_html': self.driver.html}, 
                    dont_filter=True)

            finally:
                # 无论是否发生异常，此代码块总是会执行。
                # 当不再需要监听器时（对于此特定操作而言），停止它是很好的做法。
                self.logger.info(" >>> 正在停止监听器")

# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def parse_api_data(self, response):
        """
        response : 服务器返回的参数
        
        """
        api_data_object = response.meta.get('api_data_object')
        final_data_dict = None

        if api_data_object is not None:
            # 如果是自带你 那么就 赋值给  final_data_dict
            if isinstance(api_data_object, dict):
                self.logger.info(" >>> API 数据作为预解析的字典接收")
                final_data_dict = api_data_object
                
            # B .如果是bite流 那么就 分解到 字典模式 
            elif isinstance(api_data_object, bytes):
                self.logger.info(" >>> API 数据作为字节串接收。尝试解码并解析为 JSON")
                try:
                    api_data_str = api_data_object.decode('utf-8')
                    final_data_dict = json.loads(api_data_str)
                except UnicodeDecodeError:
                    with open('test_raw_api_error_unicode.dat', 'wb') as file:
                        file.write(api_data_object)
                except json.JSONDecodeError:
                    self.logger.error(" >>> json 解析错误")
                    with open('test_api_not_json_error.txt', 'w', encoding='utf-8') as file:
                        file.write(api_data_str)
                except Exception as e:
                    self.logger.error(f" >>> 处理 API {e}")
                    with open('test_api_processing_error_bytes.dat', 'wb') as file:
                        file.write(api_data_object)
                
            else:
                self.logger.error(f" >>>error API 数据的类型非预期: {type(api_data_object)}")
                with open('test_api_unexpected_type.txt', 'w', encoding='utf-8') as file:
                    file.write(str(api_data_object))

            if final_data_dict is not None and isinstance(final_data_dict, dict):
                
                # 保存到json文件里面去
                filename = 'boss_api_data.json'
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(final_data_dict, f, ensure_ascii=False, indent=4)
                    self.logger.info(f"API 数据已成功保存至 {filename}")
                except Exception as e:
                    self.logger.error(f"将 final_data_dict 保存到 JSON 文件时出错: {e}")
                    with open('boss_api_data_save_error.txt', 'w', encoding='utf-8') as f:
                        f.write(str(final_data_dict))

                zp_data_dict = final_data_dict.get('zpData')
                jobs_data_list = None

                if isinstance(zp_data_dict, dict):
                    jobs_data_list = zp_data_dict.get('jobList')
                else:
                    self.logger.warning(f" >>>warning 期望 'zpData' 是一个字典，但得到的是 {type(zp_data_dict)}")

                if jobs_data_list and isinstance(jobs_data_list, list):
                    self.logger.info(f"找到对应的joblist内容，共 {len(jobs_data_list)} 条。")
                    for job_data in jobs_data_list:
                        if not isinstance(job_data, dict):
                            self.logger.warning(f" >>>warning Skipping non-dict job_data: {job_data}")
                            continue
                            
                        try:
                            #  用自定义的类型 封装信息
                            item =NexItem()
                        except AttributeError:
                            self.logger.error(" >>>error 无法实例化  "
                                              " 请检查中的类定义和此处的调用方式 ")
                            continue

                        item['boss_name'] = job_data.get('bossName')
                        item['job_name'] = job_data.get('jobName')
                        item['job_salary'] = job_data.get('salaryDesc')
                        item['job_labs'] = job_data.get('jobLabels')
                        item['skills'] = job_data.get('skills')
                        item['job_exper'] = job_data.get('jobExperience')
                        item['job_degree'] = job_data.get('jobDegree')
                        item['area_district'] = job_data.get('areaDistrict')
                        item['business_location'] = job_data.get('businessDistrict')
                        item['brand_name'] = job_data.get('brandName')
                        yield item
                        
                else:
                    self.logger.warning(f" >>>warning 在 API 响应中未找到 'jobList' 列表，或者它不是一个列表。Found: {type(jobs_data_list)}")
                    
        else: 
            self.logger.warning(" >>>warning 在 response.meta 中未找到 'api_data_object'。无数据可处理。")
                
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def parse_page_fallback(self, response): 
        """
        如果捕获 API 数据失败 ...
        """
        # 检索从 start_requests 传递过来的 HTML 内容。
        # 如果 'drission_html' 不在 meta 中，则回退到 Scrapy 的 response.text
        drission_html = response.meta.get('drission_html', response.text) 
        
        self.logger.info(f" >>> 备选方案: 正在为 {response.url} 解析页面内容 ")
        
        # 将备选的 HTML 内容保存到文件以供检查。
        # 这对于调试 API 可能失败的原因或查看主页面上有哪些数据很有用。
        with open('fallback_page_content.html', 'w', encoding='utf-8') as f:
            f.write(drission_html)
            
        self.logger.info(" >>> 备选页面的 HTML 已保存")
        
        # TODO: 在此处添加逻辑，使用 Scrapy 选择器解析 'drission_html'，
        #       或者如果需要复杂交互，则将其重新加载到 DrissionPage 对象中。
        #       例如:
        # from scrapy.selector import Selector
        # sel = Selector(text=drission_html)
        # titles = sel.xpath('//h1/text()').getall()
        # for title in titles:
        #     self.logger.info(f"备选方案找到标题: {title}")
        #     # 如果适用，yield item





# —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    def spider_closed(self, spider, reason):
        
        """
        清理一下
        """
        self.logger.info(f" >>info 爬虫已关闭: {reason}。正在关闭 DrissionPage 驱动 ")
        # 在尝试退出之前，检查驱动属性是否存在且不为 None。
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit() # 关闭浏览器并释放资源。
            self.logger.info("DrissionPage 驱动已成功退出。")

    