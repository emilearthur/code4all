package main

import (
	"fmt"
	"math/rand"
	"strings"
)

// IF statement

// Currency structure
type Currency struct {
	Name    string
	Country string
	Number  int
}

// GHS currency
var GHS = Currency{
	Name:    "Ghana Cedis",
	Country: "Ghana",
	Number:  936,
}

// CAD currency
var CAD = Currency{
	Name:    "Canadian Dollar",
	Country: "Canada",
	Number:  124,
}

// FJD currency
var FJD = Currency{
	Name:    "Fiji Dollar",
	Country: "Fiji",
	Number:  242,
}

// JMD currency
var JMD = Currency{
	Name:    "Jamaican Dollar",
	Country: "Jamaica",
	Number:  388,
}

// USD currency
var USD = Currency{
	Name:    "US Dollar",
	Country: "USA",
	Number:  840,
}

func printCurr(number int) {
	if GHS.Number == number {
		fmt.Printf("Found: %+v\n", GHS)
	} else if CAD.Number == number {
		fmt.Printf("Found: %+v\n", CAD)
	} else if FJD.Number == number {
		fmt.Printf("Found: %+v\n", FJD)
	} else if JMD.Number == number {
		fmt.Printf("Found: %+v\n", JMD)
	} else if USD.Number == number {
		fmt.Printf("Found: %+v\n", USD)
	} else {
		fmt.Println("No currency found with number", number)
	}
}

// SWITCH statements

// Curr structure
type Curr struct {
	Currency string
	Name     string
	Country  string
	Number   int
}

var currencies = []Curr{
	{"DZD", "Algerian Dinar", "Algeria", 12},
	{"AUD", "Australian Dollar", "Australia", 36},
	{"EUR", "Euro", "Belgium", 978},
	{"CLP", "Chilean Peso", "Chile", 152},
	{"EUR", "Euro", "Greece", 978},
	{"HTG", "Gourde", "Haiti", 332},
	{"HKD", "Hong Kong Dollar", "Hong Kong", 344},
	{"KES", "Kenyan Shilling", "Kenya", 404},
	{"MXN", "Mexican Peso", "Mexico", 484},
	{"USD", "US Dollar", "United States", 840},
	{"EUR", "Euro", "Italy", 978},
}

// isDollar check
func isDollar(curr Curr) bool {
	var result bool
	switch curr {
	default:
		result = false
	case Curr{"AUD", "Australian Dollar", "Australia", 36}:
		result = true
	case Curr{"HKD", "Hong Kong Dollar", "Hong Kong", 344}:
		result = true
	case Curr{"USD", "US Dollar", "United States", 840}:
		result = true
	}
	return result
}

// isDollar check2
func isDollar2(curr Curr) bool {
	dollars := []Curr{currencies[2], currencies[6], currencies[9]}
	switch curr {
	default:
		return false
	case dollars[0]:
		fallthrough
	case dollars[1]:
		fallthrough
	case dollars[2]:
		return true
	}
}

func isEuro(curr Curr) bool {
	switch curr {
	case currencies[2], currencies[4], currencies[10]:
		return true
	default:
		return false
	}
}

// Expressionless switches
func find(name string) {
	for i := 0; i < 10; i++ {
		c := currencies[i]
		switch {
		// case expression evalute a Boolean.
		// case strings.Contains(c.Currency, name), strings.Contains(c.Name, name), strings.Contains(c.Country, name):
		case strings.Contains(c.Currency, name) || strings.Contains(c.Name, name) || strings.Contains(c.Country, name):
			fmt.Println("Found", c)
		}
	}
}

func findNumber(num int) {
	for _, curr := range currencies {
		if curr.Number == num {
			fmt.Println("Found", curr)
		}
	}
}

func findAny(val interface{}) { // we call on type interface (which is an empty interface)
	switch i := val.(type) {
	case int:
		findNumber(i)
	case string:
		find(i)
	default:
		fmt.Printf("Unable to search with type %T\n", val)
	}
}

