package main

import (
	"bufio"
	"bytes"
	"encoding/gob"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

// Buffered IO
// most IO  operation convered are unbuffered -- i.e. each read and write operation could negatively impacted by the latency of
// the underlying os to handle io reuquests. Buffered operation reduces latency by buffering data in the internal memory during
// IO operations. bufio package offers buffered read and write IO operations.
// in general, the constructor functions in the bufio package create a buffered write by wrapping an existing io.Writer as it
// underlying source.

// Scanning the buffer
// bufio package also make avaialable primitivs that are used to scan and tokeniz buffered input data from an io.Reader source.
// The bufio.Scanner type scans inputs data using the Split method to define tokenization strategies.

// In-memory IO
// the bytes pakage offeres common primitives to achieve streaming IO on blocks of bytes, stored in memory, represented by the
// bytes.Buffer type. Since the bytes.Buffer type implements both io.Reader and io.Writer interfaces it is great option to stream
// data into or out of memeory using streaming IO primitives.

// Encoding and decoding data
// common aspect of IO in Go is the encoding of data from one representation to another as it is being streamed. The encoder and
// decorder of the standard library /encoding, use the io.Reader and io.Writer interfaces to leverage IO primitives as a way of
// streaming data during encoding and decording. the decoding processs does reverse by streaming the gob-encoded binary data using
// an io.Reader and automatically reconstructing it as a strongly-typed Go value.

// Name object
type Name struct {
	First, Last string
}

// Book object
type Book struct {
	Title       string
	PageCount   int
	ISBN        string
	Authors     []Name
	Publisher   string
	PublishDate time.Time
}

// Binary encoding with gob
// gob package provides an encoding format that can eb used to convert complex go data types into binary. Gob is self-describing
// (i.e. each encoded data item is accompanied by a type description). the encoding process involves straming the gob-encoded data
// to an io.Wrtie so it can written to a resource for future consumption.

// Encoding data as JSON
// encoding package comes with a json encoder sub-package to support JSON-formatted data. JSON encoding works similarly as the encoder
// and decoder from the glob package. the difference is that the generated data takes the form of a clear text JSON-encoded format
// instead of a binary.

// Controlling JSON mapping with struct tags
// by default, the name of a struct filed is used as the key for the generated JSON object. This can be controlled using struct
// type tags to specify how JSON object key name are are mapped during encoding and decoding for the data.

// BookC object
type BookC struct {
	Title       string    `json:"book_title"`      // maps the Title struct field to the JSON object key book_title
	PageCount   int       `json:"pages,string"`    // mpas the PageCount struct field to the JSON oject key pages and outputs value as string isntead of number.
	ISBN        string    `json:"-"`               // - caused the ISDN field to be skipped during encoding and decoding
	Authors     []Name    `json:"auths,omniempty"` // maps the Authors field to the JSON object key auths. the annotation, omniempty causes the field to be ommited if it value is nil
	Publisher   string    `json:",omniempty"`      // maps the struct field name, Publisher as the JSON object key name. omniempty causes the field to be ommited if it value is nil or empty
	PublishDate time.Time `json:"pub_date"`        // mapes the field name PublishDate to the JSON objecy key pub_date
}

// Custom encoding and decoding
// the JSON package uses two interfaces, Marshaler and Unmarshaler, to hook into encoding and decoding events
// respectively. when the encoder encouters a value whose type implements a json.Marshaler, it delegates
// serialization of teh value to the method MarshalJSON defined in the Marshaller interface.
// eg below type NameM is update to implment json.Marshaller

// NameM object
type NameM struct {
	First, Last string
}

// MarshalJSON function -- update name type with JSON Marshal
func (n *NameM) MarshalJSON() ([]byte, error) {
	return []byte(
		fmt.Sprintf("\"%s, %s\"", n.Last, n.First),
	), nil
}

// UnmarshalJSON function -- decodes input and puts them into first name and last name.
func (n *NameM) UnmarshalJSON(data []byte) error {
	var name string
	err := json.Unmarshal(data, &name)
	if err != nil {
		fmt.Println(err)
		return err
	}
	parts := strings.Split(name, ", ")
	n.Last, n.First = parts[0], parts[1]
	return nil
}

// BookM object
type BookM struct {
	Title       string
	PageCount   int
	ISBN        string
	Authors     []NameM
	Publisher   string
	PublishDate time.Time
}

func main() {
	rows := []string{
		"The quick brown fox",
		"jumps over the lazy sheep",
	}

	// Scanning the buffer
	// buffer writer
	fout, err := os.Create("./filewritess.data")
	writer := bufio.NewWriter(fout)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer fout.Close()

	var count int
	for _, row := range rows {
		nbyte, err := writer.WriteString(row)
		if err != nil {
			fmt.Println("Unable to write data", err)
			os.Exit(1)
		}
		count += nbyte
	}
	writer.Flush()
	fmt.Println(count)
	fmt.Print("\n")

	// buffer reader
	file, err := os.Open("./strongtyped.go") // open file
	if err != nil {
		fmt.Println("Unable to open file:", err)
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file) //  wrap file around buffer
	for {
		line, err := reader.ReadString('\n') // read file using the '\n' character as the content delimter.
		if err != nil {
			if err == io.EOF {
				break
			} else {
				fmt.Println("Error reading:", err)
				return
			}
		}
		fmt.Print(line)
	}

	// Scanning the buffer
	fileS, err := os.Open("./planets.txt") // open file
	if err != nil {
		fmt.Println("Unable to open file:", err)
		return
	}

	defer fileS.Close()
	fmt.Printf("%-10s %-10s %-6s %-6s\n", "Planet", "Diameter", "Moons", "Rings?")
	scanner := bufio.NewScanner(fileS) // wrap file to NewScanner constructor
	scanner.Split(bufio.ScanLines)     // setting split for the scanner. content tokenized
	for scanner.Scan() {               // tranversing through the scanner for the next token
		fields := strings.Split(scanner.Text(), " ") // reading token data with scanner.Text method.
		fmt.Printf("%-10s %-10s %06s %-6s\n", fields[0], fields[1], fields[2], fields[3])
	}

	// In-memory IO
	// code below stores several string values in the byte.Buffer variable book. Then the buffer is streamed to os.Stdout
	var books bytes.Buffer
	books.WriteString("The Great Gatsby \n")
	books.WriteString("1984 \n")
	books.WriteString("A Tale of Two Cities \n")
	books.WriteString("Les Miserable \n")
	books.WriteString("The call of the Wild \n")

	// books.WriteTo(os.Stdout) // writing to stdout interface.
	fileOut, err := os.Create("./books.txt")
	if err != nil {
		fmt.Println("Unable to create file:", err)
		return
	}
	defer fileOut.Close()
	books.WriteTo(fileOut)

	// Encoding and decoding data
	// Binary encoding with gob
	bookEnc := []Book{
		{
			Title:       "Learning Go",
			PageCount:   375,
			ISBN:        "9781784395438",
			Authors:     []Name{{"Vladimir", "Vivien"}},
			Publisher:   "Packt",
			PublishDate: time.Date(2016, time.July, 0, 0, 0, 0, 0, time.UTC),
		},
		{
			Title:     "The Go Programming Language",
			PageCount: 380,
			ISBN:      "9780134190440",
			Authors: []Name{{"Alan", "Donavan"},
				{"Brain", "Kernighan"}},
			Publisher:   "Addison-Wesley",
			PublishDate: time.Date(2015, time.October, 26, 0, 0, 0, 0, time.UTC),
		},
		{
			Title:       "Introducing Go",
			PageCount:   124,
			ISBN:        "978-1491941959",
			Authors:     []Name{{"Caleb", "Doxsey"}},
			Publisher:   "O'Reilly",
			PublishDate: time.Date(2016, time.January, 0, 0, 0, 0, 0, time.UTC),
		},
	}

	// serialize data structure to file
	fileSOut, err := os.Create("book.dat")
	if err != nil {
		fmt.Print("Unable to create file", err)
		return
	}
	defer fileSOut.Close()
	// glob encoder created.
	enc := gob.NewEncoder(fileSOut)
	// notes: If with assignment used here. ==> if assignment
	// encoding data. this streams the encoded data into fileSOut
	if err := enc.Encode(bookEnc); err != nil {
		fmt.Println("Error occurred during Encoding", err)
		return
	}
	// could be code below.
	// err = enc.Encode(bookEnc)
	// if err != nil {
	// 	fmt.Println("Error occurred during Encoding", err)
	// }

	// Binary encoding with gob
	fileEnc, err := os.Open("book.dat")
	if err != nil {
		fmt.Println("Unable to open file:", err)
		return
	}
	defer fileEnc.Close()

	var bookDec []Book
	//  glob decoder
	dec := gob.NewDecoder(fileEnc)
	if err := dec.Decode(&bookDec); err != nil {
		fmt.Println("Error occurred during Decoding", err)
		return
	}
	fmt.Println(bookDec)

	// Encoding data as JSON
	fileJSONENC, err := os.Create("books.dat")
	if err != nil {
		fmt.Println("Unable to Create file:", err)
		return
	}
	defer fileJSONENC.Close()
	encJSON := json.NewEncoder(fileJSONENC)
	if err := encJSON.Encode(bookEnc); err != nil {
		fmt.Println("Error occurred during Encoding", err)
	}

	// Decoding data as JSON
	fileJSONDEC, err := os.Open("books.dat")
	if err != nil {
		fmt.Println("Unable to Opening file:", err)
		return
	}
	defer fileJSONDEC.Close()

	var booksJSON []Book
	decJSON := json.NewDecoder(fileJSONDEC)
	if err := decJSON.Decode(&booksJSON); err != nil {
		fmt.Println("Error Decoding file:", err)
		return
	}
	fmt.Println(booksJSON)

	// Encoding data as JSON usging bookC
	bookEncN := []BookC{
		{
			Title:       "Learning Go",
			PageCount:   375,
			ISBN:        "9781784395438",
			Authors:     []Name{{"Vladimir", "Vivien"}},
			Publisher:   "Packt",
			PublishDate: time.Date(2016, time.July, 0, 0, 0, 0, 0, time.UTC),
		},
		{
			Title:     "The Go Programming Language",
			PageCount: 380,
			ISBN:      "9780134190440",
			Authors: []Name{{"Alan", "Donavan"},
				{"Brain", "Kernighan"}},
			Publisher:   "Addison-Wesley",
			PublishDate: time.Date(2015, time.October, 26, 0, 0, 0, 0, time.UTC),
		},
		{
			Title:       "Introducing Go",
			PageCount:   124,
			ISBN:        "978-1491941959",
			Authors:     []Name{{"Caleb", "Doxsey"}},
			Publisher:   "O'Reilly",
			PublishDate: time.Date(2016, time.January, 0, 0, 0, 0, 0, time.UTC),
		},
	}

	fileJSONN, err := os.Create("bookss.dat")
	if err != nil {
		fmt.Println("Unable to Create file:", err)
		return
	}
	defer fileJSONENC.Close()
	encJSONN := json.NewEncoder(fileJSONN)
	if err := encJSONN.Encode(bookEncN); err != nil {
		fmt.Println("Error occurred during Encoding", err)
	}

	// Custom encoding and decoding
	booksM := []BookM{
		{
			Title:       "Learning Go",
			PageCount:   375,
			ISBN:        "9781784395438",
			Authors:     []NameM{{"Vladimir", "Vivien"}},
			Publisher:   "Packt",
			PublishDate: time.Date(2016, time.July, 0, 0, 0, 0, 0, time.UTC),
		},
		{
			Title:     "The Go Programming Language",
			PageCount: 380,
			ISBN:      "9780134190440",
			Authors: []NameM{{"Alan", "Donavan"},
				{"Brain", "Kernighan"}},
			Publisher:   "Addison-Wesley",
			PublishDate: time.Date(2015, time.October, 26, 0, 0, 0, 0, time.UTC),
		},
		{
			Title:       "Introducing Go",
			PageCount:   124,
			ISBN:        "978-1491941959",
			Authors:     []NameM{{"Caleb", "Doxsey"}},
			Publisher:   "O'Reilly",
			PublishDate: time.Date(2016, time.January, 0, 0, 0, 0, 0, time.UTC),
		},
	}

	fileJSONM, err := os.Create("bookM.dat")
	if err != nil {
		fmt.Println("Unable to Create file:", err)
		return
	}
	defer fileJSONM.Close()
	encM := json.NewEncoder(fileJSONM)
	if err := encM.Encode(booksM); err != nil {
		fmt.Println("Error in Encoding \n", err)
	}

	// decoding
	fileJSONMO, err := os.Open("bookM.dat")
	if err != nil {
		fmt.Println(err)
		return
	}

	var booksJSONM []BookM
	decJSONM := json.NewDecoder(fileJSONMO)
	if err := decJSONM.Decode(&booksJSONM); err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println("\n", " ")
	fmt.Println(booksJSONM)

}
