import os
import sys
import time
import argparse

class testinfo:

   DIR_TEXT = "%DIR%"
   SLEEP_TIME = 5

   sig_path = "#droid.properties#signatures#"
   sig_file = "DROID_SignatureFile_V85.xml"
   container_sig_file = "container-signature-20160629.xml"
   
   #don't waste time printing to console
   nul = "> nul"

   #paths to follow
   container = "siegfried.sigs#container#"
   no_container = "siegfried.sigs#no-container#"

   def __init__(self):
 
      self.sep = os.path.sep
      if self.sep == "\\":
         self.sep = "\\\\"
      
      self.cwd = os.getcwd()
      
      droid_no_container = 'java -Xmx1000m -jar ' + self.cwd + '#droid#droid-command-line-6.2.1.jar -Nr "%DIR%" -Ns "' + self.cwd + self.sig_path + self.sig_file + '" -R'
      droid_container = 'java -Xmx1000m -jar #droid#droid-command-line-6.2.1.jar -Nr "%DIR%" -Ns "' + self.cwd + self.sig_path + self.sig_file + '"-Nc "' + self.cwd + self.sig_path + self.container_sig_file + '" -R'

      self.droid_no_container = droid_no_container.replace('#', self.sep)
      self.droid_container = droid_container.replace('#', self.sep)

      #sf with container identification
      self.sf_one = "sf -sig " + self.container + "NOLIMIT-1.6.1-v85-june2016-default.sig %DIR%"
      self.sf_two = "sf -sig " + self.container + "10MB-1.6.1-v85-june2016-default.sig %DIR%" 
      self.sf_three = "sf -sig " + self.container + "65535-1.6.1-v85-june2016-default.sig %DIR%"

      #sf without container identification
      self.sf_no_one = "sf -sig " + self.no_container + "NOLIMIT-1.6.1-v85-june2016-nocontainer-default.sig %DIR%"
      self.sf_no_two = "sf -sig " + self.no_container + "10MB-1.6.1-v85-june2016-nocontainer-default.sig %DIR%"
      self.sf_no_three = "sf -sig " + self.no_container + "65535-1.6.1-v85-june2016-nocontainer-default.sig %DIR%" 

def run_tests(dir, no):

   ti = testinfo()

   '''
   ti.returncommands()  #return an array dictionary of command labels and commands
   run each command x times
   add each time to an array 
   calculate mean
   calculate standard deviation
   output to stderr
   run next command
   output all results to console
   '''

   cmd = ti.droid_no_container.replace(ti.DIR_TEXT, "C:\\\\working\\\\droid-test\\\\govdocs\\\\")   
   os.system(cmd)
   time.sleep(ti.SLEEP_TIME)


def outputtime(start_time, text=False):
   if text:
      sys.stderr.write(text)
   sys.stderr.write("\n" + "--- %s seconds ---" % (time.time() - start_time) + "\n")

def main():

   #	Usage: --dir [dir to run] --no [number of runs]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Experiment to time the intitial stages of digital preservation.')
   parser.add_argument('--dir', help='Directory of files to run the experiment over.', default=False)
   parser.add_argument('--no', help='Number of iterations to generate statistics for.', default=False)

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()

   if not args.dir:
      sys.stderr.write("Must enter a directory of files to scan.")
      sys.exit(1)

   if not args.no or int(args.no) <= 0:
      sys.stderr.write("Must enter a number for iterations.")
      sys.exit(1)

   start_time = time.time()      
   run_tests(args.dir, args.no)
   outputtime(start_time, "Complete script time:")

if __name__ == "__main__":      
   main()