// switch initializer
func assertEuro(c Curr) bool {
	switch name, curr := "Euro", "EUR"; {
	case c.Name == name:
		return true
	case c.Currency == curr:
		return true
	}
	return false
}

// FOR statements
/*
for statement ==> usage
for condition ==> used to semanticaly replace while and do...while loops: for x<10 {...}
infinite loop ==> conditional expression omitted to create infinite loop: for {...}
traditional loop ==> initializer , test and update: for x := 0; x < 10, x++ {...}
for range ==> Used to iterate over collection of item in array, string, slice, map and channel: for i, val := range values {...}
*/

func listCurrs(howlong int) {
	i := 0
	for i < len(currencies) {
		fmt.Println(currencies[i])
		i++
	}
}

// traditional for statement
func sortByNumber() {
	N := len(currencies)
	for i := 0; i < N-1; i++ {
		currMin := i
		for k := i + 1; k < N; k++ {
			if currencies[k].Number < currencies[currMin].Number {
				currMin = k
			}
		}
		// swap
		if currMin != i {
			temp := currencies[i]
			currencies[i] = currencies[currMin]
			currencies[currMin] = temp
		}
	}
}

var list1 = []string{"break", "lake", "go", "right", "strong", "kite", "hello"}
var list2 = []string{"fix", "river", "stop", "left", "weak", "flight", "bye"}

func nextPair(list1 []string, list2 []string) (w1, w2 string) {
	pos := rand.Intn(len(list1))
	return list1[pos], list2[pos]
}

// The for range
/* for statement supports one additional form that uses the keyword range to iterate over an expression that evaluate
to an array, slice, map, string or channel.
generic form --> for [<identifier-list>:=] range<expression>{...}

range expression											==>		range variable
loop over array or slice: for i,v := range[]V{1,2,3}{...}			range brings two values. i the loop index and
																	value v from the collection.
loop over string value: for i,v := range"Hello" {...}				range produces two value. i index of bytes in string,
																	v value of UTF-8 encoded bytes at v[i] as rune.
loop over map: for k, v := range map[K]V {...}						ranges produced two values. k is assigned the value of
																	the map key of type K and v gets stored at map[k] of type V.
loop over channel values: for ch chanT for c := range ch {...}		A channnel is two-way conduit able to recieve and emit values.
																	The for...range statement assign each value recieved from the
																	channel to variable c with each iteration

*/

func printCurrencies() {
	for i := range currencies {
		fmt.Printf("%d: %v\n", i, currencies[i])
	}
}

// The break, continue and goto statements

// Break statement
// the label identifier Declaring a label in Go requires an identifier followed by a colon ==> DoSearch:

// The break statement: break statement terminates and eixts the innermost closing switch or for statement code block and
// transfers control to another part of the running program. The break statement can accept an optional label indentifier
// specifying a labeled location, in the enclosing function, where the flow of the program will resume.
// attributes of the label for the break statement to remember:
// 1. The label must be declared within the same running function where the break statement is located.
// 2. A declared label must be followed immediately by the enclosing control statement(a for loop or switch statement) where the break is nested.
// if a break statement is followed by a label, control is transferred, not to the location where the label is, but rather to the
// statement immediately following the labeled block. If a label is not provided, the break statement abruptly exists and transfers
// control to the next statement following its enclosing for statements (or switch statement) block.

func searchUseBreak(word string, words [][]string) {
DoSearch: //label
	for i := 0; i < len(words); i++ {
		for k := 0; k < len(words[i]); k++ {
			if words[i][k] == word {
				fmt.Println("Found", word)
				break DoSearch // breaking using label. This will exit out of the innermost for loop and cause the execution flow
				// to continue after the outmost labeled for statment.
			}
		}
	}
}

// Continue statement
// the continue statement causes the control flow to immediately terminate the current iteration of the enclosing for loop
// and jump to the next ieteration. ontinue take optional label too. Properties of break statements is;
// 1. The label must be declared within the same running function where the continue statement is located.
// 2. The declared label must be followed immediately by an enclosing for loop statment where the continue statement is nested.
// when present, the continue statement is reaced within for statement block, the for loop will be abruptlly terminated and control
// will be transfered to the outmost labeled for loop block for continuation. If label is not specified, the continue statements
// will simple transfer control to the start of its enclosing for loop block for continuation of the next iteration.

