package main

import (
   "io/ioutil"
   "os"
   "fmt"
   "time"
   "math"
   "bufio"
   "strconv"
   "math/rand"   
   "github.com/satori/go.uuid"   
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func doesntExist(name string) bool {
   if _, err := os.Stat(name); os.IsNotExist(err) {
     return true
   }
   return false
}

func makeDirectory(name string) {
   //http://stackoverflow.com/questions/14249467/os-mkdir-and-os-mkdirall-permission-value/31151508#31151508
   if doesntExist(name) {
      err := os.Mkdir(name, 0644)   //http://permissions-calculator.org/
      if err != nil {
         fmt.Fprintln(os.Stderr, "ERROR: Creating directory,", err)
      }
      fmt.Fprintln(os.Stderr, "Made directory:", name)
   } else {
      fmt.Fprintln(os.Stderr, "Directory already exists:", name)
   }
}

var MAXBYTE int32 = 255

func RandomByteString(strlen int) []byte {
   rand.Seed(time.Now().UTC().UnixNano())
   result := make([]byte, strlen)
   for i := 0; i < strlen; i++ {
      result[i] = byte(rand.Int31n(MAXBYTE))  //any byte value between 0 and 255
   }
   return result
}

var BUFSIZE int = 10485760

func makeFile(fsize int, loc string) {
   fname := uuid.NewV4()
   newdir := loc + "\\" + fname.String()
   if fsize > BUFSIZE {    //buffer generation for large files
      for ; fsize > 0 ; {
         f, err := os.OpenFile(newdir, os.O_CREATE | os.O_APPEND, 0644)
         check(err)
         defer f.Close()
         wsize := int(math.Min(float64(BUFSIZE), float64(fsize)))        
         f.Write(RandomByteString(wsize))
         fsize = fsize-BUFSIZE
         if fsize <= 0 {
            fsize = 0
         }
      }
   } else {
      ioutil.WriteFile(newdir, RandomByteString(fsize), 0644)      
   }  
}

var DIRNAME string = "fake_govdocs"
var FOLDERNO int = 100

func main() {

   //time output
   start := time.Now()

   makeDirectory(DIRNAME)
   FILES := 0

   //first dir to output to...
   u1 := uuid.NewV4()  
   newdir := DIRNAME + "\\" + u1.String()  
   makeDirectory(newdir)   

   file, err := os.Open("filesizes")
   check(err)

   scanner := bufio.NewScanner(file)
   for scanner.Scan() {

      if FILES >= FOLDERNO {
         FILES = 0
         u1 = uuid.NewV4()
         newdir = DIRNAME + "\\" + u1.String()  
         makeDirectory(newdir)
      } else {
         FILES+=1
      }

      no, err := strconv.Atoi(scanner.Text())
      check(err)

      makeFile(no, newdir)
   }
   check(scanner.Err())

   elapsed := time.Since(start)
   fmt.Fprintf(os.Stderr, "File generation took %s", elapsed)   
}