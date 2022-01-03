package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"time"
)

// composite types include arrays, slices, maps, and structs.

// The array type
// Go arrays are containers for storing sequenced valuess of the same type that are numerically indexed.
// type format [<length>]<element_type>.
// array types can be defined to be multi-dimensions. This is done by combining and nesting the definition of 1-D array types.
// go does not have seperate types for multi-dimensional arrays. An array with more than one dimension is composed of 1-D arrays
// that are nested within each other.
var val [100]int
var days [7]string
var weekdays [5]string
var truth [256]bool
var histogram [5]map[string]int
var board [4][2]int         // 1-D
var matrix [2][2][2][2]byte // Multi-D array

// Array initialization
// when an array variable is not explicitly initialized, all its elements wil be assigned the zero-value for the declared type
// of the elements. An array can be initialized with a composite literal value with the ff. format
// <array_type>{<comma-seperated list of element values}

var valI [100]int = [100]int{44, 72, 12, 55, 64, 1, 4, 90, 13, 54}
var daysI [7]string = [7]string{
	"Monday",
	"Tuesday",
	"Wednesday",
	"Thursday",
	"Friday",
	"Saturday",
	"Sunday",
}
var truthI = [256]bool{true}
var histogramI = [2]map[string]int{
	{"A": 12, "B": 1, "D": 15},
	{"man": 1344, "women": 844, "children": 577},
}

var boardI = [4][2]int{
	{33, 23},
	{62, 2},
	{23, 4},
	{51, 88},
}

var matrixI = [2][2][2][2]byte{
	{{{4, 4}, {3, 5}}, {{55, 12}, {22, 4}}},
	{{{2, 2}, {7, 9}}, {{43, 0}, {87, 7}}},
}

var weekdaysI = [...]string{
	"Monday",
	"Tuesday",
	"Wednesday",
	"Thursday",
	"Friday",
}

// the literal value of an array can be indexted.

var msg = [12]rune{0: 'H', 2: 'E', 4: 'L', 6: 'O', 8: '!'}

// Declaring named array types
// to avoid repeatation, we can declare an alias array tpes declarations.
type matrixD [2][2][2][2]byte

func initMat() matrixD {
	return matrixD{
		{{{4, 4}, {3, 5}}, {{55, 12}, {22, 4}}},
		{{{2, 2}, {7, 9}}, {{43, 0}, {87, 7}}},
	}
}

// Using arrays
// arrays are static entities that cannot grow or shrink in size once they are declared with a specific length. Arrays are a
// great option when a program needs to allocate a block of sequential memory of a predefined size. When a variable of an array
// type is declared, it is ready to be used without any further allocation sematics.
var image [256]byte

// Array traversal
// array traversal can be done using the traditional for statemnt or with more idiomatic for...range statement.
const size = 1000

var nums [size]int

func init() {
	rand.Seed(time.Now().UnixNano())
	for i := 0; i < size; i++ {
		nums[i] = rand.Intn(10000)
	}
}

func max(nums [size]int) int {
	temp := nums[0]
	for _, val := range nums {
		if val > temp {
			temp = val
		}
	}
	return temp
}

// Array as parameters
// arrays values are treated as a single unit. an array variable is not a pointer to a location in memory but rather represents
// the entire block of memory containing the array elements. This has an implications of creating a new copy of values when the
// array variable is reassigned or passed in as a function parameter. This could have unwanted side ffects on memory consumption
// for the program. One fix for is to use pointer types to reference array values.
type numbers [1024 * 1024]int

func initialize(nums *numbers) { // recieving the point of type
	rand.Seed(time.Now().UnixNano())
	for i := 0; i < size; i++ {
		nums[i] = rand.Intn(10000)
	}
}
func maxP(nums *numbers) int {
	temp := nums[0]
	for _, val := range nums {
		if val > temp {
			temp = val
		}
	}
	return temp
}

// note that a composite literal array of value can be initialized with address opeator & to initialize and return a pointer for
// the array.
type galaxies [14]string

func printGalaxies(names *galaxies) {
	for _, name := range names {
		fmt.Println(name)
	}
}

