import os
import sys
import time
import math
import shutil
import argparse
from os.path import expanduser

class stddev:
   
   mean = 0
   std_dev = 0

   def calc_mean(self, number_list):
      len_list = len(number_list)
      total = 0
      for li in number_list:
         total = total + li
      self.mean = total/len_list      
      return self.mean
      
   def calc_std_dev(self, number_list):
      #=SQRT(((G6-L6)^2+(H6-L6)^2+(I6-L6)^2+(J6-L6)^2+(K6-L6)^2)/5)
      len_list = len(number_list)
      total = 0
      for li in number_list:
         total = total + math.pow((li-self.mean),2)
      total = total/len_list
      return math.sqrt(total)

class testinfo:

   DIR_TEXT = "%DIR%"
   CMD_SLEEP_TIME = 20

   #DROID paths
   sig_path = "#droid.properties#signatures#no-profile#"
   profile_path = "#droid.properties#profiles#"
   
   #DROID signature files
   sig_file = "DROID_SignatureFile_V86.xml"
   container_sig_file = "container-signature-20160727.xml"

   #DROID profiles
   profile_home = ".droid6"
   profile_basename = "droid.properties"
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
      self.md5 = self.md5.replace(self.DIR_TEXT, dir) + self.nul
      
      #sha1
      self.sha1 = self.sha1.replace(self.DIR_TEXT, dir) + self.nul
      
      return [self.sha1, self.md5, self.droid_container, self.droid_no_container, self.sf_NOLIMIT, self.sf_65B, self.sf_10M, self.sf_no_NOLIMIT, self.sf_no_65B, self.sf_no_10M]

   def get_droid_profiles(self):
      p0 = self.cwd + self.profile_path.replace('#', self.sep) 
      p1 = p0 + self.profile_10M
      p2 = p0 + self.profile_65B
      p3 = p0 + self.profile_NOLIMIT
      return [p1, p2, p3]

   def get_droid_home(self):
      home = expanduser("~") 
      return str(home) + self.sep + self.profile_home + self.sep

def output_cmd_time(start_time):
   return (time.time() - start_time)
  
def run_cmd(cmd):
   cmd_start_time = time.time()      
   os.system(cmd)
   runtime = output_cmd_time(cmd_start_time)
   return runtime

def add_csv_field(val):
   val = "%.4f" % round(val,4)   #format the output, despite precition?
   sys.stdout.write(",(" + str(val) + ")")
   
def write_output(text, time_list):
   time_list.pop(0)
   sys.stdout.write(text.replace(" > nul", "") + ",")
   new_t = []
   for t in time_list:
      new_t.append(str(t))
   sys.stdout.write(','.join(new_t))
   
   dev = stddev()
   me = dev.calc_mean(time_list)
   sd = dev.calc_std_dev(time_list)
   
   #seconds
   add_csv_field(me)
   add_csv_field(sd)
   
   #minutes
   add_csv_field(me/60)
   add_csv_field(sd/60)
   
   sys.stdout.write("\n")
   sys.stdout.flush()   #get a look at the results sooner
   
def run_tests(dir, no, start_time):

   ti = testinfo()
   cmd_list = ti.configure_dirs(dir)

   for cmd in cmd_list: 

      #initiate a list of times
      time_list = []

      for n in range(no+1):
      
         #set DROID profiles so we can change MAX BYTE SCAN
         if 'droid-command-line-6.2.1.jar' in cmd and " -Nc " in cmd:
            home = ti.get_droid_home()
            
            for profile in ti.get_droid_profiles():
               droid_prof = home + ti.profile_basename
               shutil.copy(profile, droid_prof)
               
               #output the profile we're using
               time_results = []
               
               #Then run command...
               for y in range(no+1):
                  time_list.append(run_cmd(cmd))
                  if y == no:
                     command_name = cmd + " " + profile
                     prof_text = profile.split("droid.properties-",1)[1]
                     write_output("droid container output: " + prof_text, time_list)
                     outputelapsed(start_time, "Elapsed time, DROID container: " + prof_text)
                     time_list = []
                     
            #get out of the loop and don't triple up...
            break
               
         elif 'droid-command-line-6.2.1.jar' in cmd and " -Nc " not in cmd:
            home = ti.get_droid_home()

            for profile in ti.get_droid_profiles():
               droid_prof = home + ti.profile_basename
               shutil.copy(profile, droid_prof)
               
               #output the profile we're using
               time_results = []         
               
               #Then run command...
               for y in range(no+1):
                  time_list.append(run_cmd(cmd))
                  if y == no:
                     command_name = cmd + " " + profile
                     prof_text = profile.split("droid.properties-",1)[1]
                     write_output("droid non-container output: " + prof_text, time_list)
                     outputelapsed(start_time, "Elapsed time, DROID non-container: " + prof_text)
                     time_list = []
                     
            #get out of the loop and don't triple up...
            break
            
         else:     
            time_list.append(run_cmd(cmd))         
            if n == no:
               write_output(cmd, time_list)
               time_list = []
         
         #give memory time to clear
         time.sleep(ti.CMD_SLEEP_TIME)
      
      if 'java' not in cmd:    
         outputelapsed(start_time, "Elapsed time, cmd: " + cmd)
      
def outputtime(start_time, text=False):
   if text:
      sys.stdout.write(text + ",")
   sys.stdout.write("%s seconds" % (time.time() - start_time) + "\n")

def outputelapsed(start_time, text=False):
   if text:
      sys.stderr.write(text + ": ")
   sys.stderr.write("%s seconds" % (time.time() - start_time) + "\n")

def main():
   #	Usage: --dir [dir to run] --no [number of runs]
   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Experiment to time the intitial stages of digital preservation.\nWARNING: This will overwrite your local droid.profile file, please back it up if you do need it.')
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
   run_tests(args.dir, int(args.no), start_time)
   outputtime(start_time, "Complete script execution time:")

if __name__ == "__main__":      
   main()
