package main

import (
	"fmt"
	"strings"
	"time"
)

// Goroutines
// goroutines allows a program to launch a function (routine) to execute independently from its calling function. goroutines are
// lightweight execution contexts that are multiplexed among a small number OS-backed threads and scheduled by Go's runtime
// scheduler. this makes creating goroutine check to create without the overhead requirements of true kernel threads.

// The go statement
// goroutines are launched using the go statement --> go <function or expression>
// in the example below both main and count will be executed concurrently. main function will execute before the count function.

func count(start, stop, delta int) {
	for i := start; i <= stop; i += delta {
		fmt.Println(i)
	}
}

// Goroutine scheduling
// go runtime scheduler uses a from of coperative schduling to schedule goroutines. By default, the schedular will allow a running
// goroutine to execute to completition. However, the scheduler will auto yield to another goroutine for execution if one of the
// 4 occurs: 1. a go statment encountered in the executing goroutine 2. A channel operation is encountered 3. A blocking systems
// call (file or network IO for instance) is encountered 4. After the completion of a garbage collection cycle.
// the schedule will schedule a queued goroutine ready to enter execution when one of the previous events is encounted in a running
// goroutine. note that scheduler makes no guarantee of the order of execution of goroutines.

// Channels
// go uses channels as a conduit between running goroutines to communicate and share data.

// The Channel type
// the channel type declares a conduit within which only values of a given element type may be sent or recieved by the channel.
// chan keyword is used to specify a channel type as --> chan <element type>

// The send and receieve operations
// go uses the <-(arrow) operator to indicate data movement within a channel
// example				--> operation 	--> Description
// intCh <- 12 			--> Send 		--> when arrow is palce to left of the value, varialbe or expression, it indicate send
//										operation to the channel it points to. 12 is sent into channel intCh
// value := <- intCh 	--> Receive 	--> when arrow is palce to left of the channel, it indicate a receieve operation from
//										 	the channel it points to. the value variable is assigned the value received from the
//											intCh channel.

// An uninitialized channel has a nil zero value and must be initialized using the built-in make function. a channel can be
// initialized as either unbuffered or buffered, depending on its capacity.

// Unbuffered channel
// when the make function is invoked without the capacity args, it returns a bidirectional unbuffered channel.
// how unbuffered channel works:
// i. if the channel is empty, the receiver blocks until there is data ii. the sender can send only to an empty channel
// and blocks until the next receieve operation iii. when the channel has data, the receiver can proceed to receieve the data.
// sending to an unbuffered channel can easily cause a deadlock if the operation is not wrapped in a goroutine.

// Buffered channel
// when make function uses the capacity args, it return a bidirectional buffered channel
// the buffered channel operates as a FIFO blocking queue. the buffered channel has the following characteristics.
// i. when the channel is empty, the receiver blocks until there is at least one element ii. the sender always succeed as long
// as the channel is not at capacity iii. when the channel is at capacity, the sender blocks until at least one element receieved.
// using buffereed channel, it is possible to send and receive values within the same goroutine without causing a deadlock.

// Unidirectional channels
// at declaration, a channel type may also include unidirectional operator (<-) to indicate whether a channel is send-only or
// receive-only
// declaration 				-->  Operation
// <-chan<element type>		Declares a receieve-only channel. var inCh chan<- int
// chan <-<element type> 	Declares a send-only channel. var outCh <-chan int

// function makeEvenNums with a send-only channel ags of type chan <- int
func makeEvenNums(count int, in chan<- int) {
	for i := 0; i < count; i++ {
		in <- 2 * i
	}
}

// Channel length and capacity
// the len and cap function can be used to return a channel's length and capacity. the len function return current number of
// element queued in the channel prior to be read by a receiver. the capacity of the channel remins constant throught the life
// of the channel. An unbuffered channel has a length and a capacity of 0.

// Closing a channel
// once a channel is initialized it is ready for send and receieve operations. A channel will remain in that open state until
// it is forcibly closed using the built-in close function. once a channel is closed, it has the following properties;
// 1. Subsequent send operations will cause a program to panic 2. Receieve operations never block (regardlesss of whether buffered
// or unbuffered) 3. All receive operations return the zero value of teh channel's element type.
// go offers a ong form of receive operation that returns the value read from the channel followed by a boolean indicating the
// closed status of the channel.

// Writing concurrent programs
// the true power of channels and goroutines are realized when they are combined to create concurrent programs.

// Synchronization
// one primary uses of channels is synchronization between running goroutine.

