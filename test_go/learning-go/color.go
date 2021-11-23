package main

import "fmt"

const favColor string = "blue"

func main() {
	var guess string
	// create an input loop
	for {
		// ask user to guess fav color
		fmt.Println("Guess my favorite color:")
		// try read a line from input from the user. print out the error 0
		if _, err := fmt.Scanln(&guess); err != nil {
			return
		}
		// did they guess the correct color?
		if favColor == guess {
			// they guessed it!
			fmt.Printf("%q is my fav color!\n", favColor)
			return // return statement here terminates the program afterwards.
		}
		// wrong! have them guess again
		fmt.Printf("sorry, %q is not my favorite color. Guess again.\n", guess)
	}
}
