require 'find'
require 'mimemagic'
require 'digest/md5'
require 'set'
require 'childprocess'
require 'fileutils'
require 'json'
include FileUtils

TEST_FRAMES = 100
START_TIME = "00:00:20"
SEARCH_DIR = File.expand_path("video/")
TMP_DIR = File.expand_path("tmp/")
TILES_DIR = File.expand_path("tiles/")

# Create directories if they don't exist
mkdir SEARCH_DIR if ! File.directory?(SEARCH_DIR)
mkdir TMP_DIR if ! File.directory?(TMP_DIR)
mkdir TILES_DIR if ! File.directory?(TILES_DIR)

# Helper to run command silently and raise exception if didn't run correctly
def quietrun(cmd)
    process = ChildProcess.build(*cmd)
    process.start
    begin
      process.poll_for_exit(60)
    rescue ChildProcess::TimeoutError
    end
    return process.exit_code
end

Dir.chdir(TMP_DIR) do
  Find.find(SEARCH_DIR) do |filename|

    # Skip if not a file or not video
    next if ! File.file?(filename)
    filemime = MimeMagic.by_path(filename)
    next if ! filemime || ! filemime.video?
    puts "*** Analysing: %s" % filename

    # Get some frames with mplayer
    print "\tMplayer "
    if quietrun(['mplayer', '-nosound', '-vo', 'jpeg', '-fps', '10', '-vf', 'scale=320:240', '-ss', START_TIME, '-frames', TEST_FRAMES.to_s, filename]) != 0
      print "...failed, skipping...\n"
      next
    end

    # Sanity check
    if %x(ls *.jpg).split("\n").length < 1
      puts "\n\tUnable to create images, skipping..."
      next
    end

    scores = []
    print "|| ImageMagick tiles "
    Find.find(TMP_DIR) do |frame|
      quietrun(['convert', '-colorspace', 'gray', '-crop', '80x120', frame, '../tiles/tile%03d.png'])

      scores.push(IO.popen(['python', File.expand_path("../centroid/centroid.py"), TILES_DIR+"/tile*.png"]).read.strip)
    end

    File.open(filename+".json", 'w+') { |file| file.write(scores.to_json) }

    # Delete the images created by mogrify and mplayer
    #rm(%x(ls *.jpg).split("\n"))

  end
end