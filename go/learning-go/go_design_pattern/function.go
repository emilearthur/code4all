package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	"math"
	"os"
)

// Go function
// In go function are first-class, typed programming elements. A declared function literal always has a type and a value
// (the defined function itself) and can be optionally be bound to a named identifier. Because function can be used as data
// they can be assigned to variables or passed around as parameters of other functions.
// Function declaration --> func [<func-identifier>]([<argument-list>])[(<result-list>)]{...[return][<value or expression list>]}
// The return statement causes the execution flow to exit a function.

func printPi() {
	fmt.Printf("printPi() %v\n", math.Pi) // no return statement
}

func avogadro() float64 {
	return 6.02214129e23
}

func fib(n int) {
	fmt.Printf("fib(%d): [", n)
	var p0, p1 uint64 = 0, 1
	fmt.Printf("%d %d ", p0, p1)
	for i := 2; i <= n; i++ {
		p0, p1 = p1, p0+p1
		fmt.Printf("%d ", p1)
	}
	fmt.Println("]")
}

func isPrime(n int) bool { //type o return value indicated.
	lim := int(math.Sqrt(float64(n)))
	for p := 2; p <= lim; p++ {
		if (p % n) == 0 {
			return false
		}
	}
	return true
}

// the function type

func add(op0 int, op1 int) int {
	return op0 + op1
}

func sub(op0 int, op1 int) int {
	return op0 - op1
}

// Variadic parameters
// last parameter of a function can be declared as variadic (variable length args) by affixing ellipses(...) before
// the parameter's type. This indicates that zero or more values of that type may be passed to the function when it is called.

func avg(nums ...float64) float64 {
	n := len(nums)
	t := 0.0
	for _, v := range nums {
		t += v
	}
	return t / float64(n)
}

func sum(nums ...float64) float64 { //... same as *args in python
	var sum float64 //decalaring type which result to 0.0. Same as sum := 0.0
	for _, v := range nums {
		sum += v
	}
	return sum
}

// function result parameters
func div(op0, op1 int) (int, int) {
	r := op0
	q := 0
	for r >= op1 {
		q++
		r = r - op1
	}
	return q, r

}

// Named results parameters
func divNamed(dvdn, dvsr int) (q, r int) {
	r = dvdn
	for r >= dvsr {
		q++
		r = r - dvsr
	}
	return q, r
}

// Passing parameter values
// in go, all params passed into a function are done so by value. This means a local copy of the passed values is created inside
// the called function. There is no inherent concept of passing parameters values by reference.

func dbl(val float64) {
	val = 2 * val // update params
	fmt.Printf("db1()=%.5f\n", val)
}

// Achieving pass by reference
// Go can achieve pass-by-reference semantics using pointer parameter values. This allows a called function to reach outside of
// its lexical scope and change the value stored at the location referenced by the pointer parameter.

func half(val *float64) {
	fmt.Printf("call half(%f)\n", *val)
	*val = *val / 2 // dereferencing the val pointer and update inplace.
}

// Anonymous functions and closures
// Functions can be written as literals without a named identifier. ==>> anonymous functions and can be assigned to a variable
// to be invoked later.

var (
	mul = func(op0, op1 int) int {
		return op0 * op1
	}

	sqr = func(val int) int {
		return mul(val, val)
	}
)

// Higher-order function
// While types such as struct let programmers abstract data, higher-order functions provide a mechnanism to encapsulate and
// abstract behaviors that can be composed together to form more complex behaviors.

// function accepts a slice of integer and a function as parameter.It applies the specificd function to each element  in the slice.
func apply(nums []int, f func(int) int) func() {
	for i, v := range nums {
		nums[i] = f(v)
	}
	return func() { fmt.Println(nums) }
}

// Error Signaling and Handling
// Go has simplified approach to error signalling and error handling that puts the onus on the programmer to handle possible
// errors immediately after a called function returns. In Go, the traditional way of signaling errors is to return a value of
// type error when something goes wrong during the execution of your function.

