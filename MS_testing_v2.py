# creation flow amazon example
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
import random
import argparse
import json
import yaml
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from delete_act_DB_firebase import delete_firebase_user_by_email, delete_mongo_user
from sys import platform
import pyautogui


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")  # Run headless Chrome (no GUI)
options.add_argument("--disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--guest")
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
# Setup ChromeDriver
if platform == "darwin":
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),  # type: ignore
        options=options,
        )
else:
    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)



main_window_handle = driver.current_window_handle
n = str(random.randint(1, 100))


def network_logs():
    logs = driver.get_log('performance')
    error_logs = []
    for log in logs:
        log_message = json.loads(log['message'])['message']
        if 'Network.responseReceived' in log_message['method']:
            response = log_message['params']['response']
            status = response.get('status')
            if status >= 400:  # Check for client and server errors
                error_logs.append(log_message)
        
        # Print out the error network logs for inspection
    for log in error_logs:
        print(json.dumps(log, indent=2))


def xpath_click(str1, time1):    #waiting_for_element
    try:
        element = WebDriverWait(driver, time1).until(EC.visibility_of_element_located((By.XPATH, str1)))
        element.click()
    except:
        # print(f"Error: Element with XPath '{str1}' not found within the timeout period.")
        network_logs()

def xpath_send(str1, time1, value):    #waiting_for_element
    try:
        element = WebDriverWait(driver, time1).until(EC.visibility_of_element_located((By.XPATH, str1)))
        element.clear()
        element.send_keys(value)
    except:
        # print(f"Error: Element with XPath '{str1}' not found within the timeout period.")
        network_logs()

def id_click(str1, time1):     #waiting_for_element_id
    try:
        element = WebDriverWait(driver, time1).until(EC.visibility_of_element_located((By.ID, str1)))
        element.click()
    except:
        # print(f"Error: Element with ID '{str1}' not found within the timeout period.")
        network_logs()

def id_send(str1, time1, value):     #waiting_for_element_id
    try:
        element = WebDriverWait(driver, time1).until(EC.visibility_of_element_located((By.ID, str1)))
        element.clear()
        element.send_keys(value)
    except:
        # print(f"Error: Element with ID '{str1}' not found within the timeout period.")
        network_logs()

def id_send_js(str1, time1, value):
    try:
        element = WebDriverWait(driver, time1).until(EC.visibility_of_element_located((By.ID, str1)))
        element.clear()
        element.click()
        driver.execute_script(f"arguments[0].value = '{value}';", element)
    except Exception as e:
        print(f"Error: Element with ID '{str1}' not found or interactable. {e}")

def get_org_id():
    try:
       id_click('side-nav-shortcut-organization', 200)
       ele= WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, 'organization-id')))
       org = ele.get_attribute("value")
       print("Org id: ", org)
       return org
    except:
        return "0"


def assistedshopping_parameter():
    try:
        ele= WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.ID, "capability-card-2")))
        edit1=ele.find_element(By.ID, "capability-edit-icon")
        edit1.click()
        #adding group
        id_click("add-new-group-btn", 20)
        id_send("new-group-name-inputbox", 20, "shopping")
        id_click("add-group-btn", 20)
        #Remove example utterance
        example_utterance = driver.find_element(By.ID, "capability-example-utterances")
        exp_close_btn = example_utterance.find_elements(By.CLASS_NAME, "lucide lucide-circle-x fill-current stroke-primary-200")
        for i in exp_close_btn:
            i.click()
        time.sleep(5)
        #Add example utterance
        id_send("properties-example-utterance-inputbox", 20, "2 black nike shoes for men size 10 below 1500 rupees, Add 5 KG India Gate basmati rice to the cart, Suggest an AC for 15 by 15 room,")
        #edit parameter
        id_click("parameters", 20)  #parameters tab
        id_click("parameter-0-trash-btn", 20)
        xpath_click("/html/body/div[9]/div/button[2]", 20)  #proceed btn to delete parameter
        id_click('add-parameter-plus-btn', 20)
        id_send('parameter-0-name', 20, "search_term")
        id_click('parameter-0-datatype', 20)
        id_click('parameter-0-string', 20)
        id_send('parameter-0-description', 20, "The main product name to search for.")
        id_click("parameter-0-required-checkbox", 20)
        #save and close
        id_click("save-btn", 20)
    except:
        print("Unable to add group")
        

def recipe_flow_paremeter():
    try:
        ele= WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "capability-card-3")))
        edit1=ele.find_element(By.ID, "capability-edit-icon")
        edit1.click()
        #adding group
        id_click("add-new-group-btn", 20)
        id_send("new-group-name-inputbox", 20, "shopping")
        id_click("add-group-btn", 20)
        #save and close
        id_click("save-btn", 20)
    except:
        print("Unable to recipe capability")


def domain_faq_paremeter():
    try:
        #click edit btn
        domain_cap_card = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "capability-card-3")))
        edit_domain = domain_cap_card.find_element(By.ID, "capability-edit-icon")
        edit_domain.click()
        #adding group
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "multi-select-down-arrow")))
        id_click("multi-select-down-arrow", 30)
        id_send("select-group-inputbox", 35, "shopping")
        x=driver.find_element(By.ID, "select-group-inputbox")
        x.send_keys(Keys.RETURN)
        id_send("properties-example-utterance-inputbox", 35, "What are the health benefits of drinking milk, Compare top load washing machine and front load washing machine,")
        id_send("properties-tool-topics-inputbox", 20, "Health benefits, Compare products,")
        #enable global internet search
        id_click("knowledge", 20) # click on knowledge tab
        id_click("global-internet-search-checkbox", 20)
        id_click("save-btn", 20)
    except:
        print("Unable to edit domain faq capability")
           

def add_custom_capability(str1):
    try:
        id_click('create-new-capability-card', 100)   # Add capability
        id_click("create-capability-tab", 20) #custom capability button
        try:
            ele = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID, "monaco-editor")))
            # monaco editor input
            try:
                element = ele.find_element(By.TAG_NAME, "textarea")
                element.clear()
                element.send_keys(str1)
                id_click("monaco-editor-create-btn", 20)
                time.sleep(5)
                WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.ID, "create-new-capability-card")))
                return 1
            except Exception as e:
                print(f"Error: Element with ID '{element}' not found or interactable. {e}")
                return 0
        except:
            print("unable to edit")
            return 0
    except:
        return 0

def login_cred(user, password):
    try:
        id_send("email-input", 20, user)
        id_send("password-input", 5, password)
        id_click("auth-submit-btn", 5)
        return 1
    except:
        network_logs()
        return 0

def register_user(user, password):
    try:
        id_send("email-input", 30, user)
        id_send("password-input", 5, password)
        id_send("confirm-password-input", 5, password)
        id_click("auth-submit-btn", 5)
        return 1
    except:
        return 0


