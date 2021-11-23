package main

import (
	"fmt"
	"strings"
)

func main() {
	fmt.Println("Please enter your name.")
	var name string                     // declare  string
	fmt.Scanln(&name)                   // fmt.Scanln waits for user inputs ending with new line
	name = strings.TrimSpace(name)      // remove space character
	fmt.Printf("Hi, %s! I'm Go!", name) // fmt.Printf function takes a string and using special printing verbs %s.
}