// Streaming data
// a natural use of channels is to stream data from one goroutine to another. this pattern is quite common and it must follow the
// following to work 1. Continuously send data on a channel 2. Continuousy receieve the incoming data from that channel
// 3. signal the end of the stream so the receiver may stop.

// Generator functions
// channels and goroutine provide a natural substrate for implementation of producer/producer pattern using generator functions.
/// in this approach, a goroutine is wrapped in a function which generates values that are sent via a channel returned by the
// function. the consumer goroutine receives these values as they are generated.

// generator function that produces data
func wordsg(data []string) <-chan string {
	out := make(chan string)
	go func() {
		defer close(out) // closes channel upon fn return
		for _, line := range data {
			words := strings.Split(line, " ")
			for _, word := range words {
				word = strings.ToLower(word)
				out <- word
			}
		}
	}()
	return out
}

// the generator function declared func word return a receive only channel of string elements. the consumer function , in the
// instance main() receieves the data emitted byt eh generator function, which is processed using a for...rnage loop.

// Selecting form multiple channels
// sometimes it is necessary for concurrent program to handle send and receieve operations for multiple channels at the same time
// to facilitate such endeavor,the go language supports the select statment that multiplexes selection among multiple send and
// receieve operations:
// select {
//case<send_or_receieve_expression>:
//default:
//}
// the case statment operate similarly to a switch statment with case clauses. the select statment, however selects one of the
// send or receive cases which succeded. if two or more communcation cases happen to be ready at the same time, one will be
// selected at random. the default case is always selected when no other cases succeed.
// the code below use the select statement. the generator word select between two channels out to send data as before and a new
// channel stopCh passed as a parameter, which is used to detect an interruption signal to stop sending data.

// generator function that produces data
func wordsG(stopCh chan struct{}, data []string) <-chan string {
	out := make(chan string)
	go func() {
		defer close(out) // closes channel  upon function return
		for _, line := range data {
			words := strings.Split(line, " ")
			for _, word := range words {
				word = strings.ToLower(word)
				select {
				case out <- word:
				case <-stopCh: // succeeds first when close
					return
				}
			}
		}

	}()
	return out
}

// Channel timeout
// with go concurrency the use of select statement can be implmented wih timeouts. this works byusing the statment to wait for
// a channel operation to succeed withint a give time duration using the API from the time package.

