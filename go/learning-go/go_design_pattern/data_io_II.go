package main

import (
	"fmt"
	"io"
	"os"
)

// Formatted IO with fmt
// the most common usage of the fmt package is for writing ot standard output and reading from standard input.

// Printing to io.Writer interfaces
// the fmt package offers several functions designed to write text data to arbitrary implementations of io.Writer.
// the fmt.Fprint and fmt.Fprintln functions write text with default format while fmt.Fprintf supports format specifiers.

type metalloid struct {
	name   string
	number int32
	weight float64
}

// Reading from io.Reader
// the fmt package also support formatted reading of textual data from io.Reader interfaces. the fmt.Fscan and fmt.Fscanln
// functions can be used to read multiple values, seperated by spaces into specified parameters. the fmt.Fscanf function
// supports specifiers for richer and flexible parsing of data input from io.Reader implementation.

// Reading from standard input
// instead of reading from an arbitrary io.Reader, the fmt.Scan, fmt.Scanf, and fmt.Scanln are used to read data from standard
// input file handle, os.Stdin.

func main() {
	var metalloids = []metalloid{
		{"Boron", 5, 10.81},
		{"Silicon", 14, 28.085},
		{"Germanium", 32, 74.63},
		{"Arsenic", 33, 74.921},
		{"Antimony", 51, 121.760},
		{"Tellerium", 52, 127.60},
		{"Polonium", 84, 209.0},
	}
	file, _ := os.Create("./metalloids.txt")
	defer file.Close()

	for _, m := range metalloids {
		fmt.Fprintf(file, "%-10s %-10d %-10.3f\n", m.name, m.number, m.weight) // write same format for file
	}

	// printing standard output
	for _, m := range metalloids {
		fmt.Printf("%-10s %-10d %-10.3f\n", m.name, m.number, m.weight)
	}
	fmt.Println()

	// Reading from io.Reader
	var name, hasRing string
	var diam, moons int

	// read data
	data, err := os.Open("./planets.txt")
	if err != nil {
		fmt.Println("Unable to open file:", err)
		return
	}
	defer data.Close()

	for {
		_, err := fmt.Fscanf(data, "%s %d  %d %s\n", &name, &diam, &moons, &hasRing) // scan data [pointer]
		if err != nil {
			if err == io.EOF {
				break
			} else {
				fmt.Println("Scan error:", err)
				return
			}
		}
		fmt.Printf("%-10s %-10d %-6d %-6s\n", name, diam, moons, hasRing)
	}
	fmt.Println()

	var  choice int
	fmt.Println("A square is what?")
	fmt.Println("Enter 1=quadrilateral 2=rectagonal:")

	n, err := fmt.Scanf("%d", &choice)
	if n != 1 || err != nil {
		fmt.Println("Follow directions!")
		return 
	}
	if choice == 1 {
		fmt.Println("Follow direction!")
	} else {
		fmt.Println("Wrong, Google it.")
	}
}
