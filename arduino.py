import sublime
import sublime_plugin

import os
import thread
import subprocess
import sys
# import re

PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
PLUGIN_PATH = os.getcwd().replace(os.path.join(os.getcwd(), '..', '..') + os.path.sep, '').replace(os.path.sep, '/')
RESULT_VIEW_NAME = 'monitor_result_view'

packages_dir = sublime.packages_path()
arduino_dir = '/Applications/Arduino.app/Contents/Resources/Java'
reference_dir = '%s/reference' % arduino_dir
keywords_file = '%s/lib/keywords.txt' % arduino_dir
css_file = "%s/arduinoUno.css" % reference_dir
make_path = '%s/hardware/tools/avr/bin/make' % arduino_dir
user_dir = '${HOME}/Documents/Arduino/'

def plugin_file(name):
    return os.path.join(PLUGIN_PATH, name)

class CompileCommand(sublime_plugin.WindowCommand):
    """ Compile the current file """
    def run(self):
        self.window.run_command('set_build_system', {
          'file': 'Packages/ST2-Arduino/Arduino-Compile.sublime-build'
        })
        self.window.run_command('build')

class UploadCommand(sublime_plugin.WindowCommand):
    """ Upload the current sketch to the board """
    def run(self):
        self.window.run_command('set_build_system', {
          'file': 'Packages/ST2-Arduino/Arduino-Upload.sublime-build'
        })
        self.window.run_command('build', "upload": "upload")

class NewSketchCommand(sublime_plugin.WindowCommand):
    """ Create new sketch file from template """
    def run(self):
        template = open(plugin_file('sketch_template'), 'r').read()
        file = self.window.new_file()
        edit = file.begin_edit()
        file.insert(edit, 0, template)
        file.end_edit(edit)

class OpenArduinoDirectory(sublime_plugin.WindowCommand):
    """ Open Arduino's application directory """
    def run(self):
        if sys.platform == 'darwin':
            path = arduino_dir
            subprocess.check_call(['open', '--', path])

class OpenArduinoLibraries(sublime_plugin.WindowCommand):
    """ Open Arduino's built-in libraries """
    def run(self):
        if sys.platform == 'darwin':
            path = '%s/libraries' % arduino_dir
            subprocess.check_call(['open', '--', path])

class OpenArduinoExamples(sublime_plugin.WindowCommand):
    """ Open Arduino's example sketches directory """
    def run(self):
        if sys.platform == 'darwin':
            path = '%s/examples' % arduino_dir
            subprocess.check_call(['open', '--', path])

class OpenUserArduinoDirectory(sublime_plugin.WindowCommand):
    """ Open user's arduino directory """
    def run(self):
        path = os.getenv('HOME') + '/Documents/Arduino'
        subprocess.check_call(['open', '--', path])

class OpenUserArduinoLibraries(sublime_plugin.WindowCommand):
    """ Open user's library files """
    def run(self):
        path = os.getenv('HOME') + '/Documents/Arduino/libraries'
        subprocess.check_call(['open', '--', path])

class LocalHelpCommand(sublime_plugin.TextCommand):
    """ Open Arduino help for currently selected word """
    def run(self, edit):
        loop = 'loop'
        sel = self.view.sel()[0]
        if not sel.empty():
            word = self.view.substr(sel)
        else:
            word = ""

        lines = [line.split() for line in open(keywords_file)]
        keywords = [l for l in lines if ((len(l) >= 2) or (l and l[0] != "#"))]
        for kw in keywords:
            if word == kw[0]:
                html_file = '%s/%s.html' % (reference_dir, kw[-1])

        if 'html_file' in locals():
            try:
                subprocess.check_call(['open', html_file])
                # Will add this if sublime ever gets formatted output window
                # html = open(html_file).read()
                # css = open(css_file).read() + """
                #     #wikitext p:first-child,
                #     #pageheader,
                #     #pagenav,
                #     #pagefooter {
                #         display: none;
                #     }
                #     #page {
                #         width: 100%;
                #     }
                # """
                # html = re.sub('<link.*arduino.*\.css.*?>', "<style type='text/css'>#{css}</style>", html, re.S|re.I)
            except Exception, e:
                print "failed to open html"
        else:
            print 'No documentation found for "%s"' % word