def log_out():
    try:
        WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.ID, "profile-btn")))
        id_click("profile-btn", 15)
        id_click("logout-btn", 15)
        return 1
    except:
        return 0
    
def google_register(user, password):
    try:
        xpath_send("/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input", 35, user)      #sign in with gmail account - email
        xpath_click("/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/span", 10)
        time.sleep(5)
        xpath_send('/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input', 35, password)      #sign in with gmail account - password
        xpath_click("/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/span", 10)
    except:
        print("Unable to Register with google login")

def switch_window(wind:str, main_window_handle:str):
    if wind == "new":
        try:
            WebDriverWait(driver, 30).until(EC.new_window_is_opened(driver.window_handles))
            window_handles = driver.window_handles
            new_window_handle = None
            for handle in window_handles:
                if handle != main_window_handle:  # Find new window handle
                    new_window_handle = handle
                    break

            if new_window_handle:
                driver.switch_to.window(new_window_handle)
                time.sleep(2)  # Small delay to allow window switch to complete
            else:
                raise Exception("New window handle not found.")
        except Exception as e:
            print(f"Error switching to new window: {e}")
            network_logs()
            return

    elif wind == "main":
        try:
            if driver.current_window_handle != main_window_handle:
                driver.close()  # Close the new window
            driver.switch_to.window(main_window_handle)
            time.sleep(2)  # Small delay to allow window switch to complete
        except Exception as e:
            print(f"Error switching to the main window: {e}")
            network_logs()
            return

def pg_textbox_test(t:str):
    id_send('playground-input', 20, t)
    id_click('playground-send-btn', 5) #enter button
    time.sleep(7)
    try:
        ele = driver.find_element(By.XPATH, "//div[@class='relative']//pre/code")
        sspan = ele.find_elements(By.CSS_SELECTOR, 'span.token')
        for x in sspan:
            print(x.text, end = "")
    except:
        network_logs()

    
def add_knowledge_app_faq():
    try:
        domain_cap_card = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, "capability-card-4")))
        edit_domain = domain_cap_card.find_element(By.ID, "capability-edit-icon")
        edit_domain.click()
        # adding description for answering from pdf
        description_value = "Provides answers to frequently asked questions about MK Retail. Answer any questions related to retail stores"
        id_send('capability-goal', 30, description_value)
        #adding group
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, "multi-select-down-arrow")))
        id_click("multi-select-down-arrow", 20)
        id_send("select-group-inputbox", 20, "shopping")
        x=driver.find_element(By.ID, "select-group-inputbox")
        x.send_keys(Keys.RETURN)
        print(f"Test case 14: Adding group - Pass")
    except:
        print(f"Test case 14: Adding group - Fail")
    
    #add knowledge
    try:
        id_click("knowledge", 20) #click on knowledge tab
        id_click("create-knowledge-btn", 20)  # create knowledge
        #html url for home page
        id_send("knowledge-name", 20, "MK Retail return and refund policy") #knowlwdge name
        id_send("knowledge-description", 10, "link for MK Retail return and refund policies") #knowledge description
        id_click("html-upload-btn", 20)
        id_click("add-new-url-btn", 20)
        id_send("add-1-url-textbox", 20, "https://www.termsfeed.com/blog/sample-return-policy-ecommerce-stores/")
        enter1 = driver.find_element(By.ID, "add-1-url-textbox")
        enter1.send_keys(Keys.RETURN)
        id_click("add-multiple-url-btn", 20)
        id_send("add-multiple-url-inputbox", 30, "https://www.shopify.com/tools/policy-generator/refund\nhttps://www.websitepolicies.com/blog/sample-return-refund-policy-template")
        id_click("add-url-btn", 20)
        time.sleep(10)
        id_click("web-knowledge-save-btn", 100)
        id_click("create-data-group-btn", 40)
        time.sleep(15)
        print(f"Test case 15: Adding HTML knowledge single and multiple links - Pass")
    except:
        print(f"Test case 15: Adding HTML knowledge single and multiple links - Fail")

    try:
        #add - remove and add csv knowledge
        # main_window_handle = driver.current_window_handle
        id_click("attach-knowledge-btn", 20)
        id_click("create-knowledge-from-attach", 20)
        id_send("knowledge-name", 20, "MK Retail category") #knowlwdge name
        id_send("knowledge-description", 10, "List of retail categories") #knowledge description
        id_click("structured-knowledge-upload-btn", 20)
        #add and remove a csv file
        id_click("structured-file-dropzone", 20)
        pyautogui.hotkey('command', 'tab')
        # switch_window("new", main_window_handle)
        time.sleep(2)
        pyautogui.hotkey('command', 'shift','g') 
        time.sleep(3)
        pyautogui.write("/Users/divyac/Documents/Required_files/Mylo_golden_dataset.csv", interval=0.1)  # Type the file path
        pyautogui.press('return')
        time.sleep(2)
        pyautogui.press('return')
        id_click("structured-knowledge-trash", 20)
        print(f"Test case 16: Deleting a knowledge - Pass")
        #add one more csv knowledge
        id_click("structured-file-dropzone", 20)
        pyautogui.hotkey('command', 'tab')
        pyautogui.hotkey('command', 'tab')
        # switch_window("new", main_window_handle)
        time.sleep(2)
        pyautogui.hotkey('command', 'shift','g') 
        time.sleep(3)
        pyautogui.write("/Users/divyac/Documents/Required_files/Amazon category.csv", interval=0.1)  # Type the file path
        pyautogui.press('return')
        time.sleep(2)
        pyautogui.press('return')
        id_click("csv-row-advance-setting-icon", 30)
        id_click("multi-select-down-arrow", 20)
        id_send("multiselect-inputbox", 30, "Mai category")
        pyautogui.press('enter')
        pyautogui.press('return')
        time.sleep(5)
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "structured-knowledge-save-btn")))
        id_click("structured-knowledge-save-btn", 20)
        id_click("create-data-group-btn", 20)
        time.sleep(15)
        print(f"Test case 17: Adding csv knowledge - Pass")
    except:
        print(f"Test case 17: Adding csv knowledge - Fail")

    try:
        #add pdf knowledge
        id_click("attach-knowledge-btn", 100)
        id_click("create-knowledge-from-attach", 20)
        id_send("knowledge-name", 20, "All about retail stores") #knowlwdge name
        id_send("knowledge-description", 10, "PDF value") #knowledge description
        id_click("unstructured-knowledge-upload-btn", 20)
        #add and remove a pdf file
        id_click("unstructured-file-dropzone", 20)
        pyautogui.hotkey('command', 'tab')
        # switch_window("new", main_window_handle)
        time.sleep(2)
        pyautogui.hotkey('command', 'shift','g') 
        time.sleep(3)
        pyautogui.write("/Users/divyac/Documents/Required_files/Retail_store.pdf", interval=0.2)  # Type the file path
        pyautogui.press('return')
        time.sleep(2)
        pyautogui.press('return')
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "unstructured-knowledge-save-btn")))
        id_click("unstructured-knowledge-save-btn", 20)
        id_click("create-data-group-btn", 20)
        time.sleep(15)
        print(f"Test case 18: Adding pdf knowledge - Pass")
    except:
       print(f"Test case 18: Adding pdf knowledge - Fail")   

    try:
        #add text knowledge
        id_click("attach-knowledge-btn", 100)
        id_click("create-knowledge-from-attach", 20)
        id_send("knowledge-name", 20, "MK Retail address") #knowlwdge name
        id_send("knowledge-description", 10, "Text value") #knowledge description
        id_click("text-knowledge-upload-btn", 20)
        try:
            ele = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID, "monaco-editor")))
            # monaco editor input
            try:
                element = ele.find_element(By.TAG_NAME, "textarea")
                element.clear()
                element.send_keys("Contact person: MK Reatil cutomer support team, Address: 734, Bangalore, Karnataka, Phone number: 080-41261555")
            except Exception as e:
                print(f"Error: Element with ID '{element}' not found or interactable. {e}")
        except:
            print("unable to edit monaco editor")
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "text-knowledge-save-btn")))
        id_click("text-knowledge-save-btn", 20)
        id_click("create-data-group-btn", 20)
        time.sleep(15)
        print(f"Test case 19: Adding text knowledge - Pass")
    except:
        print(f"Test case 19: Adding text knowledge - Fail")
    try:
        id_click("save-btn", 20)
    except:
        print("Unable to add knowledge")


