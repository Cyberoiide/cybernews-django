import requests
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

class DjangoAPIPipeline:
    def open_spider(self, spider):
        self.token = os.getenv("DJANGO_API_TOKEN")
        if not self.token:
            raise ValueError("DJANGO_API_TOKEN is missing in environment variables")

        self.endpoint = "http://web:8000/api/articles/"
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

    def process_item(self, item, spider):
        try:
            response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(item))
            if response.status_code not in [200, 201]:
                logging.error(f"❌ POST failed: {response.status_code} - {response.text}")
            else:
                logging.info(f"✅ Article posté : {item.get('title')}")
        except Exception as e:
            logging.error(f"🔥 Exception during POST: {e}")
        return item
