import os
import sys
import time
import argparse

class testinfo:

   DIR_TEXT = "%DIR%"
   SLEEP_TIME = 5

   #DROID paths
   sig_path = "#droid.properties#signatures#"
   profile_path = "#droid.properties#profiles#"
   
   #DROID signature files
   sig_file = "DROID_SignatureFile_V85.xml"
   container_sig_file = "container-signature-20160629.xml"

   #DROID profiles
   profile_10M = "droid.properties-10MB"
   profile_65B = "droid.properties-65535"
   profile_NOLIMIT = "droid.properties-NOLIMIT"
   
   #don't waste time printing to console
   nul = " > nul"

   #paths to follow
   container = "siegfried.sigs#container#"
   no_container = "siegfried.sigs#no-container#"

   #checksum commands
   md5 = "md5deep -r %DIR%"
   sha1 = "sha1deep -r %DIR%"

   def __init__(self):
 
      self.sep = os.path.sep
      if self.sep == "\\":
         self.sep = "\\\\"
      
      self.cwd = os.getcwd()
      
      droid_no_container = 'java -Xmx1000m -jar ' + self.cwd + '#droid#droid-command-line-6.2.1.jar -Nr "%DIR%" -Ns "' + self.cwd + self.sig_path + self.sig_file + '" -R'
      droid_container = 'java -Xmx1000m -jar ' + self.cwd + '#droid#droid-command-line-6.2.1.jar -Nr "%DIR%" -Ns "' + self.cwd + self.sig_path + self.sig_file + '" -Nc "' + self.cwd + self.sig_path + self.container_sig_file + '" -R'

      self.droid_no_container = droid_no_container.replace('#', self.sep)
      self.droid_container = droid_container.replace('#', self.sep)

      #sf with container identification
      self.sf_NOLIMIT = "sf -sig " + self.container.replace('#', self.sep) + "NOLIMIT-1.6.1-v85-june2016-default.sig %DIR%"
      self.sf_65B = "sf -sig " + self.container.replace('#', self.sep) + "10MB-1.6.1-v85-june2016-default.sig %DIR%" 
      self.sf_10M = "sf -sig " + self.container.replace('#', self.sep) + "65535-1.6.1-v85-june2016-default.sig %DIR%"

      #sf without container identification
      self.sf_no_NOLIMIT = "sf -sig " + self.no_container.replace('#', self.sep) + "NOLIMIT-1.6.1-v85-june2016-nocontainer-default.sig %DIR%"
      self.sf_no_65B = "sf -sig " + self.no_container.replace('#', self.sep) + "10MB-1.6.1-v85-june2016-nocontainer-default.sig %DIR%"
      self.sf_no_10M = "sf -sig " + self.no_container.replace('#', self.sep) + "65535-1.6.1-v85-june2016-nocontainer-default.sig %DIR%" 

   def configure_dirs(self, dir):   
      if '\\' in dir:
         dir = dir.replace("\\", "\\\\")
   
      #sf with container identification
      self.sf_NOLIMIT = self.sf_NOLIMIT.replace(self.DIR_TEXT, dir) + self.nul
      self.sf_65B = self.sf_65B.replace(self.DIR_TEXT, dir) + self.nul
      self.sf_10M = self.sf_10M.replace(self.DIR_TEXT, dir) + self.nul

      #sf without container identification
      self.sf_no_NOLIMIT = self.sf_no_NOLIMIT.replace(self.DIR_TEXT, dir) + self.nul
      self.sf_no_65B = self.sf_no_65B.replace(self.DIR_TEXT, dir) + self.nul
      self.sf_no_10M = self.sf_no_10M.replace(self.DIR_TEXT, dir) + self.nul
      
      #droid
      self.droid_no_container = self.droid_no_container.replace(self.DIR_TEXT, dir) + self.nul
      self.droid_container = self.droid_container.replace(self.DIR_TEXT, dir) + self.nul

      #md5
      self.md5.replace(self.DIR_TEXT, dir) + self.nul
      
      #sha1
      self.sha1.replace(self.DIR_TEXT, dir) + self.nul
      
      return [self.sha1, self.md5, self.droid_container, self.droid_no_container, self.sf_NOLIMIT, self.sf_65B, self.sf_10M, self.sf_no_NOLIMIT, self.sf_no_65B, self.sf_no_10M]

def run_cmd(cmd):
   print "xxx"

def run_tests(dir, no):

   ti = testinfo()
   cmd_list = ti.configure_dirs(dir)

   for cmd in cmd_list:
      sys.stderr.write(cmd + "\n")
      if 'droid' in cmd and " -Nc " in cmd:
         print "droid-container"
      elif 'droid' in cmd and " -Nc " not in cmd:
         print "droid-no-container"
      os.system(cmd)
      sys.stderr.write('\n')


   '''
   ti.returncommands()  #return an array dictionary of command labels and commands
   run each command x times
   monitor exit status
   add each time to an array 
   calculate mean
   calculate standard deviation
   output to stderr
   run next command
   output all results to console
   '''


   time.sleep(ti.SLEEP_TIME)


def outputtime(start_time, text=False):
   if text:
      sys.stderr.write("--- " + text + " ---")
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
   run_tests(args.dir, int(args.no))
   outputtime(start_time, "Complete script execution time:")

if __name__ == "__main__":      
   main()
