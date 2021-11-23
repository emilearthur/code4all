package main

import "fmt"

func main() {
	// Define shark var. as a slice of  ==> list
	sharks := []string{"hammerhead", "greate white", "dogfish", "frilled", "dcoktime"}

	// looping  through list shark
	// for _, shark := range(sharks) {  // here the index is not assigned.
	//		fmt.Println(shark)
	for index, shark := range sharks {
		fmt.Println(index, shark)
	}

}
