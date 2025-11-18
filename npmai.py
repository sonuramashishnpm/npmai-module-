
from langchain_core.language_models.llms import LLM
from typing import Any, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#1.GeminiAIMode
class GeminiAIMode(LLM):
    @property
    def _llm_type(self) -> str:
        return "gemini_ai_mode_web_llm"

    def _call(self, prompts: str, stop: Optional[List[str]] = None) -> str:
        driver = None
        try:
            options = Options()
            options.add_argument("--incognito")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            driver = webdriver.Chrome(options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })
            url="https://www.google.com"
            driver.get(url)
            time.sleep(10)
            aimode=driver.find_element(By.CLASS_NAME,"plR5qb")
            aimode.click()
            time.sleep(6)
            query=driver.find_element(By.CLASS_NAME,"ITIRGe")
            query.send_keys(prompts)
            query.send_keys(Keys.RETURN)
            time.sleep(15)
            result=driver.find_element(By.CLASS_NAME,"pWvJNd")
            return result.text

        except Exception as e:
            return f"[Error during NPM AI call: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def invoke(self, prompts: str) -> str:
        return self._call(prompts)


#2.Gemini
class Gemini(LLM):
    driver: Optional[webdriver.Chrome] = None
    @property
    def _llm_type(self) -> str:
        return "gemini_ai_web_llm"
    def __init__(self,**kwargs:Any):
        super().__init__(**kwargs)
        options = Options()
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        })

        self.driver.get("https://gemini.google.com/app")
        self.driver.maximize_window()
        time.sleep(5)

    def _call(self, prompts: str, stop: Optional[List[str]] = None) -> str:
        try:
            prompt_box = self.driver.find_element(
                By.XPATH,
                "/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/"
                "bard-sidenav-content/div[2]/div/div[2]/chat-window/div/input-container/"
                "div/input-area-v2/div/div/div[2]/div/div/rich-textarea/div[1]"
                )
            prompt_box.clear()
            prompt_box.send_keys(prompts)
            prompt_box.send_keys(Keys.RETURN)

            time.sleep(20)
            responses = self.driver.find_elements(By.XPATH, "//model-response//response-container//div/div[2]/div[2]")
            if responses:
                print(responses[-1].text.strip())
            else:
                return "Invalid input. Please enter 'C' or 'O'."

        except Exception as e:
            return f"[Error in Gemini: {str(e)}]"

       

    def invoke(self, prompts: str) -> str:
        return self._call(prompts)
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver=None

#3.ChatGPT
class ChatGPT(LLM):
    driver: Optional[webdriver.Chrome] = None
    @property
    def _llm_type(self) -> str:
        return "chatgpt_web_llm"

    def __init__(self,**kwargs:Any):
        super().__init__(**kwargs)
        options = Options()
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        })
        self.driver.get("https://chatgpt.com/")
        self.driver.maximize_window()
        time.sleep(7)

    def _call(self, prompts: str, stop: Optional[List[str]] = None) -> str:    
        try:
            try:
                cookies = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/button[3]")
                cookies.click()
                time.sleep(2)
            except:
                pass

            prompt_box = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/main/div/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/div[1]/div/div")
            time.sleep(2)
            prompt_box.clear()
            prompt_box.send_keys(prompts)
            time.sleep(2.5)
            prompt_box.send_keys(Keys.RETURN)
            time.sleep(23)
            try:
                login_pop = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/a")
                if login_pop:
                    login_pop.click()
            except:
                pass

            response = self.driver.find_elements(By.XPATH, "//main//article")
            if response:
                final_response = response[-1]
                print(final_response.text)
            else:
                print("Invalid input. Please enter 'C' or 'O'.")

        except Exception as e:
            return f"[Error in ChatGPT: {str(e)}]"

    def invoke(self, prompts: str) -> str:
        return self._call(prompts)
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver=None
#4.Grok
class Grok(LLM):
    @property
    def _llm_type(self) -> str:
        return "grok_web_llm"

    def _call(self, prompts: str, stop: Optional[List[str]] = None) -> str:
        driver = None
        try:
            options = Options()
            options.add_argument("--incognito")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            driver = webdriver.Chrome(options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })
            url="https://grok.com"
            driver.get(url)
            driver.maximize_window()
            time.sleep(10)

            adbtncut=driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/main/div[2]/div/div[2]/div[1]/div[2]/div/button")
            time.sleep(1)
            adbtncut.click()
            time.sleep(4)

            prompt=driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/main/div[2]/div/div[2]/div[1]/div[1]/form/div/div/div[2]/div[1]/textarea")
            time.sleep(2)
            prompt.send_keys(prompts)
            time.sleep(1.6)
            prompt.send_keys(Keys.RETURN)
            time.sleep(30)

            result=driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div[2]/div[2]/div/div[1]")
            return result.text

        except Exception as e:
            return f"[Error in Grok: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def invoke(self, prompts: str) -> str:
        return self._call(prompts)


#5.Perplexity
class Perplexity(LLM):
    @property
    def _llm_type(self) -> str:
        return "perplexity_llm"
    def _call(self,prompts:str,stop:Optional[List[str]] = None) -> str:
        driver=None
        try:
            options = Options()
            options.add_argument("--incognito")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
                })
            wait = WebDriverWait(driver, 30)

            url="https://www.perplexity.ai/"
            driver.get(url)
            time.sleep(1)
            driver.maximize_window()

            prompt=driver.find_element(By.XPATH,"/html/body/main/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/div/span/div/div[1]/div/div[1]/div/div")
            prompt.send_keys(prompts)
            time.sleep(0.5)
            prompt.send_keys(Keys.RETURN)
            time.sleep(17.7)

            result=driver.find_element(By.XPATH,"/html/body/main/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
            time.sleep(3)
            return result.text
        except Exception as e:
            return f"[Error in Perplexity: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    def invoke(self, prompts:str) -> str:
        return self._call(prompts)

   
# Call Code
if __name__ == "__main__":
    models = {"1": GeminiAIMode, "2": Gemini, "3": ChatGPT, "4":Grok, "5":Perplexity}
    choice = input("Choose model 1:-GeminiAIMode,2:-Gemini, 3:-ChatGPT, 4:-Grok, 5:-Perplexity ").strip()
    prompts = input("Enter query: ").strip()
    Selected = models.get(choice, Gemini)
    llm = Selected()
    print(llm.invoke(prompts))
