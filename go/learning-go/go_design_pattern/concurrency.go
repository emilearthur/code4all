// Caculates sum of all multiple of 3 and 5 less than MAX value.

package main

import (
	"fmt"
)

// MAX value
const MAX = 1000

func main() {
	work := make(chan int, MAX)
	result := make(chan int)

	// 1. Create channel of multiple 3 and 5 concurrently using goroutine
	go func() {
		for i := 1; i < MAX; i++ {
			if (i%3) == 0 || (i%5) == 0 {
				work <- i // push for work
			}
		}
		close(work)
	}()
	// 2.  Concurrently sum up work and put results in channel results
	go func() {
		r := 0
		for i := range work {
			r = r + i
		}
		result <- r
	}()
	// 3. Wait for result, then print
	fmt.Println("Total:", <-result)

}
