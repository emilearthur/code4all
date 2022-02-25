package main

import (
	"compress/gzip"
	"crypto/md5"
	"crypto/sha1"
	"fmt"
	"io"
	"os"
	"strings"
)

// IO with readers and writers
// go models data input and output as a stream that flows from source to target. data sources such as files, netoworked
// connections or even some in-memory objects can be modeled as streams of btes from which data can be read or written.
// i.e. data source[input with reader: reads btyes into stream]  --> [stream of bytes ([]bytes)] --> data source[output with writer: writes bytes from stream]
// the stream of data is represented as a slice of bytes([]byte) that can be accessed from reading or writing.

// The io.Reader interface
// io.Reader interface helps implement codes that reads and transfer data from a source into a stream of bytes.
// the io.Read interface is simple. it consist of a single method, Read([]bytes) (int, error) intended to let programmers
// implement code that reads data from an arbitrary source and transfers it into  the provided slice of bytes.

// Reader interface here
type Reader interface {
	Read(p []byte) (n int, err error) // returns total number of bytes transferred into the provided slice and err value value
}

type alphaReaderR string

func (a alphaReaderR) Read(p []byte) (int, error) {
	count := 0
	for i := 0; i < len(a); i++ {
		if (a[i] >= 'A' && a[i] <= 'Z') || (a[i] >= 'a' && a[i] <= 'z') {
			p[i] = a[i]
		}
		count++
	}
	return count, io.EOF //io.EOF is returned when the reader has no more data to transfer into stream p
}

// Chaining readers
// chances that the standard library already has a reader that can be resued. thus its common to wrap an existing reader and use
// it to stream as  the source for new implementation. e.g. below
type alphaReader struct {
	src io.Reader // alphaReader type is now a struct which embeds an io.Reader value.
}

// NewAlphaReader implmentation
func NewAlphaReader(source io.Reader) *alphaReader { // to use alphaReader, it must be provided with an existing reader,
	// which is facilitated by this constuctor function.
	return &alphaReader{source}
}

func (a *alphaReader) Read(p []byte) (int, error) { // when this enovked, it calls the wrapper reader as a.src.Read(p),
	// which will inject the source data into bytes slice p.
	if len(p) == 0 {
		return 0, nil
	}
	count, err := a.src.Read(p) // p has now the data source
	if err != nil {
		return count, err
	}
	for i := 0; i < len(p); i++ {
		if (p[i] >= 'A' && p[i] <= 'Z') || (p[i] >= 'a' && p[i] <= 'z') {
			continue
		} else {
			p[i] = 0
		}
	}
	return count, io.EOF
}

// The io.Writer interface

// Writer interface here
type Writer interface {
	Write(p []byte) (n int, err error)
}

// the interface requires the implmentation of a single method, Write (p []bytes) (c int, e error) that copies data from the
// the provided stream p and writes the data to sink resources such as an in-memory structure, standard output, a file, a network
// connection or a number of io.Writer implmentations that comes with the Go stardard library. the Write method returns the
// he number of bytes copied from p followed by an error value if any was encountered.

// implmentation of the channelWriter type.
// channelWriter type - a writer that decomposes and serializes its stream that sent over a Go channel as consecutive bytes.
type channelWriter struct {
	Channel chan byte
}

// NewChannelWriter function -
func NewChannelWriter() *channelWriter {
	return &channelWriter{
		Channel: make(chan byte, 1024),
	}
}

func (c *channelWriter) Write(p []byte) (int, error) {
	if len(p) == 0 {
		return 0, nil
	}
	go func() { // using go routine to copy each byte  from p and send it to across the channel. go routine closes channel after
		// completion, so consumers are notified when to stop consuming from the channel.
		defer close(c.Channel) // when done
		for _, b := range p {
			c.Channel <- b
		}
	}()
	return len(p), nil
}

// Working with the io package
// io package define input and output primitives as teh io.Reader and io.Writer interfaces.
// io.Copy() -->	its a variants io.CopyBuffer and io.CopyN and its makes it easy to copy data from an arbitrary io.Reader source
//				into an equally arbitrary io.Write,
// PipeReader / PipeWriter --> inclues PipeReadder and PipeWriter types that model IO operations as in-mem pipe. Data is writtern
//							   to the pipe's io.Writer and can independently be read at the pipe's io.Reader.
// io.TeeReader() --> Similar to io.Copy function, io.TeeReader transfers content from a reader to a writer. also the function
//					  also emits the copied bytes(unaltered) via a returned io.Reader. The teeReader works well for composing
//					  multi-step IO stream processing.
// io.WriteString() --> io.WriteString function writes the content of string into a specified wrtie.
// io.LimitedReader --> io.LimitedReader struct is a reader that reads only N number of bytes from the specified io.Reader.
// io.SectionReader --> io.SectionReader type implments seek and skip primitives by specifying an index (zero based) where
//						to start reading and an offset value indicating the number of bytes to read.

