package main

import (
	"fmt"
	"sync"
)

// go runtime schedular auto. multiplexes and schedules goroutines across avaiable OS-managed threads. this means concurrent
// programs that can be parallelized have the ability to take advantage of underlying processor cores with little or no
// configuration.

// MAX value in container
const MAX = 1000

const workers = 2

func main() {
	values := make(chan int)
	result := make(chan int, workers)
	var wg sync.WaitGroup

	go func() {
		defer close(values) // close channel after running function
		// gen multiple of 3 & 5 values
		for i := 1; i < MAX; i++ {
			if (i%3) == 0 || (i%5) == 0 {
				values <- i // push downstream
			}
		}
	}()

	work := func() {
		// work unit, calc partial result
		defer wg.Done()
		r := 0
		for i := range values {
			r += i
		}
		result <- r
	}

	wg.Add(workers) // launch workers

	// distribute work to goroutine
	for i := 0; i < workers; i++ {
		go work()
	}

	wg.Wait() // wait for all goroutines
	close(result)

	total := 0

	// gather partials
	for pr := range result {
		total += pr
	}
	fmt.Println("Total:", total)
}