// The slice type
// the slice type is commonly used as the idiomatic construct for indexed data in go. the slice is more flexible and has many
// more interesting characteristics than arrays. The slice itself is a composite type with semantics similar to arrays.
// ie. a lice uses an array as its underlying data storage mechanism. form of slice  -> []<element_type>
var (
	imageS     []byte
	ids        []string
	vector     []float64
	months     []string
	histogramS []map[string]int // slice of a map
	tables     []map[string][]int
	boardS     [][]int
	graph      [][][][]int
)

func print(strs []string) {
	for _, str := range strs {
		fmt.Println(str)
	}
}

// Slice initialization
// a slice is representatin by the type system as a value. Unlike the array type, an uninitalized slice has a zero value of nil,
// which means any attempt to access elements of an uninitialized slice will cause a program to panic. Initialize a slice is
// with a composite literal value using the following format -> <slice_type>[<comma-seperated list of element value>]
var (
	idsS    []string = []string{"fe255", "ac144", "3b12c"}
	vectorS          = []float64{12.4, 44, 126, 2, 11.5}
	monthsS          = []string{
		"Jan", "Feb", "Mar", "Apr",
		"May", "Jun", "Jul", "Aug",
		"Sep", "Oct", "Nov", "Dec",
	}
	// slice of map type
	tablesS = []map[string][]int{
		{
			"age": {53, 13, 5, 44, 45, 62, 34, 7},
			"pay": {124, 66, 777, 531, 933, 231},
		},
	}
	graphS = [][][][]int{
		{{{44}, {3, 5}}, {{55, 12, 3}, {22, 4}}},
		{{{22, 12, 9, 19}, {7, 9}}, {{43, 0, 44, 12}, {7}}},
	}
)

// Slice representation
// slice is represented by a composite value with the following three attributes
// a pointer --> the pointer is the address of the first element of the slice stored in an underlying array. when the slice is
//				 uninitialized wil return nil as it zero value. However, the slice value is not treated as a reference value by
//				 the type system. This means certain function can be applied to a nil slice while others will cause panic.
//				 Once a slice is created, the pointer does not change. To point to a different starting point, new slice must be created.
// a length --> the length indicate the number of contiguous elements that can be accessed starting with the first elements. it is
//				a dynamic value that can grow up to the capacity of the slice. the lenggth of a slice is always less or equal to
//				its capacity. Attempts to access elements beyond the length of the a slice, without resizzing will cause panic.
//				this is true even when the capacity is larger than the length.
// a capacity --> the capacity of a slice is the maximum number of elements that may be stored in the slice, starting from its
//				  first element. The capacity of a slice is bounded by the length of the underlying array.

// Slicing
// another way to create a slice value is by slicing an existing array or another slice value (or pointer to these values).
// --> <slice or array values>[<low_index>:<high_index>] // low value is zero-based index where the slice segments starts.
// high value is the nth elements offset where the segment stops.

var (
	halfyr = []string{"Jan", "Feb", "Mar", "Apr", "May", "June"}
	all    = halfyr[:]
	q1     = halfyr[:3]
	q2     = halfyr[3:]
	mapr   = halfyr[2:4]
)

// Slice an array
var (
	halfyrS = monthsS[:6]
	q1S     = halfyrS[:3]
	q2S     = halfyrS[3:6]
	q3S     = monthsS[6:9]
	q4S     = monthsS[9:]
)

// Slice expression with capacity
// go slice expression supports a longer form where the maximum capacity of the slice is included in the expression.
// -> <slice_or_array_value>[<low_index>:<high_index>: max]
// max attribute specificies the index value to be used as the maximum capacity of the new slice. it can be less of equal to
// the new slice.
var summer1 = monthsS[6:9:9] // the max index is set to position 9. If the max capacity is not stated it takes the length of
// the array.

// Make a slice
// a slice can be initialized at runtime using the built-in function make. This func creates a new slice value and initializes
// its elements with the zero value of the element type.  An uninitilized slice has a nil zero value an indication that it is
// not pointing an underlying array. Without an explicitly initializaiton with composite literal or value or using the make
// function, atttempts to access elemeents of a slice will cause a panic.

