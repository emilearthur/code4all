package main

import (
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
	src io.Reader
}

// NewAlphaReader implmentation
func NewAlphaReader(source io.Reader) *alphaReader {
	return &alphaReader{source}
}

func (a *alphaReader) Read(p []byte) (int, error) {
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

func main() {
	strR := alphaReaderR("Hello! Where are you?")
	io.Copy(os.Stdout, &strR) // copies stream of bytes emitted by the alphaReader variable into writer interface
	fmt.Println()

	str := strings.NewReader("Hello! Where are you?")
	alpha := NewAlphaReader(str)
	io.Copy(os.Stdout, alpha)
	fmt.Println()

}
