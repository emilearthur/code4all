package main

import "fmt"

var x = 5
var count int


func main(){
	for i := 0; i < x; i++ {
		fmt.Println(i)
		count ++
	}
	fmt.Println("Count of object:", count)
}