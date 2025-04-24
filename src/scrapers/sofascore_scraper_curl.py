import os
from curl_cffi import Curl, CurlOpt, CurlError
import json
import gzip
import zlib
import brotli
import time

class SofaScoreScraper:
    def __init__(self):
        self.curl = Curl()
        self.origin = 'https://www.sofascore.com/api/v1'
        self.api_key = 'sofascore'
        self.content = None
        self.buffer = bytearray()  # Buffer para coletar resposta
        self.response_headers = {}  # Para armazenar os cabeçalhos da resposta

    def get_headers(self):
        return {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': self.origin,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }

    def _handle_response(self, data):
        """ Callback para armazenar os dados recebidos. """
        self.buffer.extend(data)
        return len(data)

    def _handle_header(self, data):
        """ Callback para armazenar cabeçalhos da resposta. """
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
                self.buffer = bytearray()  # Resetar buffer
                self.response_headers = {}  # Resetar cabeçalhos

                self.curl.setopt(CurlOpt.URL, url)
                self.curl.setopt(CurlOpt.HTTPHEADER, [f"{k}: {v}".encode('utf-8') for k, v in headers.items()])
                self.curl.setopt(CurlOpt.SSL_VERIFYPEER, 0)
                self.curl.setopt(CurlOpt.SSL_VERIFYHOST, 0)
                self.curl.setopt(CurlOpt.TIMEOUT, 10)
                self.curl.setopt(CurlOpt.FOLLOWLOCATION, 1)
                self.curl.setopt(CurlOpt.MAXREDIRS, 5)
                self.curl.setopt(CurlOpt.WRITEFUNCTION, self._handle_response)
                self.curl.setopt(CurlOpt.HEADERFUNCTION, self._handle_header)
                self.curl.perform()

                if not self.buffer:
                    raise Exception("Nenhum conteúdo recebido.")

                http_code = self.curl.getinfo(2097154)  # CurlInfo.RESPONSE_CODE
                if http_code != 200:
                    raise Exception(f"Erro HTTP {http_code}: {self.buffer.decode('utf-8', errors='ignore')}")

                # Decodificar conforme content-encoding
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
                print(f"Tentativa {attempt}/{max_retries} falhou: {e}")
                if attempt < max_retries:
                    time.sleep(10)
                else:
                    raise Exception(f"Falha após {max_retries} tentativas: {e}")

    def _handle_response(self, data):
        """
        Callback function to handle response data.
        Appends the data to the buffer.
        """
        self.buffer.extend(data)
        return len(data)  # Return the length of the data processed

    def _get_content_encoding(self):
        """
        Get the Content-Encoding header from the response.
        """
        # Use curl_cffi's getinfo to retrieve headers
        headers = self.curl.getinfo(CurlOpt.HEADER)
        if headers:
            for line in headers.decode('utf-8').splitlines():
                if line.lower().startswith('content-encoding:'):
                    return line.split(':', 1)[1].strip().lower()
        return None