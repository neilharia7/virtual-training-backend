import os

from gtts import gTTS
from mutagen.mp3 import MP3

from src.functions.text_extractor import extract_text


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
	os.system(f"ruby {os.getcwd()}/ppt_to_scorm_compliant.rb {course_name} {assignment_description} {course_name}")
	file_path = f'{os.getcwd()}/course_data'
	
	audio_file_list = list()
	
	# Extract text from images
	for file in os.listdir(f'{file_path}'):
		if file.endswith('.jpg'):
			text_details = extract_text(f'{file_path}/{file}', file)
			
			audio_details = gTTS(text=text_details, lang='en', slow=False)
			
			audio_file_name = f"{file_path}/{file.split('.')[0]}.mp3"
			audio_details.save(audio_file_name)
			
			# get the audio length
			audio = MP3(audio_file_name)
			info_length = audio.info.length
			
			audio_file_list.append(audio_file_name)
	
	with open(f'{file_path}/media.json', 'wb') as f:
		for file_name in audio_file_list:
			f.write(file_name)
	
	os.system(f'ruby {os.getcwd()}/ppt_to_scorm_compliant.rb {assignment_name} {assignment_description} {course_name}')
	
	print("done!")