// Using slices
// slice traversal can be done using the traditional for statement or with more idiomatic, for ... range statement
func scale(factor float64, vector []float64) []float64 {
	for i := range vector {
		vector[i] *= factor
	}
	return vector
}

func contains(val float64, numbers []float64) bool {

	for i := 0; i < len(numbers); i++ {
		if numbers[i] == val {
			return true
		}
	}
	return false
}

func containsO(val float64, numbers []float64) bool {
	for _, num := range numbers {
		if num == val {
			return true
		}
	}
	return false
}

// Copying slices
// go offeres copy function , which returns a deep copy of a slice along with a new underlying array.
func clone(v []float64) (result []float64) {
	result = make([]float64, len(v), cap(v)) // both source and target slice must be same size and same type or else failure.
	copy(result, v)
	return
}

// Strings as slice
// a slice expression on a string wil reutrn a new string value pointing to its underlying array of runes. the string values can
// be converted to a slice of bytes(or slice of rune).
func sort(str string) string {
	bytes := []byte(str)
	var temp byte
	for i := range bytes {
		for j := i + 1; j < len(bytes); j++ {
			if bytes[j] < bytes[i] {
				temp = bytes[i]
				bytes[i], bytes[j] = bytes[j], temp
			}
		}
	}
	return string(bytes)
}

// The map type
// go map is a composite type that is used as container for storing unordered elements of the same type indexed by an arbitrary
// key value. in general map type is specified -> map[<key_type>]<element_type>

var (
	legends     map[int]string
	histogramMT map[string]int
	calibration map[float64]bool
	matrixMT    map[[2][2]int]bool                          //map with array key type
	tableMT     map[string][]string                         // map of string slices
	log         map[struct{ name string }]map[string]string // map (with struct key) of a string
)

// the key specfifies the type of a value that will be sued to index the stored elements of the map. Unlke arrays and slice, map
// key can be of any type not just int. Map keys, however must be of types that are comparable including numeric, string, bool,
// pointers, arrys, struct and interface types.

// Map initialization
// similar to a slice, a map manages an underlying data structure, opaque to its user, to store its values. An unitialized map
// has a nil zero value as well. Attempts to insert into an uninitialized map will result to panic. Unlike slice, it is possible
// to access elements from a nil map, which will return the zero value of the element.
// maps are initialized <map_type>{<comma-separated list of key:value pairs>}

var (
	histogramMTI = map[string]int{
		"Jan": 100, "Feb": 445, "Mar": 514, "Apr": 233,
		"May": 321, "Jun": 644, "Jul": 113, "Aug": 734,
		"Sep": 553, "Oct": 344, "Nov": 831, "Dec": 312,
	}

	tableMTI = map[string][]int{
		"Men":   {32, 55, 12, 55, 42, 53},
		"Women": {44, 42, 23, 41, 65, 44},
	}
)

// Using maps
// index expressions are used to access and update the elements stored in maps. To set/update a map element, use the index
// expressions.
// go provides a way to test for the absence of an element by returning an optional Boolean values as part of the results of an
// index expresion.

func save(store map[string]int, key string, value int) {
	val, ok := store[key]
	if !ok {
		store[key] = value
		fmt.Println("Done")
	} else {
		panic(fmt.Sprintf("Slot %d taken", val))
	}
}

// Map functions
// map types support two additional function
// len(map) --> len() function returns the number of entries in a map. The len function will return zero for an unitialized map.
// delete(map. key) --> delete function deletes an element from a given map associated with the provided key.

// Maps on parameters
// Because maps maintains an internal pointer to it backing storage structure, all updated to map parameter within a called func
// will be seen by the caller once the func returns.
func remove(store map[string]int, key string) error {
	_, ok := store[key]
	if !ok {
		return fmt.Errorf("key out found")
	}
	delete(store, key)
	return nil
}

