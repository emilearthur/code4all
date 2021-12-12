package main

import "fmt"

func main() {
	planet := struct {
		name     string
		diameter int
	}{"earth", 12742}
	fmt.Printf("%-10s %-10d\n",planet.name, planet.diameter)
}