def load_config(env):
    try:
        with open('../polyglot/tools/testing/Automation/Magic_Studio_console/ms_config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        if env in config['configurations']:
            env_config = config['configurations'][env]
            return env_config
        else:
            raise ValueError("Invalid environment specified")
    except Exception as e:
        print("didnt find file", e)

def assistant_create_url_manual(a):
    if(a == 1):
        b = 0
        try:
            id_click("create-new-assistant-card", 20)    #clicking create assistant btn
            id_send("project_url_inputbox", 20, "https://play.google.com/store/apps/details?id=com.innobits.enstore.mkretail&hl=en-IN")
            id_click("manual-create-btn", 20)
            WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "next-add-capabilities")))
            id_send("app_name", 40, "Automated_mkretail")
            description_value = "MK Retail is a comprehensive shopping app, making it a one-stop solution for all your shopping needs. It provides information about the products, answer any question related to retail stores, compare the products, give health benefits of products, recommend products. Users can find a variety of products ranging from fresh fruits and vegetables to packaged goods, beverages, and household items. The app emphasizes superfast delivery, ensuring that customers receive their orders promptly. With its extensive catalog, MK Retail caters to diverse shopping preferences, making it easy for users to discover and purchase their desired items."
            id_send_js('project-description', 30, description_value)
            #change the app category
            category_value = "grocery, fashion, home, beauty, electronics, Alexa Devices, sporting goods, toys, automotive, pets, baby, books, video games, musical instruments, office supplies, house hold, fitness, personal care, pharmacy, furniture, gift,  fitness, mother and baby care, retail stores, health benefits,"
            id_send("project-category-inputbox", 30, category_value)
            try:
                id_click("next-add-capabilities", 10)
                print(f"Test case 10: App grokker works - Pass")
                b = 1
            except:
                print(f"Test case 10: App grokker doesn't work - Fail")
        except:
            print(f"Unable to get response from grokking / edit the grokker form")
        
            
        # Adding Capability
        # Add custom capability for Assisted Shopping
        if(b==1):
            c = 0
            try:
                replace_string = """Enhance the user's shopping experience through an "assisted_shopping" capability to find products quickly and accurately for {MK Retail app}. 
Message: You MUST provide an appropriate response that includes "message".
Search Term: Identify the search term from the input query. The search term must be a product name with or without the brand name. It MUST NOT include conjunctions.Shopping List: If the user gives more than one product in the input query, treat it as a shopping list. Add the first product to the search term. Add the remaining products to "related_products". Do NOT add this shopping list to the cart until the user wants you to add to cart.
Related Products: You MUST Provide 4 to 6 products related to the search term as "related_products". Do NOT list these products as product 1, product 2, etc. They all must be valid product names.
Brand Name: Identify the brand name only if the user is looking for a particular brand.
Cart Value: Depending on whether the user wants to add the product to the cart or not, the cart value must be 0 or 1.
Quantity and Measurement: If the user gives the quantity and measurement unit, store it in respective parameters.
Recommendations: If the user asks for recommendations or suggestions like gift ideas, suggest some products that align with the input query, and the search term must be a product.
Filters: Enhance the user's search by using an object of dictionary. Filters such as gender, age, size, color, price, and rating is used to narrow down the search.
Category Adherence: You MUST not answer any questions that do not adhere to the app category.
    """
                flag1 = add_custom_capability(replace_string)
                if(flag1==1):
                    assistedshopping_parameter()
                    print(f"Test case 11: Adding custom capability and editing parameters - Pass")
                    c = 1
            except:
                print(f"Test case 11: Unable to add custom capability and edit parameters - Fail")
                
            
        # Adding capability from store
        if(b==1):
            try:
                # Add capability from store for domain FAQ
                time.sleep(2)
                id_click("create-new-capability-card", 300)
                domain_card = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, "outline-card-0")))
                import_domain = domain_card.find_element(By.ID, "capability-outline-card-small-import")
                import_domain.click()
                domain_faq_paremeter()
                c=1
                print(f"Test case 12: Adding capability from store, editing description, enabling gloabl internet search - Pass")
            except:
                print("Unable to add domain faq")
                print(f"Test case 12: Adding capability from store, editing description, enabling gloabl internet search - Fail")
                
            try:
                # Add capability from store for App FAQ
                id_click("create-new-capability-card", 50)
                domain_card = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, "outline-card-1")))
                import_domain = domain_card.find_element(By.ID, "capability-outline-card-small-import")
                import_domain.click()
                c=1
                print(f"Test case 13: Adding capability from store, adding all types of knowledges, enabling internet search - Pass")
                add_knowledge_app_faq()
            except:
                print("Unable to add app faq")
                print(f"Test case 13: Adding capability from store, adding all types of knowledges, enabling internet search - Fail")
            

        #Building Assistant
        if((b==1) or (c==1)):
            try:
                id_click("next-build-assistant-btn", 1500)
                try:
                    WebDriverWait(driver, 10000).until(EC.element_to_be_clickable((By.ID, "try-assistant-btn")))
                    id_click("try-assistant-btn", 10)
                    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, "chat-window-suggestion-0")))
                    print(f"Test case 20:  compiling, setting up and configuring - Pass")
                    return 1
                except:
                    print(f"Test case 20: Unable to compiling, setting up and configuring - Fail")
                    return 0
            except:
                print("Unable to build an assistant")
                return 0
            