// The Struct type
// it is a composite type that serves as a container for other named types known as field.
// format-> struct{<field declaration set>}
// In most struct form, a field is a unique identifier with an assigned type which follows go variable declaration conventions

var (
	empty    struct{}
	car      struct{ make, model string }
	currency struct {
		name, country string
		code          int
	}
	node struct {
		edges  []string
		weight int
	}
	person struct {
		name    string
		address struct {
			street      string
			city, state string
			postal      string
		}
	}
)

// Accessing struct fields
// a struct uses a selector expression (or dot notation) to access the values stored in fields. For instance, the following
// would print the value of the name field of the person struct variable.

// Struct intialization
// similar to arrays, structs are pure values with no additional underlying storage structure.  the fields for an unintailized
// struct are assigned thier respective zero values. this means an unintialized struct requires no further allocation and is
// ready to be used.  <struct_tpe>{<positional or named field values>}

var (
	currencySF = struct {
		name, country string
		code          int
	}{
		"USD", "United State", 840,
	}
	carD = struct {
		make, model string
	}{
		make: "Ford", model: "F150",
	}
	nodeD = struct {
		edges  []string
		weight int
	}{
		edges: []string{"north", "south", "west"},
	}
)

// Declaring named struct types
// attempts to reuse struct types can get unwiedly fast.
type personDN struct {
	name    string
	address address
}

type address struct {
	street      string
	city, state string
	postal      string
}

func makePerson() personDN {
	addr := address{
		city:   "Accra",
		state:  "Greater Accra",
		postal: "2333",
	}
	return personDN{
		name:    "emile bondzie-arthur",
		address: addr,
	}
}

// struct type definition are bind to the identifiers person and addrress. This allows the struct type to be resued in different
// context without need to carray around the long form of type diffinitions

// The anonymous field
// previous definition of struct types involved the use of named fields. however, it is also possible to define a field with only
// its type, ommitting the identifier. ==> anonymous field.  it has the effect embeding the type directly into the struct.

type diameter int

type name struct {
	long   string
	short  string
	symbol rune
}

type planet struct {
	diameter // diameter is embeded as anonymous fields to planet type
	name     // name is embedded as anonymous field to planet type
	desc     string
}

// rules when using anonymous field:
// 1. the name of the type becomes the name of the field
// 2. the name of an anonymous field may not clash with other field names
// 3. use only the unqualified (omit package) type name of imported types

// Structs as parameters
// struct varaibles store actual values. this implies that a new cop of a struct value is created whenever a struct varaible is
// reassigned or passed in as a function parameter.
type personSP struct {
	name  string
	title string
}

func updateNameOLD(p personSP, name string) {
	// function will not update
	p.name = name
}

func updateName(p *personSP, name string) {
	p.name = name
}

// Field tags
// during the definition of a struct type, optional string values may be added to each field declaration. The value of the string
// is arbitrary and it can serve as hints to tools or other APIs that uses reflection to consume the tags. in the eg. below
// peron and address structs are tagged with JSON annotation which can be inerpreted by go's json encoder and decorder.

// Person type
type Person struct {
	Name    string `json:"person_name"`
	Title   string `json:"person_title"`
	Address `json:"person_address_obj"`
}

type Address struct {
	Street string `json:"person_addr_street"`
	City   string `json:"person_city"`
	State  string `json:"person_state"`
	Postal string `json:"person_postal_code"`
}