func searchUseContinue(word string, words [][]string) {
DoSearch:
	for i := 0; i < len(words); i++ {
		for k := 0; k < len(words[i]); k++ {
			if words[i][k] == word {
				fmt.Println("Found", word)
				continue DoSearch // statement causes the current iteration of the innermost loop to stop and transfer control
				// to the labeled outer loop, causing it to continue with the next iteration.
			}
		}
	}
}

// goto statement
// goto statement allows flow control to be transferred to an arbitary location inside a function, where a target label is defined.
// the goto statement causes an abrupt transfer of control to the label referenced by the goto statement.

func sample() {
	var a string
Start:
	for {
		switch {
		case a < "aaa":
			goto A
		case a >= "aaa" && a < "aaabbb":
			goto B
		case a == "aaabbb":
			break Start
		}
	A:
		a += "a"
		continue Start
	B:
		a += "b"
		continue Start
	}
	fmt.Println(a)
}

// notes on goto
// 1. Avoid using the goto statement unless the logic being implemented can only be achieved using goto branching. This is
// because overuse of goto statment can make code harder to reason about and debug
// 2. Place goto statments and thier trageted label within the same enclosing code block when possible.
// 3. Avoid placing labels where a goto statement will cause the flow to skip new varaible declarations or cause them to be re-declared.
// 4. It is a complaition error if you try to jump to a peer or to an enclosing code block.

func main() {
	// if statement
	num0 := 242
	if num0 > 100 || num0 < 900 {
		fmt.Println("Currency: ", num0)
		printCurr(num0)
	} else {
		fmt.Println("Currency Unknown")
	}

	if num1 := 388; num1 > 100 || num1 < 900 { // if supports composite syntax where tested expression is preceeded by initialization statment.
		fmt.Println("Currency:", num1)
		printCurr(num1)
	}

	// switch statment
	curr1 := Curr{"EUR", "Euro", "Italy", 978}
	if isDollar(curr1) {
		fmt.Printf("%+v is Dollar currency\n", curr1)
	} else if isEuro(curr1) {
		fmt.Printf("%+v is Euro currency\n", curr1)
	} else {
		fmt.Println("Currency is not Dollar or Euro")
	}

	curr2 := Curr{"HKD", "Hong Kong Dollar", "Hong Kong", 344}
	if isDollar2(curr2) {
		fmt.Println("Dollar currency found:", curr2)
	}

	find("Kenya")

	findAny("Peso")
	findAny(404) 
	findAny(978)
	findAny(false)

	// for statement
	listCurrs(5)

	// traditional for statement
	rand.Seed(31)
	for w1, w2 := nextPair(list1, list2); w1 != "go" && w2 != "stop"; w1, w2 = nextPair(list1, list2) { // the compound logical expression will keep the loop running if true
		fmt.Printf("Word Pair -> [%s, %s]\n", w1, w2)
	}

	// for range
	vals := []int{4, 2, 6}
	for i, v := range vals {
		vals[i] = v - 1 // update original
	}
	fmt.Print(vals, "\n")

	fmt.Println(currencies)
	for i, v := range currencies {
		currencies[i].Number = v.Number + 100
	}
	fmt.Println(currencies)

	printCurrencies()

	// express range without variable declaration
	for range []int{1, 1, 1, 1} {
		fmt.Println("Looping")
	}

	var words = [][]string{
		{"break", "lake", "go", "right", "strong", "kite", "hello"},
		{"fix", "river", "stop", "left", "weak", "flight", "bye"},
		{"fix", "lake", "slow", "middle", "sturdy", "high", "hello"},
	}

	searchUseBreak("slow", words)
	searchUseBreak("duck", words)
	searchUseContinue("slow", words)
	searchUseContinue("duck", words)

	sample()
}
