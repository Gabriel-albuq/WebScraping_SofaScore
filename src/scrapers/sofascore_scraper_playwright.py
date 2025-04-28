from playwright.sync_api import sync_playwright
import json
import time

class SofaScoreScraper:
    def __init__(self):
        self.base_url = "https://www.sofascore.com/api/v1"

    def get_headers(self):
        return {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }

    def _make_request(self, url):
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)  # Launch headless browser
                    context = browser.new_context()

                    # Abrir a página e capturar o conteúdo JSON
                    page = context.new_page()
                    print(f"Requisitando: {url}")
                    page.goto(url, timeout=10000)

                    # Captura o conteúdo da página
                    content = page.locator("body").text_content()

                    browser.close()

                    # Tenta decodificar o JSON recebido
                    return json.loads(content)
            except json.JSONDecodeError:
                print("Erro ao decodificar JSON.")
                return None
            except Exception as e:
                print(f"Erro ao fazer requisição: {e}")
            
            # Se ocorrer um erro, espera 3 segundos antes de tentar novamente
            attempts += 1
            if attempts < max_attempts:
                print(f"Tentando novamente... ({attempts}/{max_attempts})")
                time.sleep(3)

        # Se atingir o número máximo de tentativas sem sucesso, retorna None
        print("Máximo de tentativas atingido. Não foi possível completar a requisição.")
        return None

    def fetch_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        return self._make_request(url)

# Exemplo de uso
if __name__ == "__main__":
    scraper = SofaScoreScraper()
    data = scraper.fetch_data("sport/-10800/event-count")  # Substitua o endpoint conforme necessário
    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False))
