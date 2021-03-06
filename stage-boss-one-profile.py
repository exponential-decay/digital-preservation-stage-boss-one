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
   NULL_FILE = "NULL.DROID"

   #DROID paths
   sig_path = "#droid.properties#experiment-signature-files#profile#"
   con_profile_path = "#droid.properties#profiles#container#"
   no_con_profile_path = "#droid.properties#profiles#no-container#"
   
   #DROID signature files
   sig_file = "DROID_SignatureFile_V86.xml"
   droid_container_sig_file = "container-signature-20160727.xml"
   droid_no_container = "no-container-signature-20160727.xml"

   #DROID profiles
   profile_home = ".droid6"
   profile_basename = "droid.properties"
   profile_10M = "droid.properties-10MB"
   profile_65B = "droid.properties-65535"
   profile_NOLIMIT = "droid.properties-NOLIMIT"
   
   #don't waste time printing to console
   nul = " > nul"

   #paths to follow
   sf_container = "siegfried.sigs#container#"
   sf_no_container = "siegfried.sigs#no-container#"

   #checksum commands
   md5 = "md5deep -r %DIR%"
   sha1 = "sha1deep -r %DIR%"

   def __init__(self):
 
      self.sep = os.path.sep
      if self.sep == "\\":
         self.sep = "\\\\"
      
      self.cwd = os.getcwd()     

      droid = 'java -Xmx1000m -jar ' + self.cwd + '#droid#droid-command-line-6.2.1.jar -a "%DIR%" -R -p ' + self.NULL_FILE
      self.droid = droid.replace('#', self.sep)

      #sf with container identification
      self.sf_NOLIMIT = "sf -sig " + self.sf_container.replace('#', self.sep) + "NOLIMIT-1.6.2-v86-july2016-default.sig %DIR%"
      self.sf_10M = "sf -sig " + self.sf_container.replace('#', self.sep) + "10MB-1.6.2-v86-july2016-default.sig %DIR%" 
      self.sf_65B = "sf -sig " + self.sf_container.replace('#', self.sep) + "65535-1.6.2-v86-july2016-default.sig %DIR%"

      #sf without container identification
      self.sf_no_NOLIMIT = "sf -sig " + self.sf_no_container.replace('#', self.sep) + "NOLIMIT-1.6.2-v86-july2016-nocontainer-default.sig %DIR%"
      self.sf_no_10M = "sf -sig " + self.sf_no_container.replace('#', self.sep) + "10MB-1.6.2-v86-july2016-nocontainer-default.sig %DIR%"
      self.sf_no_65B = "sf -sig " + self.sf_no_container.replace('#', self.sep) + "65535-1.6.2-v86-july2016-nocontainer-default.sig %DIR%" 

   def copy_signature_files(self):
      #DROIDHOME//container_sigs
      #DROIDHOME//signature_files
      container_home = 'container_sigs'
      standard_home = 'signature_files'
      
      home = self.get_droid_home()
      droid_container = home + container_home
      droid_standard  = home + standard_home      
      
      standard = (self.cwd + self.sig_path + self.sig_file).replace('#', self.sep)
      cont = (self.cwd + self.sig_path + self.droid_container_sig_file).replace('#', self.sep)
      no_cont = (self.cwd + self.sig_path + self.droid_no_container).replace('#', self.sep)
            
      shutil.copy(cont, droid_container)      
      shutil.copy(no_cont, droid_container)
      shutil.copy(standard, droid_standard)

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
      self.droid = self.droid.replace(self.DIR_TEXT, dir) + self.nul

      #md5
      self.md5 = self.md5.replace(self.DIR_TEXT, dir) + self.nul
      
      #sha1
      self.sha1 = self.sha1.replace(self.DIR_TEXT, dir) + self.nul
      
      return [self.sha1, self.md5, self.droid, self.sf_NOLIMIT, self.sf_no_NOLIMIT, self.sf_10M, self.sf_no_10M, self.sf_65B, self.sf_no_65B]

   def get_droid_profiles(self):
      p0 = self.cwd + self.con_profile_path.replace('#', self.sep)      #containers
      p1 = p0 + self.profile_10M
      p2 = p0 + self.profile_65B
      p3 = p0 + self.profile_NOLIMIT
      p4 = self.cwd + self.no_con_profile_path.replace('#', self.sep)   #no containers 
      p5 = p4 + self.profile_10M
      p6 = p4 + self.profile_65B
      p7 = p4 + self.profile_NOLIMIT   
      return [p3, p7, p1, p5, p2, p6]

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
   ti.copy_signature_files()
   cmd_list = ti.configure_dirs(dir)

   for cmd in cmd_list: 

      #initiate a list of times
      time_list = []

      sys.stderr.write(str(no+1) + "\n\n")

      for n in range(no+1):
      
         sys.stderr.write(cmd + " " + str(n) + "\n\n")
      
         #set DROID profiles so we can change MAX BYTE SCAN
         if 'droid-command-line-6.2.1.jar' in cmd:
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
                     prof_text = profile.split("\\\\droid.properties\\\\profiles\\\\",1)[1]
                     write_output("droid container output: " + prof_text, time_list)
                     outputelapsed(start_time, "Elapsed time, DROID container: " + prof_text)
                     time_list = []
               
               if os.path.exists(ti.NULL_FILE):
                  os.remove(ti.NULL_FILE)
      
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

   sys.stderr.write("WARNING: Experiment has started, will overwrite parts of your DROID configuration.\n")

   start_time = time.time()      
   run_tests(args.dir, int(args.no), start_time)
   outputtime(start_time, "Complete script execution time:")

if __name__ == "__main__":      
   main()