def pg_fetch_first_expanded_response():
    try:
        element = WebDriverWait(driver, 3500).until(EC.visibility_of_element_located((By.ID, "assistant-message")))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        id_click("assistant-expand-icon", 2000) # click on expand json
        time.sleep(1)
        try:
            WebDriverWait(driver, 500).until(EC.visibility_of_element_located((By.ID, "pg-response-code")))
            resp_div = driver.find_element(By.ID, "pg-response-code")
            try:
                pre_res = resp_div.find_element(By.CLASS_NAME, "text-xs")
                try:
                    pre1 = pre_res.find_element(By.TAG_NAME, 'pre') 
                    try:
                        code=pre1.find_element(By.TAG_NAME, 'code')
                        sspan = code.find_elements(By.CLASS_NAME, 'line')
                    except:
                        try:
                            code=driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/main/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div/span/pre/code")
                            sspan = code.find_elements(By.CLASS_NAME, 'line')
                        except:
                            sspan = driver.find_elements(By.CLASS_NAME, 'line')
                    for x in sspan:
                        span = x.find_elements(By.TAG_NAME, 'span')
                        for y in span:
                            print(y.text, end = "")
                    print()
                    return 1
                except Exception as e:
                    print("Unable to get code ", e)
            except:
                print("Unable to get pre")
        except:
            print("Unable to get pg-response-code")
            return 1
    except:
        return 0
    
def pg_fetch_first_response():
    try:
        element = WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.ID, "assistant-message")))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        msg = driver.find_element(By.ID, "assistant-message")
        print("Response message", msg.text)
        try:
            id_click("assistant-response-parameter-arrow", 2) # click on expand json
            time.sleep(1)
            resp_parameter = driver.find_element(By.ID, "assistant-response-parameter")
            pre1 = resp_parameter.find_element(By.TAG_NAME, 'pre') 
            try:
                code=pre1.find_element(By.TAG_NAME, "code")
            except:
                code=driver.find_element(By.CSS_SELECTOR, "#pg-response-code > div > span > pre > code")
            sspan = code.find_elements(By.CLASS_NAME, 'line')
            for x in sspan:
                span = x.find_elements(By.TAG_NAME, 'span')
                for y in span:
                    print(y.text, end = "")
            print()
            return 1
        except:
            print("Response hightlight was not available")
            return 1
    except:
        return 0


def pg_fetch_second_response():
    try:
        time.sleep(2)
        pg_msg_3 = WebDriverWait(driver, 2500).until(EC.presence_of_element_located((By.ID, "pg-msg-3")))
        msg = pg_msg_3.find_element(By.ID, "assistant-message")
        print("Response message", msg.text)
        try:
            arr = pg_msg_3.find_element(By.ID, "assistant-response-parameter-arrow")
            arr.click()
            time.sleep(1)
            resp_parameter = pg_msg_3.find_element(By.ID, "assistant-response-parameter")
            pre1 = resp_parameter.find_element(By.TAG_NAME, 'pre') 
            code=pre1.find_element(By.TAG_NAME, "code")
            sspan = code.find_elements(By.CLASS_NAME, 'line')
            for x in sspan:
                span = x.find_elements(By.TAG_NAME, 'span')
                for y in span:
                    print(y.text, end = "")
            print()
            return 1
        except:
            print("Response hightlight was not available")
            return 0
    except:
        return 0

    
def test_assistant_retail():
    e=0
    # Open PG app
    try:
        id_click('side-nav-shortcut-playground', 1500) #Click on playgroup tab
        e=1
    except:
        print("Unable to open playground")

    # First hint is clicked
    if(e==1):
        flag=0
        try:
            WebDriverWait(driver, 150).until(EC.presence_of_element_located((By.ID, "chat-window-suggestion-0")))
            sug = driver.find_element(By.ID, "chat-window-suggestion-0")
            par = sug.find_element(By.TAG_NAME, "p")
            print("Query : ", par.text)
            id_click('chat-window-suggestion-0', 30) # click on first hint
            flag = pg_fetch_first_expanded_response()
            if(flag==1):
                print(f"Test case 15: Playground Testing - First hint - Pass")
                for i in range(0, 2):
                    print("")
            else:
                print(f"Test case 15: Playground Testing - First hint - Fail")
        except:
            print("Unable to test first hint")

    # input box testing
    if(e==1):
        flag=0
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'add 2 black adidas t-shirts for women to the cart')
            print("Query : add 2 black adidas t-shirts for women to the cart")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_response()
            if(flag==1):
                print(f"Test case 16: Playground Testing - Text input infer works- Pass")
                for i in range(0, 2):
                    print("")
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 16: Playground Testing - Text input infer doesn't work - Fail")

        # input box
        if(flag==1):
            try:
                id_send('pg-inputbox', 100, 'size M')
                print("Query : size M")
                id_click("pg-inputbox-send-button", 20)
                flag = pg_fetch_second_response()
                if(flag==1):
                    print(f"Test case 17: Playground Testing - conversation infer works- Pass")
                    for i in range(0, 2):
                        print("")
                else:
                    print("Unable to fetch the output")
            except:
                print(f"Test case 17: Playground Testing - conversation infer doesn't work - Fail")


     # query realted to html knowledge
    if(e==1):  
        flag=0    
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'what is the return and refund policy')
            print("Query : what is the return and refund policy")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_response()
            if(flag==1):
                print(f"Test case 19: Playground Testing - html knowledge- Pass")
                for i in range(0, 2):
                    print("")
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 19: Playground Testing - html knowledge- Fail")

    # query realted to csv knowledge
    if(e==1):  
        flag=0    
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'what is the Subcategory 1 of Books?')
            print("Query : what is the Subcategory 1 of Books?")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_response()
            if(flag==1):
                print(f"Test case 20: Playground Testing - csv knowledge- Pass")
                for i in range(0, 2):
                    print("")
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 20: Playground Testing - csv knowledge- Fail")

    # query realted to pdf knowledge
    if(e==1):  
        flag=0    
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'What are the different types of retail stores?')
            print("Query :What are the different types of retail stores?")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_response()
            if(flag==1):
                print(f"Test case 20: Playground Testing - pdf knowledge- Pass")
                for i in range(0, 2):
                    print("")
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 20: Playground Testing - pdf knowledge- Fail")

    # query realted to text knowledge
    if(e==1):      
        flag=0
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'what is the contact detail')
            print("Query : what is the contact detail")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_response()
            if(flag==1):
                print(f"Test case 21: Playground Testing - text knowledge- Pass")
                for i in range(0, 2):
                    print("")
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 21: Playground Testing - text knowledge- Fail")


    # selecting capability with gloabl internet search enabled
    if(e==1):
        flag=0
        try:
            id_click("pg-new-thread-btn", 20)
            id_click("pg-cap-select", 20)   # capability optionselection btn
            id_click("pg-cap-select-0", 20)     #select domain faq
            id_send('pg-inputbox', 20, 'What is the benefit of eating ginger')
            print("Query : What is the benefit of eating ginger")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_response()
            if(flag==1):
                print(f"Test case 18: Playground Testing - capability selection query- Pass")
                for i in range(0, 2):
                    print("")
                return 1
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 18: Playground Testing - capability selection query- Fail")
    return 0