func main() {
	fmt.Println(board)
	fmt.Println(matrix)
	fmt.Println(histogramI)
	fmt.Println(boardI)
	fmt.Println(matrixI)
	fmt.Println(weekdaysI)
	fmt.Println(msg)

	// declaring named arrays
	var mat1 matrixD
	mat1 = initMat()
	fmt.Println(mat1)

	// using arrays
	p := [5]int{122, 6, 23, 44, 6}
	p[4] = 82 // changing value in array
	fmt.Println(p[0], p[4])

	// length and capacity of the array
	seven := [7]string{"grumpy", "sleepy", "bashful"}
	fmt.Println(len(seven), cap(seven))

	fmt.Println(nums[0:10])
	fmt.Println(max(nums))

	// array as parameters
	var nums *numbers = new(numbers) // intialize the array of elements with thier zerio values and obtain a pointer to that array
	initialize(nums)                 // when called it receive the new address above (a copy of it) of the array instead of entire 100K sized array.
	fmt.Println(maxP(nums))

	// using address operator & to constract an array
	namedGalaxies := &galaxies{
		"Andromeda",
		"Black Eye",
		"Bode's",
		"Cartwheel",
		"Cigar",
		"Comet",
		"Hoag's",
		"Magellanic",
		"Mayall's",
		"Pinwheel",
		"Sombrero",
		"Sunflower",
		"Tadpole",
		"Whirpool",
	}
	printGalaxies(namedGalaxies)

	// slice array
	fmt.Printf("Image %T : %v\n", image, image)
	fmt.Printf("Ids %T : %v\n", ids, ids)
	fmt.Printf("Vector %T : %v\n", vector, vector)
	fmt.Printf("Months %T : %v\n", months, months)
	fmt.Printf("Tables %T : %v\n", tables, tables)
	fmt.Printf("Board %T : %v\n", board, board)
	fmt.Printf("Graph %T : %v\n", graph, graph)

	print(months)

	// slice initialization
	fmt.Printf("ids:  %v\n", idsS)
	fmt.Printf("vector: %v\n", vectorS)
	fmt.Printf("months: %v\n", monthsS)
	fmt.Printf("table: %v\n", tablesS)
	fmt.Printf("graph: %v\n", graphS)

	// slicing
	fmt.Println(halfyr)
	fmt.Println(q1)
	fmt.Println(q2)
	fmt.Println(q3S)
	fmt.Println(q4S)
	fmt.Println(mapr)
	fmt.Println(summer1)

	// making a slice
	monthsM := make([]string, 6) // array of type stiring with length and capacity of 6. returns a slice value (not a pointer)
	// after initialization with make() func , access to a legal index will return the zero value for the slice element instead
	// of causing a program panic. make can take the capacity parameter.
	monthsMC := make([]string, 6, 12)
	hh := make([]float64, 4, 10)
	var vectorLC []float64 // prints 0, no panic. slice is a value (not a pointer) that nil as its zero-value.

	fmt.Println(monthsM, len(monthsM), cap(monthsM))
	fmt.Println(monthsMC, len(monthsMC), cap(monthsMC))
	fmt.Println(hh, len(hh), cap(hh))
	fmt.Println(vectorLC, len(vectorLC), cap(vectorLC))

	// using slice
	h := []float64{12.5, 18.4, 7.0}
	fmt.Println("before change", h[0])
	h[0] = 15 // accessing the elements of a slice value at index 0 and updating
	fmt.Println("after change", h[0])

	xp := []float64{1, 2, 5, 7, 9}
	fmt.Println(contains(5, xp))
	fmt.Println(containsO(5, xp))
	fmt.Println(scale(5, xp))

	//Appending to slice
	// slice types can dynamically grow. By default a slice has a static length and capacity. Any attempt to access index beyond
	// that limit causes a panic. Go has variadic function append to dynamically add new values to a specified slice, growing
	// its length and capacity.
	monthsAS := make([]string, 3, 3)
	monthsAS = append(monthsAS, "Jan", "Feb", "Mar", "Apr", "May", "June")
	monthsAS = append(monthsAS, []string{"Jun", "Aug", "Sep"}...) // using variadic to indicate values are list
	monthsAS = append(monthsAS, "Oct", "Nov", "Dec")
	fmt.Println(len(monthsAS), cap(monthsAS), monthsAS)

	// String as slices
	msg := "Bobysaysgotohells"
	fmt.Println(
		msg[:3], msg[3:7], msg[7:12],
		msg[12:17], msg[len(msg)-1:],
	)

	fmt.Println("acmssiepqii", "->", sort("acmssiepqii"))

	// Map intialization
	for k, v := range histogramMTI {
		fmt.Println("key: ", k, " value -> ", v)
	}
	for k, v := range tableMTI {
		fmt.Println("key: ", k, " value -> ", v)
	}

	// Making slice
	hist := make(map[string]int) // can take a second parameter to specify the capacity of the map.
	hist["Jan"] = 100
	hist["Feb"] = 445
	hist["Mar"] = 415

	for k, v := range hist {
		fmt.Println("key: ", k, " value -> ", v)
	}

	// Using maps
	fmt.Println(histogramMTI["Jan"])
	histogramMTI["Jan"] = 1000 // access value via index and update
	fmt.Println(histogramMTI["Jan"])

	fmt.Println(histogramMTI["December"]) // will return 0 since element/key does not exit.

	histUM := make(map[string]int, 6)
	histUM["Jan"] = 100
	histUM["Feb"] = 445
	histUM["Mar"] = 514
	histUM["Apr"] = 233
	histUM["May"] = 321
	histUM["Jun"] = 644
	histUM["Jul"] = 113

	save(histUM, "Aug", 734)
	save(histUM, "Sep", 553)
	save(histUM, "Oct", 344)
	save(histUM, "Nov", 831)
	save(histUM, "Dec", 312)
	save(histUM, "Dec0", 332)
	// save(histUM, "Aug", 734) // causes panic

	// Map traversal
	// the for...range loop statement can be used to walk the content of a mp value.
	// for key, value := range histUM {
	// 	adjVal := int(float64(value) * 0.100)
	// 	fmt.Printf("%s (%d):", key, value)
	// 	for i := 0; i < adjVal; i++ {
	// 		fmt.Println(".")
	// 	}
	// 	fmt.Println()
	// }
	for key, value := range histUM {
		fmt.Println(key, value)
	}

	remove(histUM, "Jul")

	// Accessing struct fields
	fmt.Println(histUM["Jul"]) // return 0 because key is deleted
	fmt.Println(currencySF.country)
	fmt.Println(currencySF.code)
	fmt.Println(currencySF.name)
	fmt.Println(nodeD.edges)

	// Declaring named struct types
	perz := makePerson()
	fmt.Println(perz)

	// The anonymous field => accessing
	earth := planet{
		diameter: 7936,
		name: name{
			long:   "Earth",
			short:  "E",
			symbol: '\u2641',
		},
		desc: "Third rock from the sun",
	}
	// using the selector expression to update fields
	jupiter := planet{}
	jupiter.diameter = 88846
	jupiter.name.long = "Jupiter"
	jupiter.name.short = "J"
	jupiter.name.symbol = '\u2643'
	jupiter.desc = "A ball of gas"

	// fields of an embedded struct can be promoted to it enclosing type.  Promoted fields appears in selector expression
	// without the qualified named of thier types
	saturn := planet{}
	saturn.diameter = 120536
	saturn.long = "Saturn"
	saturn.short = "S"
	saturn.symbol = '\u2644'
	saturn.desc = "Slower mover"

	fmt.Printf("Planet %v, diam %d, desc: %s\n", earth.name, earth.diameter, earth.desc)
	fmt.Printf("Planet %v, diam %d, desc: %s\n", jupiter.name, jupiter.diameter, jupiter.desc)
	fmt.Printf("Planet %v, diam %d, desc: %s\n", saturn.name, saturn.diameter, saturn.desc)

	// Structs as parameters
	pz := personSP{
		name: "unknown"}
	updateNameOLD(pz, "Emilex Trig")

	fmt.Println(pz) // value did not update after updateName function

	updateName(&pz, "Emilex Trig")
	fmt.Println(pz)

	px := new(personSP)
	px.name = "unknown"
	updateName(px, "Fred Trig")

	fmt.Println(px)

	// Field tags
	per := Person{
		Name:  "Emilex trig",
		Title: "Software Engineer (Data, Backend)",
		Address: Address{
			Street: "North Ajao Road",
			City:   "Makeville",
			State:  "Mae",
			Postal: "00233",
		},
	}
	b, err := json.Marshal(per)
	if err != nil {
		panic(err.Error())
	}
	fmt.Println(per)
	fmt.Println(string(b))
}
