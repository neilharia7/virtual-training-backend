require 'zip'
require 'fileutils'
require 'mustache'
require 'json'


# Arguments => title, description, presentation

title = ARGV[0]
STDERR.puts "Course title => #{title}"

# course description is not been added to scorm
description = ARGV[0]
audio = ARGV[2]
STDERR.puts "Course descriptiion => #{description}"

# current dir
dir = "#{Dir.pwd}/course_data"
puts dir

begin
	Dir.mkdir("#{Dir.pwd}/courses/img")
rescue
	puts "destination dir already created"
end

dest_dir = "#{Dir.pwd}/courses"


lis = []

pptx = dir + "/#{ARGV[0]}.pptx"
assignment_id = ARGV[1]
# recursive copy template folder to destination folder
STDERR.puts "Copy template => #{dest_dir}"
FileUtils.cp_r "template", dest_dir
Dir["#{dir}/*.jpg"].each do |file|
	STDERR.puts "Copy #{file} => #{}/img"
	FileUtils.cp file, "#{dest_dir}/img/"
	STDERR.puts "Creating thumb #{file} => #{dest_dir}/img/thumb"
	name = file.split(/\//).last
	system "/usr/bin/convert", "-scale", "200x", file, "#{dest_dir}/img/thumb/#{name}"
	lis.push name
end

ordered = lis.sort_by { |x| x[/\d+/].to_i }
slides = []
thumbs = []
images = []

ordered.each do |name|
  images.push "img/#{name}"
  images.push "img/thumb/#{name}"
  slide =<<SLIDE;
                <div class="tf_slide">
                    <img data-caption="Caption" src="img/#{name}" alt="#{name}" />
                </div>
SLIDE
#   thumb =<<THUMB;
#                     <div class="tf_thumb"><img src="img/#{name}"/></div>
# THUMB
  slides.push slide
  # thumbs.push thumb
end

puts images.to_json
list =<<TEMPLATE;
        <section id="third" class="clearfix tf_slider">
            <div class="tf_container">

                #{slides.join("\n\n")}

                <span id="left"></span>
                <span id="right"></span>

                <div id="tf_thumbs" class="">
                  #{thumbs.join("\n")}
                </div>

            </div>
    </section>
TEMPLATE

puts list

template_file = "#{dest_dir}/index.html"
template = File.read template_file
STDERR.puts "Writing template file: #{template_file}"
template_out = Mustache.render(template, title: title, description: description, slides: list, images: images, assignment_id: assignment_id, audio: audio)
File.open(template_file, "w") do |f|
  f.write template_out
end

slides = {}
media = []

Zip::File.open(pptx) do |zip_file|
  zip_file.each do |entry|
    if entry.name =~ /^ppt\/media\/media/
      media.push entry.name
    end
    # content = entry.get_input_stream.read
  end
end

Zip::File.open(pptx) do |zip_file|
  zip_file.each do |entry|
    if entry.name =~ /^ppt\/slides\/_rels\//
      media.each do |file|
        search = file.gsub(/ppt\//, '')
        content = entry.get_input_stream.read
        slide = entry.name.split(/\//).last.split(/\./).first
        if content =~ /#{search}/
          puts "#{search} -> #{slide}"
          if slides.has_key? slide
            slides[slide].push file
          else
            slides[slide] = [file]
          end
        end
      end
    end
  end
end

files = {}
slides.each_key do |slide|
  slides[slide].each do |file|
    if files.has_key? file
      files[file].push slide
    else
      files[file] = [slide]
    end
  end
end

Zip::File.open(pptx) do |zip_file|
  zip_file.each do |entry|
    if files.has_key? entry.name
      files[entry.name].each_with_index do |slide,i|
        ext = entry.name.split(".").last
        media = "#{slide}_#{i}.#{ext}"
        puts "#{entry.name} -> #{dest_dir}/media/#{media}"
        entry.extract(media)
        FileUtils.mv media, "#{dest_dir}/media/"
      end
    end
    # content = entry.get_input_stream.read
  end
end