// Function os.OpenFile
// the os.OpenFile function provides generic low-level functionalities to create a new file or open existing file with
// fine-grained control over the file's behavior and its permission.
// os.OpenFile function take three params,i.e. first one is the path of the file, second is a masked bit-field values to
// indicate the behavior of the operation (e.g. read-only, read-write, rtruncate and etc), last is a posix-compliant permission
// value for the file.

// Files writing and reading
// you can use io.Copy function to move data into or out of a file. however to gain more control over logic that wirtes and
// read data, we can do otherwise, i.e. use WriteString method from os.File variable.

// Standard input, output and error
// os packages includes three pre-declared variables, os.Stdin, os.Stdout, and os.Stderr that represent file handles for
// standard input, output and error of the OS respectively.

func main() {
	strR := alphaReaderR("Hello! Where are you?")
	io.Copy(os.Stdout, &strR) // copies stream of bytes emitted by the alphaReader variable into writer interface
	fmt.Println()

	str := strings.NewReader("Hello! Where are you?")
	alpha := NewAlphaReader(str)
	io.Copy(os.Stdout, alpha)
	fmt.Println()

	// Chaining readers
	file, _ := os.Open("./parallelism.go")
	alphaC := NewAlphaReader(file)
	io.Copy(os.Stdout, alphaC)
	fmt.Println()

	// The io.Writer interface
	cw := NewChannelWriter()
	go func() {
		fmt.Fprint(cw, "Steam me!")
	}()
	for c := range cw.Channel {
		fmt.Printf("%c\t", c)
	}

	// content of a file is serialized over a channel using channelWriter. we use io.File value and io.Copy function
	// instead of fmt.Fprint func.
	cw = NewChannelWriter()
	file, err := os.Open("./parallelism.go")
	if err != nil {
		fmt.Println("Error reading file:", err)
		os.Exit(1)

	}

	_, err = io.Copy(cw, file)
	if err != nil {
		fmt.Println("Error copying", err)
		os.Exit(1)
	}

	// consume channel
	for c := range cw.Channel {
		fmt.Printf("%c", c)
	}

	// Working with the io package
	// io.Copy
	data := strings.NewReader(" Write it down.")
	fileIO, err := os.Create("./iocopy.data") // create file.
	if err != nil {
		fmt.Println("Unablbe to create file:", err)
		os.Exit(1)
	}
	io.Copy(fileIO, data) // copy data into created file.

	// PipeReader / PipeWriter -> simple pipe that writes a string to the writer pw. data is conusmed wih pr reader
	// and copied to file

	filePP, err := os.Create("./iopipe.data")
	if err != nil {
		fmt.Println("Unablbe to create file:", err)
		os.Exit(1)
	}
	pr, pw := io.Pipe()
	go func() { // in go routine to avoid deadlocks
		fmt.Fprint(pw, "Pipe streaming")
		pw.Close()
	}()
	wait := make(chan struct{})
	go func() { // in go routine to avoid deadlocks
		io.Copy(filePP, pr)
		pr.Close()
		close(wait)
	}()
	<-wait // wait for pr to finish

	// io.TeeReader --> calculating the SHA-1 has of a file content using TeeReader, data is then streamed to gzip write zip.
	fin, err := os.Open("./parallelism.go") // open file and read content
	if err != nil {
		fmt.Println("unable o open file:", err)
		os.Exit(1)
	}
	defer fin.Close()
	fout, err := os.Create("./teereader.gz") // create an empty zip file
	if err != nil {
		fmt.Println("Unable to create file:", err)
	}
	defer fout.Close()
	zip := gzip.NewWriter(fout) // new write to write into fout zip file creaetd
	defer zip.Close()
	sha := sha1.New()                          // computes a new hash
	dataTR := io.TeeReader(fin, sha)           // calculate the hash of the fin
	io.Copy(zip, dataTR)                       // copy data into zip file.
	fmt.Printf("SHA1 hash %x\n", sha.Sum(nil)) // print hash

	// to calculate both SHA-1 and MD5, we unest two TeeReaders
	sha2 := sha1.New()
	md := md5.New()
	dataTR2 := io.TeeReader(io.TeeReader(fin, md), sha2)
	io.Copy(zip, dataTR2)
	fmt.Printf("SHA1-2 hash %x\n", sha2.Sum(nil))
	fmt.Printf("md5 hash %x\n", md.Sum(nil))

	// io.WriteString
	foutWS, err := os.Create("./iowritestr.data")
	if err != nil {
		fmt.Println("Unable to create file:", err)
		os.Exit(1)
	}
	defer foutWS.Close()
	io.WriteString(foutWS, "Hello there!\n")

	// io.LimitedReader
	strIO := strings.NewReader("The quick brown " + "fox jumps over the lazy dog")
	limited := &io.LimitedReader{R: strIO, N: 19}
	io.Copy(os.Stdout, limited)
	fmt.Println("\t")

	// io.SectionReader
	section := io.NewSectionReader(strIO, 19, 23)
	io.Copy(os.Stdout, section)

	// Creating and opening files
	f1, err := os.Open("./parallelism.go") //open file
	if err != nil {
		fmt.Println("Unable to open file:", err)
		os.Exit(1)
	}
	defer f1.Close()

	f2, err := os.Create("./file0.bkp") // create file
	if err != nil {
		fmt.Println("unable to create file:", err)
		os.Exit(1)
	}
	defer f2.Close()

	n, err := io.Copy(f2, f1) // copy file and return number of bytes written
	if err != nil {
		fmt.Println("Failed to copy:", err)
		os.Exit(1)
	}
	fmt.Println()
	fmt.Printf("Copied %d bytes from %s to %s\n", n, f1.Name(), f2.Name())

	// Function os.OpenFile
	f3, err := os.OpenFile("./parallelism.go", os.O_RDONLY, 0666)
	if err != nil {
		fmt.Println("unable to open file:", err)
	}
	defer f3.Close()

	f4, err := os.OpenFile("./file0.bkp", os.O_WRONLY, 0666)
	if err != nil {
		fmt.Println("unable to open file:", err)
		os.Exit(1)
	}
	defer f4.Close()

	nN, err := io.Copy(f4, f3)
	if err != nil {
		fmt.Println("Failed to copy:", err)
		os.Exit(1)
	}
	fmt.Println()
	fmt.Printf("Copied %d bytes from %s to %s\n", nN, f3.Name(), f4.Name())

	// Files writing and reading
	rows := []string{
		"The quick brown fox",
		"jump over the lazy dog",
	}

	foutWR, err := os.Create("./filewrite.data")
	if err != nil {
		fmt.Println("Failed to copy:", err)
		os.Exit(1)
	}
	defer foutWR.Close()

	for _, row := range rows {
		foutWR.WriteString(row)
	}
	fmt.Println("Done")

	// if data is not text as above, you can write raw bytes directly to a file
	dataR := [][]byte{
		[]byte("The quick brown fox now\n"),
		[]byte("jumps over the lazy dog\n"),
	}

	foutR, err := os.Create("./filewrite.data")
	if err != nil {
		fmt.Println("Failed to copy:", err)
		os.Exit(1)
	}
	defer foutR.Close()

	for _, out := range dataR {
		foutR.Write(out)
	}
	fmt.Println("Done")

	// an io.Reader, reading from the io.File type directly can be done using the Read method. This give access to the content
	// of the file as a raw sram of byte slices.
	fiN, err := os.Open("./dict2.txt")
	if err != nil {
		fmt.Println("Failed to copy:", err)
		os.Exit(1)
	}
	defer fiN.Close()

	p := make([]byte, 1024)

	for {
		n, err := fiN.Read(p)
		if err == io.EOF {
			break
		}
		fmt.Println(string(p[:n]))
	}

	// Standard input, output and error
	f5, err := os.Open("./parallelism.go")
	if err != nil {
		fmt.Println("Unable to open file:", err)
		os.Exit(1)
	}
	defer f5.Close()

	nNN, err := io.Copy(os.Stdout, f5)
	if err != nil {
		fmt.Println("Failed to copy:", err)
		os.Exit(1)
	}
	fmt.Printf("Copied %d bytes from %s \n", nNN, f5.Name())
}
