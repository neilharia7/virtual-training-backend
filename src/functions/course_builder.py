import os

from gtts import gTTS
from mutagen.mp3 import MP3

from config.settings import current_config
from src.functions.text_extractor import extract_text
from aws.s3_functions import upload_audio_s3
import math
import json


def build_scorm_compatible_course(id_number: int, assignment_name: str, assignment_description: str):
	"""
	
	:param id_number:
	:param assignment_name:
	:param assignment_description:
	:return:
	"""
	
	print(
		f'libreoffice --headless --convert-to pdf --outdir {os.getcwd()}/course_data/ {os.getcwd()}/course_data/{assignment_name}')
	os.system(
		f'libreoffice --headless --convert-to pdf --outdir {os.getcwd()}/course_data/ {os.getcwd()}/course_data/{assignment_name}')
	
	course_name = assignment_name.split('.')[0]
	
	# Slide slicing (PPT to images)
	print(
		f'convert -density 400 -resize 2000^ {os.getcwd()}/course_data/{course_name}.pdf {os.getcwd()}/course_data/{assignment_name.split(".")[0]}%d.jpg')
	os.system(
		f'convert -density 400 -resize 2000^ {os.getcwd()}/course_data/{course_name}.pdf {os.getcwd()}/course_data/{assignment_name.split(".")[0]}%d.jpg')
	
	# Images to SCORM compatible
	print(f'course_name: {course_name}')
	print(f'assignment_description {assignment_description}')
	print(f"ruby {os.getcwd()}/ppt_to_scorm_compliant.rb {course_name} {assignment_description} {course_name}")
	# os.system(f"ruby {os.getcwd()}/ppt_to_scorm_compliant.rb {course_name} {assignment_description} {course_name}")
	file_path = f'{os.getcwd()}/course_data'

	audio_file_dict = {'metadata': list()}
	s3_audio_link = f"{current_config.S3_LINK}{course_name}"
	
	complete_assignment_audio = str()
	total_time = 0

	# Extract text from images
	for file in os.listdir(f'{file_path}'):
		if file.endswith('.jpg'):
			print(f'file_name >>  {file}')

			index = int(''.join(filter(str.isdigit, file)))
			text_details = extract_text(f'{file_path}/{file}', file)

			complete_assignment_audio += text_details
			audio_details = gTTS(text=text_details, lang='en', slow=False)
			
			audio_file_name = f"{file_path}/{file.split('.')[0]}_{index}.mp3"
			print(f'audio_file_name {audio_file_name}')
			audio_details.save(audio_file_name)

			os.system(f"aws s3 cp {audio_file_name} s3://{current_config.AWS_S3_BUCKET}/courses/{course_name}/")
			print('uploaded!')
			
			# get the audio length
			audio = MP3(audio_file_name)
			info_length = audio.info.length
			total_time += math.ceil(info_length)
			
			audio_file_dict['metadata'].append({
				"slide": index,
				"audio": f"{s3_audio_link}/{file.split('.')[0]}_{index}.mp3",
				"time": info_length
			})

	audio_details = gTTS(text=complete_assignment_audio, lang='en', slow=False)
	audio_file_name = f"{file_path}/{file.split('.')[0]}_complete.mp3"

	# upload to s3
	audio_details.save(audio_file_name)
	os.system(f"aws s3 cp {audio_file_name} s3://{current_config.AWS_S3_BUCKET}/courses/{course_name}/")
	print('uploaded!')

	audio_file_dict['complete_audio'] = f"{s3_audio_link}/{file.split('.')[0]}_complete.mp3"
	audio_file_dict['total_time'] = total_time
	audio_file_dict['metadata'] = sorted(audio_file_dict['metadata'], key = lambda k: k['slide'])
	print(audio_file_dict)

	counter = 0
	for ad in audio_file_dict['metadata']:
		if ad['slide'] == 0:
			counter = math.ceil(ad['time'])
			ad['time'] = 0
		else:
			temp = math.ceil(ad['time'])
			ad['time'] = counter
			counter += temp

	print(audio_file_dict)
	with open(f'{file_path}/{id_number}_audio.json', 'w') as af:
		af.write(json.dumps(audio_file_dict))
		
	os.system(f"aws s3 cp {os.getcwd()}/courses/ s3://{current_config.AWS_S3_BUCKET}/courses/{course_name}/ --recursive")

	# make items publicily accessible
	os.system(f"aws s3api put-object-acl --bucket {current_config.AWS_S3_BUCKET} --key courses/ --acl public-read")

	scorm_link = f"{current_config.S3_LINK}/{course_name}/index.html"
	
	# TODO delete redundant files
	initial_query(f"call update_assignment_details({id_number}, '{scorm_link}')")
	print("done!")