def check_assistant_details():
    try:
        id_click("side-nav-shortcut-integration", 20)
        WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "assistant-id")))
        ele = driver.find_element(By.ID, 'assistant-id')
        print("Asistid: ", ele.get_attribute("value"))
        ele = driver.find_element(By.ID, 'api-key')
        print("API Key: ", ele.get_attribute("value"))
        ele = driver.find_element(By.ID, 'assistant-version')
        print("Version: ", ele.get_attribute("value"))
        return 1
    except: 
        print("Unable to fetch the assistant details")
        return 0

def one_click_assistant():
    try:
        id_click("side-nav-shortcut-home", 20)
        if((WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "create-new-assistant-card")))).is_displayed()):
            try:
                id_click("create-new-assistant-card", 20)    #clicking create assistant btn
                id_send("project_url_inputbox", 20, "goindigo.com")
                id_click("1-click-btn", 20)
                try:
                    WebDriverWait(driver, 15000).until(EC.element_to_be_clickable((By.ID, "try-assistant-btn")))
                    id_click("try-assistant-btn", 10)
                    driver.implicitly_wait(2.5)
                    if(WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.ID, "chat-window"))).is_displayed()):
                        print(f"Test case 30: 1-click assistant created - Pass")
                        a = check_assistant_details()
                        if(a==1):
                            print(f"Test case 31: 1-click Integration page works - Pass")
                        else:
                            print(f"Test case 31: 1-click Integration page doesn't works - Fail")
                except:
                    print(f"Test case 30: 1-click assistant not created  - Fail")
            except:
                print(f"Unable to get response from auto grokking ")
    except:
        print("Unable to click on home page")


    # Playground testing
    if(a==1):
        b=0
        try:
            id_click("side-nav-shortcut-playground", 20) #Click on playgroup tab
            WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.ID, "chat-window-suggestion-0")))
            b=1
        except:
            print("Unable to open playground")

    # First hint is clicked
    if(b==1):
        try:
            sug = driver.find_element(By.ID, "chat-window-suggestion-0")
            par = sug.find_element(By.TAG_NAME, "p")
            print("Query : ", par.text)
            id_click('chat-window-suggestion-0', 30) # click on first hint
            c = pg_fetch_first_response()
            if(c==1):
                print(f"Test case 24: Playground Testing - First hint - Pass")
                for i in range(0, 2):
                    print("")
            else:
                print(f"Test case 24: Playground Testing - First hint - Fail")
        except:
            print(f"First hint could not be clicked")
            network_logs()

    # input box testing
    if(b==1):
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'I want to book flights from bangalore to delhi for tomorrow for 3 passengers')
            print("Query : I want to book flights from bangalore to delhi for tomorrow for 3 passengers")
            id_click("pg-inputbox-send-button", 20)
            flag = pg_fetch_first_expanded_response()
            if(flag==1):
                print(f"Test case 25: Playground Testing - Text input infer works- Pass")
                for i in range(0, 2):
                    print("")
                return 1
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 25: Playground Testing - Text input infer doesn't work - Fail")
    return 0

def draft_manual_assistant_without_url():
    try:
        a=0
        id_click("side-nav-shortcut-home", 30)
        id_click("create-new-assistant-card", 35)    #clicking create assistant btn
        id_click("no-url-checkbox", 20)
        id_click("manual-create-btn", 30)
        WebDriverWait(driver, 500).until(EC.visibility_of_element_located((By.ID, "app_name")))
        id_send("app_name", 40, "wow salon")
        id_click("select-arrow-down", 20)
        id_click("project-type-Beauty", 20)
        description_value = "Provide booking and appointment services for the salon."
        id_send('project-description', 30, description_value)
        #change the app category
        category_value = "hair spa, hair cut, hair dressing, make up, pedicure, menicure, facial, waxing, saree draping, skin and hair treatment, body spa, nail do,"
        id_send("project-category-inputbox", 30, category_value)
        id_click("multi-select-down-arrow", 20)
        ele = driver.find_element(By.ID, "multiselect-inputbox")
        id_send("multiselect-inputbox", 20, "Global")  #global region
        ele.send_keys(Keys.ENTER)
        try:
            id_click("next-add-capabilities", 50)
            WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "create-new-capability-card")))
            print(f"Test case 32: App grokker works - Pass")
            a = 1
        except:
            print(f"Test case 32: App grokker doesn't work - Fail")
    except:
        print(f"Unable to get response from grokking / edit the grokker form")
    
    #close the creation
    try:
        b=0
        if(a==1):
            WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "create-new-capability-card")))
            id_click("close-btn", 20)
            b=1
            print(f"Test case 33: Created a draft assistant - Pass")
    except:
        print(f"Test case 33: Created a draft assistant - Fail")


    #Open the draft assistant
    try:
       c=0
       if(b==1):
           WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "create-new-assistant-card")))
           id_click("draft-label", 100)
           c=1
           print(f"Test case 34: Opened the draft assistant - Pass")
    except:
        print(f"Test case 34: Opened the draft assistant - Fail")

    # Adding Capability
    # Add custom capability for Assisted Shopping
    if((c==1) or (b==0)):
        try:
            flag1=0
            replace_string = """Ability to book appointments for the salon services."""
            flag1 = add_custom_capability(replace_string)
            if(flag1==1):
                print(f"Test case 35: Adding custom capability and editing parameters - Pass")
        except:
            print(f"Test case 35: Unable to add custom capability and edit parameters - Fail")
            
        
    #Building Assistant
    try:
        e=0
        if(flag1==1):
            time.sleep(5)
            WebDriverWait(driver, 3000).until(EC.element_to_be_clickable((By.ID, "next-build-assistant-btn")))
            id_click("next-build-assistant-btn", 40)
            WebDriverWait(driver, 10000).until(EC.element_to_be_clickable((By.ID, "try-assistant-btn")))
            id_click("try-assistant-btn", 20)
            try:
                WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.ID, "chat-window-suggestion-0")))
                print(f"Test case 36:  compiling, setting up and configuring - Pass")
                e=1
            except:
                print(f"Test case 36: Unable to compiling, setting up and configuring - Fail")
    except Exception as e:
        print("Unable to build an assistant ", e)

    if(e==1):
        f = check_assistant_details()
        if(f==1):
            print(f"Test case 37: 1-click Integration page works - Pass")
        else:
            print(f"Test case 37: 1-click Integration page doesn't works - Fail")

    if(f==1):
        g=0
        try:
            id_click("side-nav-shortcut-playground", 20) #Click on playgroup tab
            WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.ID, "chat-window-suggestion-0")))
            g=1
        except:
            print("Unable to open playground")

    # First hint is clicked
    if(g==1):
        try:
            sug = driver.find_element(By.ID, "chat-window-suggestion-0")
            par = sug.find_element(By.TAG_NAME, "p")
            print("Query : ", par.text)
            id_click('chat-window-suggestion-0', 30) # click on first hint
            h = pg_fetch_first_response()
            if(h==1):
                print(f"Test case 38: Playground Testing - First hint - Pass")
                for i in range(0, 2):
                    print("")
            else:
                print(f"Test case 38: Playground Testing - First hint - Fail")
        except:
            print(f"First hint could not be clicked")
            network_logs()

    # input box testing
    if(h==1):
        try:
            id_click("pg-new-thread-btn", 20)
            id_send('pg-inputbox', 20, 'Book an appointment for hair cut on monday at 3 pm')
            print("Query : Book an appointment for hair cut on monday at 3 pm")
            id_click("pg-inputbox-send-button", 20)
            ij = pg_fetch_first_expanded_response()
            if(ij==1):
                print(f"Test case 39: Playground Testing - Text input infer works- Pass")
                for i in range(0, 2):
                    print("")
                return 1
            else:
                print("Unable to fetch the output")
        except:
            print(f"Test case 39: Playground Testing - Text input infer doesn't work - Fail")
    return 0   

