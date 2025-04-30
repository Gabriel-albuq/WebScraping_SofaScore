import os
from curl_cffi import Curl, CurlOpt
import json
import gzip
import zlib
import brotli
import time
from dotenv import load_dotenv

class SofaScoreScraper:
    def __init__(self, proxy_url=None, proxy_user=None, proxy_pass=None):
        load_dotenv()  # Carrega variáveis do arquivo .env
        
        self.curl = Curl()
        self.origin = 'https://www.sofascore.com/api/v1'
        self.api_key = 'sofascore'
        self.content = None
        self.buffer = bytearray()
        self.response_headers = {}

        # Configuração do proxy (prioridade: parâmetros > .env > nenhum proxy)
        self.proxy_url = proxy_url or os.getenv("PROXY_URL")
        self.proxy_user = proxy_user or os.getenv("PROXY_USER")
        self.proxy_pass = proxy_pass or os.getenv("PROXY_PASS")

        # Monta a string de conexão do proxy
        self.proxy = None
        if self.proxy_url:
            if self.proxy_user and self.proxy_pass:
                # Remove protocolo se existir (para evitar duplicação)
                proxy_host = self.proxy_url.split('://')[-1]
                self.proxy = f"http://{self.proxy_user}:{self.proxy_pass}@{proxy_host}"
            else:
                self.proxy = self.proxy_url

    def get_headers(self):
        return {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': self.origin,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }

    def _handle_response(self, data):
        self.buffer.extend(data)
        return len(data)

    def _handle_header(self, data):
        header_line = data.decode('utf-8').strip()
        if ":" in header_line:
            key, value = header_line.split(":", 1)
            self.response_headers[key.strip().lower()] = value.strip()
        return len(data)

    def _make_request(self, url):
        headers = self.get_headers()
        max_retries = 6
        attempt = 0

        while attempt < max_retries:
            try:
                self.buffer = bytearray()
                self.response_headers = {}

                # Configurações básicas
                options = {
                    CurlOpt.URL: url,
                    CurlOpt.HTTPHEADER: [f"{k}: {v}".encode('utf-8') for k, v in headers.items()],
                    CurlOpt.SSL_VERIFYPEER: 0,
                    CurlOpt.SSL_VERIFYHOST: 0,
                    CurlOpt.TIMEOUT: 15,
                    CurlOpt.FOLLOWLOCATION: 1,
                    CurlOpt.MAXREDIRS: 5,
                    CurlOpt.WRITEFUNCTION: self._handle_response,
                    CurlOpt.HEADERFUNCTION: self._handle_header
                }

                # Adiciona proxy se configurado
                if self.proxy:
                    options[CurlOpt.PROXY] = self.proxy
                    # Para proxies SOCKS (opcional)
                    if self.proxy.startswith('socks'):
                        options[CurlOpt.PROXYTYPE] = CurlOpt.PROXYTYPE_SOCKS5_HOSTNAME

                # Aplica todas as opções
                for opt, value in options.items():
                    self.curl.setopt(opt, value)

                self.curl.perform()

                if not self.buffer:
                    raise Exception("Nenhum conteúdo recebido")

                http_code = self.curl.getinfo(2097154)  # CURLINFO_RESPONSE_CODE
                if http_code != 200:
                    raise Exception(f"Erro HTTP {http_code}")

                content_encoding = self.response_headers.get("content-encoding", "").lower()
                if content_encoding == 'gzip':
                    self.content = gzip.decompress(self.buffer).decode('utf-8')
                elif content_encoding == 'deflate':
                    self.content = zlib.decompress(self.buffer).decode('utf-8')
                elif content_encoding == 'br':
                    self.content = brotli.decompress(self.buffer).decode('utf-8')
                else:
                    self.content = self.buffer.decode('utf-8')

                return json.loads(self.content)

            except Exception as e:
                attempt += 1
                print(f"Tentativa {attempt}/{max_retries} falhou: {str(e)}")
                if attempt < max_retries:
                    time.sleep(10)
                else:
                    raise Exception(f"Falha após {max_retries} tentativas: {str(e)}")
            finally:
                self.curl.reset()  # Limpa configurações para a próxima requisição