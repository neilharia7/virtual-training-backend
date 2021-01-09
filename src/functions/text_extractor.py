import json

import requests

from config.settings import current_config


def extract_text(path: str, filename: str):
	"""
	
	:return:
	"""
	
	payload = {
		"isOverlayRequired": False,
		"apikey": "925c15151a88957",
		"language": "eng"
	}
	
	with open(path, 'rb') as f:
		response = requests.post(
			current_config.OCR_URL,
			files={filename: f},
			data=payload
		)
	
	return json.loads(response.content.decode())['ParsedResults'][0]['ParsedText']