def log_monitoring():
    try:
        id_click("side-nav-shortcut-monitoring", 20)         #Log monitor is clicked
        try:
            time.sleep(4)
            WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, "monitor-table")))
            try:
                table = driver.find_element(By.ID, "monitor-table")
                try:
                    table_body = table.find_element(By.TAG_NAME, "tbody")
                    rows = table_body.find_elements(By.TAG_NAME, 'tr')
                    try:
                        for row in rows:
                            # row.click()
                            try:
                                cells = row.find_elements(By.TAG_NAME, 'td')
                                for cell in cells:
                                    print(cell.text, end=' ')
                                print()
                                flag=1
                            except:
                                flag=0
                        print(f"Test case 22: Log monitor - viewing the entire table works - Pass")
                        print()
                    except Exception as e:
                        print("td not found ", e)
                        print(f"Test case 22: Log monitor - viewing the entire table doesn't works - Fail")
                        flag = 0
                except:
                    print("tr not found")
                    print(f"Test case 22: Log monitor - viewing the entire table doesn't works - Fail")
                    flag = 0
            except:
                print("table not found")
                print(f"Test case 22: Log monitor - viewing the entire table doesn't works - Fail")
                flag = 0
                print()
        except:
            network_logs()
    except:
        network_logs()


    # Logs - 1 value details
    if (flag == 1):
        try:
            table = driver.find_element(By.ID, "monitor-table")  
            table_body = table.find_element(By.TAG_NAME, "tbody")
            row = table_body.find_element(By.TAG_NAME, 'tr')
            time.sleep(1)
            row.click()
            frag = table_body.find_element(By.ID, "fragmented-tr-0")
            frag.click()
            output = driver.find_element(By.ID, "side-panel-children")
            divs = output.find_elements(By.CLASS_NAME, 'space-y-3')
            for row in divs:
                cells = row.find_elements(By.TAG_NAME, 'p')
                for cell in cells:
                    print(cell.text, end=' ')
                print()
            try:
                pyautogui.moveTo(500, 500, duration=1)  # Move the cursor to the coordinates
                pyautogui.click()
            except:
                network_logs()
            print(f"Test case 23: Log monitor - viewing one row's complete detail works- Pass")
            for i in range(0, 2):
                print("")
            return 1
        except Exception as e:
            print(f"Test case 23: Log monitor - viewing one row's complete detail doesn't work- Fail ", e)
            return 0


def evaluation():
    try:
        id_click("side-nav-shortcut-evaluation", 40)
        id_click("evaluate-btn", 100)
        try:
            d1 = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "evaluation-error-msg")))
            print("Error :", d1.text)
        except:
            try:
                evl_table = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "evaluation-table")))
                WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.ID, "evaluation-status-completed")))
                print("Overall Score")
                table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "overall-evaulation-row-0")))
                trs=table.find_elements(By.TAG_NAME, "tr")
                for tr in trs:
                    tds = tr.find_elements(By.TAG_NAME, "td")
                    for td in tds:
                        print(td.text, end='')
                    print("")
                print("System Evaluation")
                id_click("ceval-id-btn-0", 50)
                table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "system-evaluation")))
                trs=table.find_elements(By.TAG_NAME, "tr")
                for tr in trs:
                    tds = tr.find_elements(By.TAG_NAME, "td")
                    for td in tds:
                        print(td.text, end='')
                    print("")
                print("Agent Evaluation")
                table = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "agent-evaluation")))
                trs=table.find_elements(By.TAG_NAME, "tr")
                for tr in trs:
                    tds = tr.find_elements(By.TAG_NAME, "td")
                    for td in tds:
                        print(td.text, end='')
                    print("")
                return 1
            except:
                print("Evaluation failed or stopped")
                return 0
    except:
        return 0



