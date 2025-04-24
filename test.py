# from selenium import webdriver
# import json
# import time

# # Inicializa o navegador (por exemplo, Chrome)
# driver = webdriver.Chrome()

# # Abre a URL
# driver.get("https://www.sofascore.com/api/v1/sport/-10800/event-count")

# # Aguarda um pouco para garantir que o conteúdo carregue (se necessário)
# time.sleep(2)

# # Captura o conteúdo da página
# content = driver.find_element("tag name", "pre").text

# # Converte o texto para JSON
# data = json.loads(content)

# # Exibe ou usa os dados
# print(data)

# # Encerra o navegador
# driver.quit()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.sofascore.com/api/v1/sport/-10800/event-count")
    #content = page.content()  # Ou `page.text_content('body')` se for JSON
    content = page.text_content('body')
    print(content)
    browser.close()


