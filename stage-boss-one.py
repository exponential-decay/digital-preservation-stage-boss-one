import os
import sys
import time
import argparse

sig_path = "droid.properties/signatures/"

sig_file = "DROID_SignatureFile_V85.xml"
container_sig_file = "container-signature-20160629.xml"

java_no_container = 'java -Xmx1000m -jar droid-command-line-6.2.1.jar -Nr "%DIR%" -Ns "' + sig_path + sig_file + '" -R'
java_container = 'java -Xmx1000m -jar droid-command-line-6.2.1.jar -Nr "%DIR%" -Ns "' + sig_path + sig_file + '"-Nc "' + sig_path + container_sig_file + '" -R'

nul = "> nul"

#paths to follow
container = "siegfried.sigs/container/"
no_container = "siegfried.sigs/no-container/"

#sf with container identification
sf_one = "sf -sig " + container + "NOLIMIT-1.6.1-v85-june2016-default.sig %DIR%"
sf_two = "sf -sig " + container + "10MB-1.6.1-v85-june2016-default.sig %DIR%" 
sf_three = "sf -sig " + container + "65535-1.6.1-v85-june2016-default.sig %DIR%"

#sf without container identification
sf_no_one = "sf -sig " + no_container + "NOLIMIT-1.6.1-v85-june2016-nocontainer-default.sig %DIR%"
sf_no_two = "sf -sig " + no_container + "10MB-1.6.1-v85-june2016-nocontainer-default.sig %DIR%"
sf_no_three = "sf -sig " + no_container + "65535-1.6.1-v85-june2016-nocontainer-default.sig %DIR%" 

print java_no_container
print java_container
print sf_one
print sf_two
print sf_three
print sf_no_one
print sf_no_two
print sf_no_three

def run_tests():
   start_time = time.time()
   outputtime(start_time)

   os.system(sf_no_one.replace("%DIR%", "-version"))

def outputtime(start_time):
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

   run_tests()

if __name__ == "__main__":      
   main()
