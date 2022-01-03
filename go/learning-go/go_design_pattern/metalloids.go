package main

import (
	"fmt"
	"strings"
)

const avogardo float64 = 6.022141e+23
const grams float64 = 100.0

// declaring constants for Big Stars. Using iota, subsequent values will be enumerated.
const (
	StarHyperGaint       = 2.0 * iota // results to 0
	StarsuperGaint                    // reuslts to 2 since it enumerating from above.
	StarsuperBrightGaint              // reuslts to 4 since it enumerating from above.
	StarGiant                         // reuslts to 6 since it enumerating from above.
	StarSubGiant                      // reuslts to 8 since it enumerating from above.
)

// declaring constants for Dwarf Stars. subsequent values will be enumerated.
const (
	StarDwarf = iota
	StarSubDwarf
	StarWhiteDwarf
	StarRedDwarf
	StarBrownDwarf
)

// thowing out certain values in enumerate. eg. we skip avalue 0 and 64
const (
	_              = iota      //value 0
	StarHyperGainT = 1 << iota // results to 0
	StarsuperGainT
	StarsuperBrightGainT
	StarGianT
	StarSubGianT
	_ // value 64
	StarDwarF
	StarSubDwarF
	StarWhiteDwarF
	StarRedDwarF
	StarBrownDwarF
)

type amu float64

type metalloid struct {
	name   string
	number int32
	weight amu
}

func (mass amu) float() float64 {
	return float64(mass)
}

var metalloids = []metalloid{
	{"Boron", 5, 10.81},
	{"Silicon", 14, 28.085},
	{"Germanuim", 32, 74.63},
	{"Arsenic", 33, 74.921},
	{"Antimony", 51, 121.760},
	{"Tellerium", 52, 127.60},
	{"Polonium", 84, 209.0},
}

// find # of moles
func moles(mass amu) float64 {
	return float64(grams) / float64(mass)
}

// return # of atoms moles
func atoms(moles float64) float64 {
	return moles * avogardo
}

// return column headers
func headers() string {
	return fmt.Sprintf("%-10s %-10s %-10s Atoms in %.2f Grams\n", "Element", "Number", "AMU", grams)
}

// func main() {
// 	fmt.Print(headers())
// 	for _, m := range metalloids {
// 		fmt.Printf("%-10s %-10d %-10.3f %e\n", m.name, m.number, m.weight.float(), atoms(moles(m.weight)))
// 	}

// }

// interfaces
func (m metalloid) String() string {
	return fmt.Sprintf("%-10s %-10d %-10.3f %e", m.name, m.number, m.weight.float(), atoms(moles(m.weight)))
}

// increment and decrement operator
func reverseprint(s string) {
	for i := len(s) - 1; i >= 0; {
		fmt.Print(string(s[i]))
		i--
	}
}

// reverse function
func reverse(s string) string {
	var revWord []byte
	for i := len(s) - 1; i >= 0; i-- {
		revWord = append(revWord, s[i])
	}
	return strings.ToLower(string(revWord))
}

// determine if string is palindrome or not
func isPalindrome(s string) bool {
	var revWord = reverse(s)
	return strings.ToLower(s) == revWord
}

func main() {
	fmt.Print((headers()))
	for _, m := range metalloids {
		fmt.Print(m, "\n")
	}

	//reverseprint("\nname")
	fmt.Print(isPalindrome("MoMo"), "\n")
	fmt.Print(isPalindrome("Anna"), "\n")
	fmt.Print(isPalindrome("Game"), "\n")

}