func main() {
	go count(10, 50, 10)
	go count(60, 100, 10)
	go count(110, 200, 20)
	// fmt.Scanln() // blocks for keyboard input inputs
	// goroutines may also be defined as function literals directly in go statement
	go func() {
		count(40, 60, 10)
	}()
	// using function literal
	start := 0
	stop := 50
	step := 5

	go func() {
		count(start, stop, step)
	}() // code is safe as far as values does not change after goroutine starts. if value update outsideit cause race condition.

	// goroutine closure captures variable in a loop
	starts := []int{10, 40, 70, 100}
	for _, j := range starts {
		go func() {
			count(j, j+20, 10)
		}() // since j is updated with each iteration, it is impossible to determine the will to be read by the closure.
		// in most cases goroutine closure will see the last updated value of j by the time they are executed.
	}
	// fixing the code above by passing the variable as a parameter in function literal
	for _, j := range starts {
		go func(s int) {
			count(s, s+20, 10)
		}(j) // here, goroutine closure, invoked with each loop iteration receive a copy of the j variable via func parameter.
	}

	// The Channel type
	// var ch chan int

	// Unbuffered channel
	ch := make(chan int) // unbuffered channel
	//ch <- 12             // blocks
	//fmt.Println(<-ch) // this causes deadblock
	go func() { ch <- 12 }()
	fmt.Println(<-ch)

	// buffered channel
	chi := make(chan int, 4) // buffered channel
	chi <- 2
	chi <- 4
	chi <- 6
	chi <- 8
	// chi <- 8 // adding this will cause a deadlck

	fmt.Println(<-chi)
	fmt.Println(<-chi)
	fmt.Println(<-chi)
	fmt.Println(<-chi)

	// Unidirectional channels
	ch = make(chan int, 10)
	makeEvenNums(4, ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)

	// Channel length and capacity
	ch = make(chan int, 10)
	makeEvenNums(4, ch)
	fmt.Println(len(ch), cap(ch))

	// Closing a channel
	ch <- 20 // adding to the channel
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	close(ch)
	fmt.Println("channel closed")
	// ch <- 19 // cause panic since channel is closed.
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch) // closed, returns zero value for element

	// receieving operation to indicate if channel I opened or closed.
	fmt.Println("new")
	ch = make(chan int, 10)
	makeEvenNums(5, ch)
	close(ch)

	for i := 0; i <= len(ch); i++ {
		if val, opened := <-ch; opened {
			fmt.Println(val)
		} else {
			fmt.Println("Channel closed")
		}
	}

	// Synchronization
	// this program reads the word from the data slice then on a seperate goroutine, collects the occurance of each word.
	data := []string{
		"The yellow fish swims slowly in the water",
		"The brown dog barks loudly after a drink ...",
		"The dark bird brid of prey lands on a small ...",
	}

	histogramS := make(map[string]int)

	done := make(chan bool) // create channel

	// splits and counts words
	go func() {
		for _, line := range data { // iterating throgh data
			words := strings.Split(line, " ")
			for _, word := range words { // iterating throgh word
				word = strings.ToLower(word)
				histogramS[word]++
			}
		}
		done <- true // synchronize with the goroutine. causes wait. unblock after e
	}()

	// if <-done {
	// 	for k, v := range histogramS {
	// 		fmt.Printf("%s\t(%d)\n", k, v)
	// 	}
	// }

	// rewritting the function above since the previous functino has a bug that causes racing condition
	histogramSI := make(map[string]int)
	done2 := make(chan struct{}) // channel declared. Empty struct{} type stores no vlaue and it is used strictly for signaling.
	// this version of code closes the done channel(instead of sending a value). This has effect on allowing the main goroutine
	// to unblock and continue execution

	// splits and counts words
	go func() {
		defer close(done2)          // closes channel upon fn return. when channel is close, all receivers succeed without blocking
		for _, line := range data { // iterating throgh data
			words := strings.Split(line, " ")
			for _, word := range words { // iterating throgh word
				word = strings.ToLower(word)
				histogramSI[word]++
			}
		}
	}()

	<-done2 // blocks until closed

	// for k, v := range histogramSI {
	// 	fmt.Printf("%s\t(%d)\n", k, v)
	// }

	// use single channel to stream data from one goroutine to another. Using signaling device to indicate the end of stream
	histogram := make(map[string]int)
	wordsCh := make(chan string) // channel used to stream data

	// splits line and sends words to channel
	go func() {
		defer close(wordsCh) // close channel when done.signal receiver that it should stop
		for _, line := range data {
			words := strings.Split(line, " ")
			for _, word := range words {
				word = strings.ToLower(word)
				wordsCh <- word // sender goroutine loops through the text line and sends a word at a time. it then blocks until
				// the word is received by the receiving (main) goroutine.
			}
		}
	}()

	// proces word stream and count words
	// loop  until wordsCh is closed
	// for {
	// 	word, opened := <-wordsCh // pulls data from the channel
	// 	if !opened {              // checks if status of chanel is open
	// 		break // breaks if closed
	// 	}
	// 	histogram[word]++ // other wise records histogram
	// }

	// for k, v := range histogram {
	// 	fmt.Printf("%s\t(%d)\n", k, v)
	// }

	// Using for...range to receive data
	// for <element> := range<channel>{...}

	for wordg := range wordsCh { // emits the receieved value from the wordsCh channel. when channel is closed,
		// the loop automatically breaks.
		histogram[wordg]++
	}

	// for k, v := range histogram {
	// 	fmt.Printf("%s\t(%d)\n", k, v)
	// }

	// Generator functions
	histogramG := make(map[string]int)

	words := wordsg(data) // return handle to data channel
	for word := range words {
		histogramG[word]++
	}
	// for k, v := range histogramG {
	// 	fmt.Printf("%s\t(%d)\n", k, v)
	// }

	// Selecting form multiple channels
	histogramgg := make(map[string]int)
	stopCh := make(chan struct{}) // used to signal stop

	wordsGG := wordsG(stopCh, data) // return handle to channel
	for word := range wordsGG {
		if histogramgg["the"] == 3 {
			close(stopCh) // cause panic if another "the" is found
		}
		histogramgg[word]++
	}

	// Channel timeout
	// the program elow, histogram eg. timesout if the program takes longer than 200 microseconds to out and print words.
	histogramTO := make(map[string]int)
	doneTO := make(chan struct{})

	go func() {
		defer close(doneTO)
		words := wordsg(data) // returns handle to channel
		for word := range words {
			histogramTO[word]++
		}
		for k, v := range histogramTO {
			fmt.Printf("%s\t(%d)\n", k, v)
		}

	}()

	select {
	case <-doneTO: // blocks util goroutine closes the done changel
		fmt.Println("Done counting words!!!")
	case <-time.After(200 * time.Microsecond):
		fmt.Println("Sorry, took too long to count.")
	}

}
