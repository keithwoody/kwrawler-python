# -*- mode: ruby -*-
# More info at https://github.com/guard/guard#readme
 
require 'guard/guard'

if RUBY_PLATFORM.match('linux')
  notification :libnotify
elsif RUBY_PLATFORM.match('darwin|mac')
  # notification :growl
  notification :off
end
 
module ::Guard
  class Pytest < ::Guard::Guard
    def run_all
      # NOTE althought this could be cached
      # needs to update when files are created
      test_files = get_test_files([Dir.getwd]) 
      output = `py.test -q #{test_files.join(' ')}`
      puts output
 
      send_notification(output, "All: ")

    end
 
    def run_on_change(paths)
      puts paths
      test_files = get_test_files(paths)
 
      output = `py.test -q #{test_files.join(' ')}`
      puts output
 
      send_notification(output)
    end

    def get_test_files(paths)
      # TODO make this more general (go deeper)
      test_files = paths.reject { |path| path.match %r{^tests/} }.inject( [] ) do |test_files, path|
        base = Dir.getwd
        dir = File.dirname( path )
        dirs = dir.split( '/' )
        filename = File.basename( path )
        puts filename
        [
          "tests/#{dir}/test_#{filename}",
          "tests/test_" + filename,
          "tests/test_" + ( dirs ).join( '_' ) + '_' +  filename,
          base + "/tests/#{dir}/test_#{filename}",
          base + "/tests/test_" +  filename,
          base + "/tests/test_" + ( dirs ).join( '_' ) + '_' +  filename,
          "#{dir}/tests/test_#{filename}",
          "#{dir}/test_#{filename}"
        ].select do |pattern|
          test_files << pattern if File.exists? pattern
        end
      end
      test_files += paths.grep( %r{^tests/} )
    end

    def send_notification(output, prefix="Test: ")
      # Send out a notification, via Growl (mac) or libnotify (linux).
      result_match = output.match( /\n.*seconds$/ )
      result = result_match ? result_match[0] : "unknown failure"
      image  = result.match( /fail/ ) ? :failed : :success
      project_name = File.basename(Dir.getwd)
      ::Guard::Notifier.notify( result,
                                :title => prefix + project_name, 
                                :image => image )
    end
  end
end
 
guard :py_test do
  watch( %r{.*.py$} )
  watch( %r{^tests/.*.py$} )
end