def edit_an_assistant():
    try:
        id_click("side-nav-shortcut-home", 30)
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "create-new-assistant-card")))
        id_click("assist-card-wow salon", 20)
        id_click("side-nav-shortcut-app-details", 30)
        description_value = "Provide booking and appointment services for the salon. It also provides beauty tips, recommendations and suggestions."
        id_send('project-description', 30, description_value)
        id_click("proj-detail-edit-save-btn", 20)
        id_click("side-nav-shortcut-agents", 20)
        id_click("create-new-capability-card", 40)
        try:
            domain_card = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, "outline-card-0")))
            import_domain = domain_card.find_element(By.ID, "capability-outline-card-small-import")
            import_domain.click()
            time.sleep(3)
            WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.ID, "create-new-capability-card")))
            print(f"Test case 40: Importing capability while editing domain faq - Pass")
        except:
            print(f"Test case 40: Importing capability while editing domain faq - Fail")
        try:
            replace_string = """Ability to tell a joke"""
            flag1 = add_custom_capability(replace_string)
            if(flag1==1):
                print(f"Test case 41: Added a new capability - Pass")
        except:
            print(f"Test case 41: Added a new capability - Fail")
        try:
            time.sleep(5)
            id_click("edit-capability-card-0", 500)
            id_click("add-new-group-btn", 20)
            id_send("new-group-name-inputbox", 20, "shopping")
            id_click("add-group-btn", 20)
            id_click("save-btn", 20)
            if(flag1==1):
                print(f"Test case 42: Editing a capability - Pass")
        except:
            print(f"Test case 42: Editing a capability - Fail")
        a=0
        try:
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID,"ready-to-publish")))
            id_click("publish-btn", 100)
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.ID,"last-published")))
            a=1
            print(f"Test case 43: Republished an assistant - Pass")
        except:
            print(f"Test case 43: Republished an assistant - Fail")
        if(a==1):
            # Playground testing
            b=0
            try:
                id_click("side-nav-shortcut-playground", 20) #Click on playgroup tab
                WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.ID, "chat-window-suggestion-0")))
                b=1
            except:
                print("Unable to open playground")

        # First hint is clicked
        if(b==1):
            try:
                sug = driver.find_element(By.ID, "chat-window-suggestion-0")
                par = sug.find_element(By.TAG_NAME, "p")
                print("Query : ", par.text)
                id_click('chat-window-suggestion-0', 30) # click on first hint
                c = pg_fetch_first_response()
                if(c==1):
                    print(f"Test case 44: Playground Testing - First hint - Pass")
                    for i in range(0, 2):
                        print("")
                else:
                    print(f"Test case 44: Playground Testing - First hint - Fail")
            except:
                print(f"First hint could not be clicked")
                network_logs()

        # input box testing
        if(b==1):
            try:
                id_click("pg-new-thread-btn", 20)
                id_send('pg-inputbox', 20, 'what are some home remidies for hair fall?')
                print("Query : what are some home remidies for hair fall?")
                id_click("pg-inputbox-send-button", 20)
                flag = pg_fetch_first_expanded_response()
                if(flag==1):
                    print(f"Test case 45: Playground Testing - Text input infer works- Pass")
                    for i in range(0, 2):
                        print("")
                    return 1
                else:
                    print("Unable to fetch the output")
            except:
                print(f"Test case 45: Playground Testing - Text input infer doesn't work - Fail")
    except:
        print("Unable to select an existing assistant")
    return 0


def data_store():
    try:
        id_click("side-nav-shortcut-home", 30)
        id_click("side-nav-shortcut-knowledge",30)
        #create a new knowledge
        a=0
        try:
            id_click("create-new-knowledge-btn", 40)
            id_send("knowledge-name", 30, "Add-text")
            id_send("knowledge-description", 30, "This knowledge is used only to test if knowledge can be added from data store")
            id_click("text-knowledge-upload-btn", 20)
            try:
                ele = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID, "monaco-editor")))
                element = ele.find_element(By.TAG_NAME, "textarea")
                element.clear()
                element.send_keys("""Here are some tips for tourists:
                                Research your destination: Before you go, learn about the local culture, customs, and language. You can also ask questions like: 
                                What is the local currency? 
                                What is the main language? 
                                Is the tap water safe to drink? 
                                What is the weather like? 
                                Is tipping expected? 
                                What is considered appropriate attire? 
                                Are there any scams to be aware of? 
                                Get travel insurance: Travel insurance can help you avoid costly expenses during your trip. 
                                Pack light: Pack only what you need and keep it to a minimum. This will make it easier to pack and unpack, and reduce the risk of losing or having your valuables stolen. 
                                Know the language: Learning some basic words and phrases can help you befriend locals and show respect. 
                                Prepare your travel documents: Make sure you have all the necessary travel documents before you leave. 
                                Get vaccinated: If possible, get vaccinated before you travel.""")
            except:
                print("unable to edit monaco editor")
            id_click("text-knowledge-save-btn", 200)
            id_click("create-data-group-btn", 200)
        except:
            print("Unable to create knowledge from knowledge store")

        #Deleteing the newly created knowledge
        try:
            time.sleep(2)
            select_card = driver.find_element(By.ID, "knowledge-card-0")
            dele = select_card.find_element(By.ID, "knowledge-card-trash-icon")
            dele.click()
            id_click("knowledge-delete-alter-delete-btn", 30)
        except:
            print("Unable to select the newly added knowledge")

        #removing refernce and then deleting the assistant
        try:
            time.sleep(2)
            select_card = driver.find_element(By.ID, "knowledge-name-Add-text")
            dele = select_card.find_element(By.ID, "knowledge-card-capability-icon")
            dele.click()
            id_click("knowledge-reference", 30)
            id_click("knowledge-reference-assistant-icon", 30)
            id_click(By.ID, "cap-name-App FAQ")
            id_click("knowledge", 30)
            trashs = driver.find_elements(By.CLASS_NAME, "lucide lucide-trash2 text-red-500")
            for t in trashs:
                t.click()
                id_click("delete_knowledge-alert-delete-btn", 30)
            id_click("save-btn", 30)
            id_click("publish-btn", 40)
            WebDriverWait(driver, 2500).until(EC.presence_of_element_located((By.ID, 'last-published')))
            id_click("side-nav-shortcut-home", 30)
            id_click("side-nav-shortcut-knowledge",30)
            select_card = driver.find_element(By.ID, "knowledge-card-0")
            dele = select_card.find_element(By.ID, "knowledge-card-trash-icon")
            dele.click()
            id_click("knowledge-delete-alter-delete-btn", 30)
            return 1
        except:
            print("Unable to select the newly added knowledge")
    except:
        return 0

                
