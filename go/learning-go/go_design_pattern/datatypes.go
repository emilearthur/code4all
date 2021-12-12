package main

import (
	"fmt"
	"math"
	"time"
)

// var name, desc string
// var radius int32
// var mass float64
// var active bool
// var satellites []string

// intitalization declaration
// var name, desc string = "Earth", "Planet"
// var radius int32 = 6378
// var mass float64 = 1.989e+30
// var active bool = true
// var satellites = []string{
// 	"Moon",
// }

// declaring constant - tpyed
const prod, dev, test string = "PROD", "DEV", "TESTS"

// variable declaration block
var (
	// intitalization declaration
	name, desc string  = "Earth", "Planet"
	radius     int32   = 6378
	mass       float64 = 1.989e+30
	active     bool    = true
	satellites         = []string{
		"Moon"}
)

// constant declaration block
const (
	// initialization block
	key, value string        = "key", "value"
	testEnv    bool          = false
	startTime  time.Duration = time.Second
	endTime    time.Duration = 4 * time.Second
	Brink      rune          = 'G'
	piHat      float64       = math.Pi * 2.0e+3
)

func main() {
	// name = "Sun"
	// desc = "Star"
	// radius = 685800
	// mass = 1.989e+30
	// active = true
	// satellites = []string{
	// 	"Mercury",
	// 	"Venus",
	// 	"Earth",
	// 	"Mars",z
	// 	"Juputer",
	// 	"Saturn",
	// 	"Uranus",
	// 	"Neptune",
	// }

	// short  varaiable declaration
	name := "Neptune"
	desc := "Planet"
	radius := 24764
	mass := 1.024e26
	active := true
	satellites := []string{
		"Naiad", "Thalassa", "Despina", "Galatea", "Larissa", "S/2004 N 1",
		"Proteus", "Triton", "Nereid", "Halimede", "Sao", "Laomedeia", "Neso", "Psamathe",
	}

	fmt.Println(name)
	fmt.Println(desc)
	fmt.Println(active)
	fmt.Println("Radius (km)", radius)
	fmt.Println("Mass (kg)", mass)
	fmt.Println("Satellites", satellites)
	fmt.Println(prod)
	fmt.Println(dev)
	fmt.Println(test)

}
