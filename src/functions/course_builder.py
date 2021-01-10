import os

from gtts import gTTS
from mutagen.mp3 import MP3

from config.settings import current_config
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
	
	audio_file_list = dict()
	
	s3_audio_link = f"{current_config.S3_LINK}/{assignment_name}"
	
	counter = 0
	# Extract text from images
	for index, file in enumerate(os.listdir(f'{file_path}')):
		if file.endswith('.jpg'):
			text_details = extract_text(f'{file_path}/{file}', file)
			
			audio_details = gTTS(text=text_details, lang='en', slow=False)
			
			audio_file_name = f"{file_path}/{file.split('.')[0]}_{index}.mp3"
			audio_details.save(audio_file_name)
			
			# get the audio length
			audio = MP3(audio_file_name)
			info_length = audio.info.length
			
			audio_file_list.append({
				"slide": index,
				"audio": f'{s3_audio_link}/{audio_file_name}',
				"time": counter
			})
			
			counter += round(int(info_length))
	
	with open(f'{file_path}/course_data/{course_name}_audio.txt', 'wb') as af:
		af.write(str(audio_file_list))
	
	os.system(f'ruby {os.getcwd()}/ppt_to_scorm_compliant.rb {assignment_name} {assignment_description} {course_name}')
	os.system(f"aws s3 cp {os.getcwd()}/course_data/ s3://{current_config.AWS_S3_BUCKET}/courses/{course_name}/")
	
	# TODO add to s3 and update table
	print("done!")