def auth_testing():
     #Register with an existing user
            main1 = driver.current_window_handle
            id_click("signup-link", 20)  #click on signup
            user = "divya@slanglabs.in"
            x = register_user(user, "abc@123")
            try:
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'signup-auth-error')))
                print(f"Test case 1: Registering an existing user credentials doesn't work {user}- Pass")
            except:
                print(f"Test case 1: Registering an existing user credentials work {user}- Fail")


            # Register with incorrect google credentials
            try:
                id_click('google-auth-btn', 20)
                switch_window('new', main1)
                ele = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")))   #sign in with gmail account - email
                user = "divi12@gmail.com"
                ele.send_keys(user)
                time.sleep(1)
                pyautogui.press('return')
                try:
                    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[2]/div[2]/div/span")))
                    print(f"Test case 2: Signup with invalid google credentials doesn't work {user} - Pass")
                except:
                   print(f"Test case 2: Signup with invalid google credentials doesn't work {user} - Fail")
                switch_window('main', main1)  # Switch back to main window
            except:
                print(f"Registering incorrect credentials worked")
               
                
            # #register with google id
            # try:
            #     driver.refresh()
            #     id_click('google-auth-btn', 20)
            #     user = "sanvi.san.div@gmail.com"
            #     switch_window('new', main1)
            #     google_register(user, "Divya_Tanav2009")
            #     try:
            #         WebDriverWait(driver, 10).until(EC._element_if_visible((By.XPATH,"/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/div[3]")))
            #         xpath_click("/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/div[3]", 20)
            #     except:
            #         network_logs()
            #     switch_window('main', main1)  # Switch back to main window
            #     try:
            #         WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID, "side-nav-shortcut-organization")))
            #         org = get_org_id()
            #         if(org!="0"):
            #             print(f"Test case 3: Signup with new valid google credentials work {user} - Pass")
            #         else:
            #             print(f"Test case 3: Signup with new valid google credentials doesn't work{user} - Fail")
            #         x = log_out()
            #         if(x==0):
            #             print("unable to log out")
            #     except:
            #         print("Unable to google login")
            # except:
            #     print(f"Test case 3: Signup with new valid google credentials work {user} - Fail")
            

            # Login with incorrect user credentials
            driver.refresh()
            id_click("login-link", 20)
            WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.ID, "signup-link")))
            user = "div@slanglabs.in"
            login_cred(user, "ab@123")
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "login-auth-error")))
                print(f"Test case 4: Login with invalid credentials doesn't work {user} - Pass")
            except:
                print(f"Test case 4: Login with invalid credentials work {user} - Fail")
    

            # Forgot password - click reset without email
            try:
                id_click('forgot-password-link', 20)
                id_click("auth-submit-btn", 15)
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID,"reset-password-error")))
                #need to check for alert
                print(f"Test case 5: Forgot password - reset password without email throws error - Pass")
            except:
                print(f"Test case 5: Forgot password - reset password without email works - Fail")


            #click reset with email
            id_send("email-input", 15, "divya@slanglabs.in")
            id_click("auth-submit-btn", 15)
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "check-email-msg")))
                print(f"Test case 6: Forgot password - reset password with email works {user} - Pass")
            except:
                print(f"Test case 6: Forgot password - reset password with email doesn't works {user} - Fail")
            
           
            
            # Login with correct user credentials
            try:
                WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID, 'signup-link')))
                user = "divya@slanglabs.in"
                x = login_cred(user, "abc@123")
                try:
                    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID, 'create-new-assistant-card')))
                    print(f"Test case 7: Login with valid credentials work {user} - Pass")
                    y=log_out()
                    if(y!=1):
                        print("Unable to log-out")
                except:
                    print(f"Test case 7: Registering an existing user credentials work {user}- Fail")
            except:
                print(f"Unable to access email and password")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load configuration based on the environment.')
    parser.add_argument('environment', type=str, help='The environment to load configuration for (stage, prod, dev)')
    args = parser.parse_args()
    try:
        config = load_config(args.environment)
        link = config['host']
        firebase_cred = config['cred']
        mongo_cred = config['mongo_uri']
        try:
            driver.execute_cdp_cmd('Network.enable', {})        # open network tab
            driver.get(link) 

            #Link to website
            id_click("website-link-img", 20)
            tabs = driver.window_handles
            driver.switch_to.window(tabs[-1])
            try:
                WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID, "particles-js")))
                print(f"Test case 1: Website link opens successfully - Pass")
            except:
                 print(f"Test case 1: Website link does not open - Fail")
            driver.close()
            driver.switch_to.window(tabs[0])
            
            # auth testing
            auth_testing()

            #Register a new user
            a=0
            try:
                id_click("signup-link", 20)
                user = "divya"+n+"@slanglabs.in"
                w = register_user(user, "abc@123")
                if(w==1):
                    a=1
                    print(f"Test case 8: Registering a new user credentials work {user} - Pass")
                else:
                    print(f"Test case 8: Registering a new user credentials doesn't work {user} - Fail")
                try:
                    WebDriverWait(driver, 3000).until(EC.element_to_be_clickable((By.ID, 'side-nav-shortcut-organization')))
                    org = get_org_id()
                    if(org!="0"):
                        print(f"Test case 9: Successfully resgisted {user} with org id {org} - Pass")
                    else:
                        print(f"Test case 9: Successfully resgisted {user} with org id {org} - Fail")
                except:
                    print("Unable to register and open account")
                # Manual Assistant creation
                try:
                    id_click("side-nav-shortcut-assistant", 200)
                    d = assistant_create_url_manual(a)
                    try:
                        # Testing in playground
                        e=0
                        if(d==1):
                            e = check_assistant_details()
                            if(e==1):
                                print(f"Test case 21: Integration page works - Pass")
                            else:
                                print(f"Test case 21: Integration page doesn't works - Fail")
                            f = test_assistant_retail()
                            if(f==1):
                                log_monitoring()
                                evaluation()
                    except:
                        print("Unable to test the manually created assistant")
                except:
                    print("Unable to complete manual creation of assistant")

            #     # # # /////////////////////////////////////////////////////////////
            #     # # Tempory account
            #     # d = login_cred("divya26@slanglabs.in", "abc@123")
            #     # WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "create-new-assistant-card")))
            #     # id_click("assist-card-Automated_mkretail", 100)
            #     # time.sleep(5)
            #     # log_monitoring()
            #     # time.sleep(5)
            #     # # # /////////////////////////////////////////////////////////////

                try:
                    # 1-click assistant
                    g = one_click_assistant()
                except:
                    print("Unable to test 1-click assistant")

                try:
                    #draft and manual without url creation
                    h = draft_manual_assistant_without_url()
                except:
                    print("Unable to test draft and without url creation")

                try:
                    #edit an already created assistant
                    k = edit_an_assistant()
                except:
                    print("Unable to test draft and with url creation")

                #Data store
                try:
                    l = data_store()
                except:
                    print("Unable to test data store")

                if((d==1) and (g==1) and (h==1) and (k==1) and (l==1)):
                    z = log_out()
                    if(z==1):
                        print(f"Test case 46: Logged out of newly resgisted assistant {org}'- Pass")
                    else:
                        print(f"Test case 46: Logged out of newly resgisted assistant {org}'- Fail")
                    if(org!="0"):
                        flag1= delete_mongo_user(org, mongo_cred)
                        if(flag1==1):
                            print(f"Test case 47: Successfully deleted user org_id {org}'- Pass")
                        else:
                            print(f"Test case 47: Deleting user org_id {org}'- Fail")
                        flag2= delete_firebase_user_by_email(user, firebase_cred)
                        if(flag2==1):
                            print(f"Test case 48: Successfully deleted user email: {user}'- Pass")
                        else:
                            print(f"Test case 48: Deleting user email: {user}'- Fail")
            except:
                print("Some test cases failed")

        except:
            print("Unable to access studio")

    finally:
        driver.quit()
            
#  To run
#  ../polyglot/.venv/bin/python ../polyglot/tools/testing/Automation/Magic_Studio_console/MS_testing_v2.py stage