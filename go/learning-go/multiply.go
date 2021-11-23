package main

import "fmt"

// function to add two numbers
func addTwoNumbers(x, y int) int {
	sum := x + y
	return sum
}

// function to multiply two numbers
func multiplyTwoNumbers(x, y int) int {
	product := x * y
	return product
}

func main() {
	/*
		Here we commenting out the addTwoNumbers function because it is failing. thus
		we use multiply only.

		a := addTwoNumbers(3,5)
		fmt.Println(a)

	*/
	m := multiplyTwoNumbers(5, 9)
	fmt.Println(m)
}