// Signaling errors
// anagram program -- groups all words with the same anagram.
// sorts letters in a word (i.e. "morning" -> "gimnnor")
func sortRunes(str string) string {
	runes := bytes.Runes([]byte(str))
	var temp rune
	for i := 0; i < len(runes); i++ {
		for j := i + 1; j < len(runes); j++ {
			if runes[j] < runes[i] {
				temp = runes[i]
				runes[i], runes[j] = runes[j], temp // swap
			}
		}
	}
	return string(runes)
}

// load loads content of file fname into memory as []string
func load(fname string) ([]string, error) {
	if fname == "" {
		return nil, errors.New("Dictionary file name cannot be empty")  // error returned.
	}
	file, err := os.Open(fname)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func main() {
	printPi()

	fmt.Printf("avogardro() = %e 1/mol\n", avogadro())
	fib(1)
	fib(41)

	prime := 37
	fmt.Printf("isPrime(%d) %v\n", prime, isPrime(prime))

	var opAdd func(int, int) int = add
	opSub := sub

	fmt.Printf("add(12,44)=%d\n", opAdd(12, 44))
	fmt.Printf("sub(99,13)=%d\n", opSub(99, 13))

	// Variadic parameters
	fmt.Printf("avg([1, 2.5, 3.75]) = %.2f\n", avg(1, 2.5, 3.75))
	points := []float64{9, 4, 3.7, 7.1, 7.9, 9.2, 10}
	fmt.Printf("sum([9,4,3.7,7.1,7.9, 9.2, 10]) = %.2f\n", sum(points...))
	fmt.Printf("sum([9,4,3.7,7.1,7.9, 9.2, 10]) = %.2f\n", sum(9, 4, 3.7, 7.1, 7.9, 9.2, 10))

	// function result params
	q, r := div(71, 5)
	fmt.Printf("div(71, 5) -> q = %d, r = %d\n", q, r)

	qNamed, rNamed := divNamed(71, 5)
	fmt.Printf("div(71, 5) -> q = %d, r = %d\n", qNamed, rNamed)

	// passing params
	p := math.Pi
	fmt.Printf("before db() p = %.5f\n", p)
	dbl(p)
	fmt.Printf("after db() p = %.5f\n", p) // same as before becuase function recieved local copy of passed parameter

	// passing params
	num := math.Pi
	fmt.Printf("before half num = %.5f\n", num)
	half(&num)
	fmt.Printf("after half num = %.5f\n", num) // half func updates  inplace the orignal value referenced b it num params.

	// Anonymous functions and closures
	fmt.Printf("mul(25,7) = %d\n", mul(25, 7))
	fmt.Printf("sqr(7) = %d\n", sqr(7))

	// Invoking anonymous function literal
	// Anonymous function does not have to be bound to an identifier. The function literal can be evaluated  inplace as an
	// expression that returns the function's results
	fmt.Printf("94 (°F) = %.2f (°C)\n", func(f float64) float64 {
		return (f - 32.0) * (5.0 / 9.0)
	}(94),
	)

	// Closures -- Go function lierals are closures. This means they have lexical visibility to non-local varaibles declared
	// outside of thier enclosing code block.
	for i := 0.0; i < 360.0; i += 45.0 {
		rad := func() float64 { // for each iteration, this closure is formed between the enclosed function literal
			// and outer non-local variable i.
			return i * math.Pi / 180

		}()
		fmt.Printf("%.2f Deg = %.2f Rad\n", i, rad)
	}

	// higher order function
	nums := []int{4, 32, 11, 77, 556, 3, 19, 88, 422}
	results := apply(nums, func(i int) int { // apply here invokes an anonymous function that halves each elements in the slice.
		return i / 2
	})
	results()

	// signaling errors
	words, err := load("dict2.txt")
	if err != nil {
		fmt.Println("Unable to load file:", err)
		os.Exit(1)
	}

	anagrams := make(map[string][]string) // for an empty dict. takes list of strings.
	for _, word := range words {
		wordSig := sortRunes(word)
		anagrams[wordSig] = append(anagrams[wordSig], word) // add to dictioanary
	}
	for k, v := range anagrams {
		fmt.Println(k, "->", v)
	}
}
