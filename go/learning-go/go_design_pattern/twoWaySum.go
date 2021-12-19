package main

import "fmt"

// brute force solution
func twoWayBruteForce(list []int, pairSum int) []int {
	n := len(list)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if list[i]+list[j] == pairSum {
				return []int{list[i], list[j]}
			}
		}
	}
	return []int{}
}

// optimal solution
func twoWayOptimal(list []int, pairSum int) []int {
	n := len(list)
	hash := make(map[int]int)

	for i := 0; i < n; i++ {
		complement := pairSum - list[i]
		j, ok := hash[complement]
		if ok {
			return []int{i, j}
		}
		hash[list[i]] = i

	}
	return []int{}
}

func main() {
	list := []int{3, 5, 2, -4, 8, 11}
	pairSum := 7

	output := twoWayBruteForce(list, pairSum)
	fmt.Println(output)

	output2 := twoWayBruteForce(list, pairSum)
	fmt.Println(output2)
}
