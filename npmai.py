from langchain_core.language_models.llms import LLM
from typing import Any, List, Optional, Union
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
import subprocess

def get_chrome_major_version():
    out = subprocess.check_output(
        r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
    ).decode()
    version = re.search(r"(\d+)\.", out).group(1)
    return int(version)

PromptType = Union[str, List[str], dict]

#1.GeminiAIMode
class GeminiAIMode(LLM):
    @property
    def _llm_type(self) -> str:
        return "gemini_ai_mode_web_llm"

    def _call(self, prompts: PromptType, stop: Optional[List[str]] = None) -> str:
        text_prompt = self._format_prompt(prompts)
        driver: Optional[uc.Chrome] = None
        try:
            options = uc.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--no-first-run")
            options.add_argument("--no-service-autorun")
            options.add_argument("--password-store=basic")
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = uc.Chrome(
                options=options,
                headless=False,
                version_main=get_chrome_major_version()
                )
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })
            url="https://www.google.com"
            driver.get(url)
            time.sleep(10)
            aimode = driver.find_element(By.CLASS_NAME,"plR5qb")
            aimode.click()
            time.sleep(6)
            query = driver.find_element(By.CLASS_NAME,"ITIRGe")
            query.send_keys(text_prompt)
            query.send_keys(Keys.RETURN)
            time.sleep(15)
            result = driver.find_element(By.CLASS_NAME,"pWvJNd")
            return result.text

        except Exception as e:
            return f"[Error during NPM AI call: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def invoke(self, prompts: PromptType) -> str:
        return self._call(prompts)

    def _format_prompt(self, prompts: PromptType) -> str:
        if isinstance(prompts, str):
            return prompts
        elif isinstance(prompts, list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts, dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid prompt type")


#2.Gemini
class Gemini(LLM):
    driver: Optional[uc.Chrome] = None 
    @property
    def _llm_type(self) -> str:
        return "gemini_ai_web_llm"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--no-first-run")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(
            options=options,
            headless=False,
            version_main=get_chrome_major_version()
            )
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        })
        self.driver.get("https://gemini.google.com/app")
        self.driver.maximize_window()
        time.sleep(5)

    def _call(self, prompts: PromptType, stop: Optional[List[str]] = None) -> str:
        text_prompt = self._format_prompt(prompts)
        try:
            prompt_box = self.driver.find_element(
                By.XPATH,
                "/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/"
                "bard-sidenav-content/div[2]/div/div[2]/chat-window/div/input-container/"
                "div/input-area-v2/div/div/div[2]/div/div/rich-textarea/div[1]"
            )
            prompt_box.clear()
            prompt_box.send_keys(text_prompt)
            prompt_box.send_keys(Keys.RETURN)

            time.sleep(20)
            responses = self.driver.find_elements(By.XPATH, "//model-response//response-container//div/div[2]/div[2]")
            if responses:
                return responses[-1].text.strip()
            return "Invalid input."

        except Exception as e:
            return f"[Error in Gemini: {str(e)}]"

    def invoke(self, prompts: PromptType) -> str:
        return self._call(prompts)

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _format_prompt(self, prompts: PromptType) -> str:
        if isinstance(prompts, str):
            return prompts
        elif isinstance(prompts, list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts, dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid prompt type")


#3.ChatGPT
class ChatGPT(LLM):
    driver: Optional[uc.Chrome] = None
    @property
    def _llm_type(self) -> str:
        return "chatgpt_web_llm"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--no-first-run")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(
            options=options,
            headless=False,
            version_main=get_chrome_major_version()
            )
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        })
        self.driver.get("https://chatgpt.com/")
        self.driver.maximize_window()
        time.sleep(7)

    def _call(self, prompts: PromptType, stop: Optional[List[str]] = None) -> str:
        text_prompt = self._format_prompt(prompts)
        try:
            try:
                cookies = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/button[3]")
                cookies.click()
                time.sleep(2)
            except:
                pass

            prompt_box = self.driver.find_element(By.XPATH,
                "/html/body/div[1]/div[1]/div/div/main/div/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/div[1]/div/div")
            time.sleep(2)
            prompt_box.clear()
            prompt_box.send_keys(text_prompt)
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
                return response[-1].text.strip()
            return "Invalid input."

        except Exception as e:
            return f"[Error in ChatGPT: {str(e)}]"

    def invoke(self, prompts: PromptType) -> str:
        return self._call(prompts)

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _format_prompt(self, prompts: PromptType) -> str:
        if isinstance(prompts, str):
            return prompts
        elif isinstance(prompts, list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts, dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid prompt type")


#4.Grok
class Grok(LLM):
    @property
    def _llm_type(self) -> str:
        return "grok_web_llm"

    def _call(self, prompts: PromptType, stop: Optional[List[str]] = None) -> str:
        text_prompt = self._format_prompt(prompts)
        driver: Optional[uc.Chrome] = None
        try:
            options = uc.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--no-first-run")
            options.add_argument("--no-service-autorun")
            options.add_argument("--password-store=basic")
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = uc.Chrome(
                options=options,
                headless=False,
                version_main=get_chrome_major_version()
                )
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })
            url="https://grok.com"
            driver.get(url)
            driver.maximize_window()
            time.sleep(10)

            adbtncut = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/main/div[2]/div/div[2]/div[1]/div[2]/div/button")
            time.sleep(1)
            adbtncut.click()
            time.sleep(4)

            prompt = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/main/div[2]/div/div[2]/div[1]/div[1]/form/div/div/div[2]/div[1]/textarea")
            time.sleep(2)
            prompt.send_keys(text_prompt)
            time.sleep(1.6)
            prompt.send_keys(Keys.RETURN)
            time.sleep(30)

            result = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/main/div[2]/div[2]/div/div[2]/div[2]/div/div[1]")
            return result.text

        except Exception as e:
            return f"[Error in Grok: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def invoke(self, prompts: PromptType) -> str:
        return self._call(prompts)

    def _format_prompt(self, prompts: PromptType) -> str:
        if isinstance(prompts, str):
            return prompts
        elif isinstance(prompts, list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts, dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid prompt type")


#5.Perplexity
class Perplexity(LLM):
    @property
    def _llm_type(self) -> str:
        return "perplexity_llm"

    def _call(self, prompts: PromptType, stop: Optional[List[str]] = None) -> str:
        text_prompt = self._format_prompt(prompts)
        driver: Optional[uc.Chrome] = None
        try:
            options = uc.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--no-first-run")
            options.add_argument("--no-service-autorun")
            options.add_argument("--password-store=basic")
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = uc.Chrome(
                options=options,
                headless=False,
                version_main=get_chrome_major_version()
                )
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })
            wait = WebDriverWait(driver, 30)

            url="https://www.perplexity.ai/"
            driver.get(url)
            time.sleep(1)
            driver.maximize_window()

            prompt = driver.find_element(By.XPATH,"/html/body/main/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/div/span/div/div[1]/div/div[1]/div/div")
            prompt.send_keys(text_prompt)
            time.sleep(0.5)
            prompt.send_keys(Keys.RETURN)
            time.sleep(30)

            result = driver.find_element(By.XPATH,"//*[@id='markdown-content-0']/div")
            time.sleep(3)                          #/html/body/main/div[1]/div/div/div[2]/div/div[1]/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div                  
            return result.text

        except Exception as e:
            return f"[Error in Perplexity: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def invoke(self, prompts: PromptType) -> str:
        return self._call(prompts)

    def _format_prompt(self, prompts: PromptType) -> str:
        if isinstance(prompts, str):
            return prompts
        elif isinstance(prompts, list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts, dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid prompt type")
#6 Image
class Image(LLM):
    @property
    def _llm_type(self)-> str:
        return "image generation model"
    def _call(self,prompts:PromptType,stop:Optional[List[str]]=None)->str:
        text_prompt=self._format_prompt(prompts)
        driver:Optional[uc.Chrome]=None
        try:
            options=uc.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--no-first-run")
            options.add_argument("--no-service-autorun")
            options.add_argument("--password-store=basic")
            options.add_argument("--disable_blink-features=AutomationControlled")

            driver=uc.Chrome(
                options=options,
                headless=False,
                version_main=get_chrome_major_version()
                )
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
                "source":"Object.defineProperty(navigator,'webdriver',{get:() => undefined })"
                })
            wait=WebDriverWait(driver,30)

            url="https://deepai.org/machine-learning-model/text2img"
            driver.get(url)
            time.sleep(1)
            driver.maximize_window()

            prompt=driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[1]/span/div[2]/textarea[1]")
            prompt.send_keys(text_prompt)
            prompt.send_keys(Keys.RETURN)
            time.sleep(12)

            image_response=driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[3]/div[1]/button[1]")
            image_response.click()
            time.sleep(6)
            return "Image Generated Successfully"
        except:
            return f"[Error in Image:{str(e)}]"

    def invoke(self,prompts:PromptType)-> str:
        return self._call(prompts)

    def _format_prompt(self, prompts:PromptType) -> str:
        if isinstance(prompts,str):
            return prompts
        elif isinstance(prompts,list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts,dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid Prompt Type")

# 7 Mistral
class Mistral(LLM):
    @property
    def _llm_type(self) -> str:
        return "mistral_llm"

    def _call(self, prompts: PromptType, stop: Optional[List[str]] = None) -> str:
        text_prompt = self._format_prompt(prompts)
        driver: Optional[uc.Chrome] = None
        try:
            options = uc.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--no-first-run")
            options.add_argument("--no-service-autorun")
            options.add_argument("--password-store=basic")
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = uc.Chrome(
                options=options,
                headless=False,
                version_main=get_chrome_major_version()
                )
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })
            wait = WebDriverWait(driver, 30)

            url="https://chat.mistral.ai/chat"
            driver.get(url)
            time.sleep(1)
            driver.maximize_window()

            tos=driver.find_element(By.XPATH,"/html/body/div[3]/button")
            tos.click()
            time.sleep(1)
            
            promptbox=driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/main/div/div/div[2]/div/div[2]/div/form/div/div/div[1]/div/div/div/div/div")
            promptbox.send_keys(prompts)
            time.sleep(0.5)
            promptbox.send_keys(Keys.RETURN)
            time.sleep(10)
            
            result=driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/main/div/div/div[2]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div")
            return result.text

        except Exception as e:
            return f"[Error in Mistral: {str(e)}]"
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def invoke(self, prompts: PromptType) -> str:
        return self._call(prompts)

    def _format_prompt(self, prompts: PromptType) -> str:
        if isinstance(prompts, str):
            return prompts
        elif isinstance(prompts, list):
            return "\n".join(str(p) for p in prompts)
        elif isinstance(prompts, dict):
            return json.dumps(prompts)
        else:
            raise ValueError("Invalid prompt type")

        
# Call Code
if __name__ == "__main__":
    models = {"1": GeminiAIMode, "2": Gemini, "3": ChatGPT, "4":Grok, "5":Perplexity}
    choice = input("Choose model 1:-GeminiAIMode,2:-Gemini, 3:-ChatGPT, 4:-Grok, 5:-Perplexity 6:-Image, 7:-Mistral").strip()
    prompts = input("Enter query: ").strip()
    Selected = models.get(choice, Gemini)
    llm = Selected()
    response = llm.invoke(prompts)
    print(response)
