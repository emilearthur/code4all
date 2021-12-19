package main

import (
	"fmt"
	"math"
	"strings"
	"unsafe"
)

// go types

var (
	a uint8   = 72
	b int32   = 240
	c uint64  = 123456721
	d float32 = 123456721.11
	e int64   = -1234567211223
	f float64 = -1.34445567775
	g int16   = 32000
	h [5]rune = [5]rune{'O', 'n', 'T', 'o', 'p'}
	j string  = "something"
)

/*
types  ==> Description
string ==> type for storing text values
rune   ==> An integer type(int32) used to represent characters.
byte, int, int8, int16, int64, rune, uint, unit8, uint16, uint32, uint64, uintptr => types for storing integral values.
float32, float64 ==> Types for storing floating point decimal values.
complex64, complex 128 ==> Types that can represent complex numbers with both real and imaginary parts.
*T, pointer of type T => A type that represents a memory address where a value of type T is stored.
array [n]T ==> An ordered collection of fixed size n of numerically indexed sequence of elements of a type T.
slice []T ==> A collection of unspecified size of numerically indexed sequence of elements of type T.
struct{} ==> A structure of a composite type composed of elements known as fields (think of an object)
map[K]T ==> An unordered sequence of elements of type T indexed by a key of arbitrary type K.
interface{} ==> A named set of function declarations that define a set of operations that can be implemented by other types.
func (T) R ==> A type that represents all functions with a given parameter type T and return type R.
chan T ==> A type for an internal communcation channel to send or receive values of type T.

*/

// numeric types
var _ int8 = 12
var _ int16 = -400
var _ int32 = 12022
var _ int64 = 1 << 33
var _ int = 3 + 1415

var _ uint8 = 18
var _ uint16 = 44
var _ uint32 = 133121
var i uint64 = 23113233
var _ uint = 7542
var _ byte = 255
var _ uintptr = unsafe.Sizeof(i)

var _ float32 = 0.5772156649
var _ float64 = math.Pi

var _ complex64 = 3.5 + 2i
var _ complex128 = -5.0i

/*
unsigned integer types
type	==> Size				==> Description
uint8	unsigned 8-bit			Range 0-255
uint16	unsigned 16-bit			Range 0-65535
uint32	unsigned 32-bit			Range 0-4294967295
uint64	unsigned 64-bit			Range 0-18446744073709551615
uit		implmentation specific	A pre-declared type desinged to represent either 32/64 bits int.
byte	Unsigned 8-bit			Alias for the unit8 type
uintptr	Unsigned				An unsigned integer type designed to store pointers (mem. addresses) for the underlying machine arch.

signed integer types
type	==> Size				==> Description
int8	signed 8-bit			Range-128-127
int16	signed 16bit			Range -32768 – 32767
int32	signed 32bit			Range -2147483648 – 2147483647
int64	signed 64bit			Range -9223372036854775808 – 9223372036854775807
int		implmentation specific	A pre-declared type designed to represent either the 32 or 64-
		bit integers.

floating point types
type	==> Size				==> Description
float32	signed 32-bit			single precision floating point values
float64 signed 64-bit			double precision floating point values

complex number typees
type		==> Size				==> Description
complex64	float32					real and imarginary parts stored as float32 values
complex128	float64					real and imarginary parts stored as float64 values

*/

// Pointers
// For data stored in memory, the value of data may be accessed directly or a pointer may be used to reference the memory
// address where the data is located.
// in go * operator is used to designate a type as a pointer.

var valPtr *float32
var countPtr *int
var person *struct {
	name string
	age  int
}
var matrix *[1024]int
var row []*int64

// given varible type T, Go uses expression *T as its pointer type. The type system consider T and *T as distinct and are not fungible.
// the zero value of a pointer, when it is not pointing to anything is address 0, represented by constant nil.

// The address operator
// Pointer values can only be assigned addresses of their declared types.
// One way you can do in Go is to use the address operate &(ampersand) to obtain the address value of a variable
var aplus int = 1024
var aptr *int = &aplus

// Pointer indirection -- accessing referenced values
// if you have an address, you can access the value to which it points by applying the * operator to the pointer value
// itself (or dereferencing).

// double - multiple value by 2
func double(x *int) {
	*x = *x * 2
	/*
		notes
		 *x * 2 -- original expression where x is of type *int
		 *(*x) * 2 -- Dereferencing pointers by applying * to address values.
		 3 * 2 = 6 -- Dereferencing value of *(*x) = 3
		 *(*x) = 6 -- The right side of this expression dereferences the value of x. It is update with result 6.
	*/

}

// cap - capitalize a string
func cap(p *struct{ first, last string }) {
	p.first = strings.ToUpper(p.first)
	p.last = strings.ToUpper(p.last)
}

// Type declaration
// It is possible to bind a type to an identifier to create a new named type that can be referenced and used to whatever type
// is needed. Declaring a type takes the general format: type<name identifier><underlying type name> E.g. type truth bool,
// type quart float64, type node string.
// A type declaration can also use a composite type literal as its underlying type. Composite types include array, slice, map and struct.

type fahrenheit float64
type celsius float64
type kelvin float64
type signal int

func fharToCel(f fahrenheit) celsius {
	return celsius((f - 32) * 5 / 9)
}

func fharToKel(f fahrenheit) kelvin {
	return kelvin((f-32)*5/9 + 273.15)
}

func celToFah(c celsius) fahrenheit {
	return fahrenheit(c*5/9 + 32)
}

func celToKel(c celsius) kelvin {
	return kelvin(c + 273.15)
}

func main() {
	fmt.Printf("a = %v[%T, %d bits]\n", a, a, unsafe.Sizeof(a)*8)
	fmt.Printf("b = %v[%T, %d bits]\n", b, b, unsafe.Sizeof(b)*8)
	fmt.Printf("c = %v[%T, %d bits]\n", c, c, unsafe.Sizeof(c)*8)
	fmt.Printf("d = %v[%T, %d bits]\n", d, d, unsafe.Sizeof(d)*8)
	fmt.Printf("e = %v[%T, %d bits]\n", e, e, unsafe.Sizeof(e)*8)
	fmt.Printf("f = %v[%T, %d bits]\n", f, f, unsafe.Sizeof(f)*8)
	fmt.Printf("g = %v[%T, %d bits]\n", g, g, unsafe.Sizeof(g)*8)
	fmt.Printf("h = %v[%T, %d bits]\n", h, h, unsafe.Sizeof(h)*8)
	fmt.Printf("j = %v[%T, %d bits]\n", j, j, unsafe.Sizeof(j)*8)

	// numeric types
	var _ int8 = 12
	var _ int16 = -400
	var _ int32 = 12022
	var _ int64 = 1 << 33
	var _ int = 3 + 1415

	var _ uint8 = 18
	var _ uint16 = 44
	var _ uint32 = 133121
	var i uint64 = 23113233
	var _ uint = 7542
	var _ byte = 255
	var _ uintptr = unsafe.Sizeof(i)

	var _ float32 = 0.5772156649
	var _ float64 = math.Pi

	var _ complex64 = 3.5 + 2i
	var _ complex128 = -5.0i

	vals := []int{
		1024,
		0x8BADF00D,
		0xBEEF,
		0777,
	}
	for _, i := range vals {
		if i == 0xBEEF {
			fmt.Printf("Got %d\n", i)
			break
		}
	}

	p := 3.1415926535
	e := .5772156649
	x := 7.2e-5
	y := 1.616199e-35
	z := .416833e32

	fmt.Println(p, e, x, y, z)

	a := -3.5 + 2i
	fmt.Printf("%v\n", a)
	fmt.Printf("%+g, %+g\n", real(a), imag(a))

	var readyToGo bool = false
	if !readyToGo {
		fmt.Println("Come on")
	} else {
		fmt.Println("Let's go!")
	}

	var (
		bksp  = '\b'
		tab   = '\t'
		nwln  = '\n'
		char1 = "&"
		char2 = "@"
		char3 = "\u0369"
		char4 = "\xFA"
		char5 = "\045"
	)
	fmt.Println(bksp)
	fmt.Println(tab)
	fmt.Println(nwln)
	fmt.Println(char1)
	fmt.Println(char2)
	fmt.Println(char3)
	fmt.Println(char4)
	fmt.Println(char5)

	var (
		txt  = "水 and 火"
		txt2 = "\u6C34\x20brings\x20\x6c\x69\x66\x65."
		txt3 = "\u6C34\x20brings\x20\x6c\x69\x66\x65."
	)
	for i := 0; i < len(txt); i++ {
		fmt.Printf("%U ", txt[i])
	}
	fmt.Println()
	fmt.Println(txt2)
	fmt.Println(txt3)

	fmt.Println(valPtr, countPtr, person, matrix, row)

	fmt.Printf("a=%v\n", aplus)
	fmt.Printf("aptr=%v\n", aptr)

	// intializaition of composite types with address
	structPtr := &struct{ x, y int }{44, 55} //address operator used directly with composite literal.
	pairPtr := &[2]string{"A", "B"}

	fmt.Printf("struct=%#v, type=%T\n", structPtr, structPtr)
	fmt.Printf("pairPtr=%#v, type=%T\n", pairPtr, pairPtr)

	// The new() function.
	// can used to initialize a pointer value. It first allocates the appropriate memory for zero-value of the specified type.
	// the function then returns the address for the newly created value.

	intptr := new(int)
	*intptr = 44

	person := new(struct{ first, last string })
	person.first = "Samuel"
	person.last = "Pierre"
	fmt.Printf("Value %d, type %T\n", *intptr, intptr)
	fmt.Printf("Person %+v\n", person)

	// point indirection
	aSub := 3
	double(&aSub)
	fmt.Println(aSub)
	pSub := &struct{ first, last string }{"Max", "Plank"}
	cap(pSub)
	fmt.Printf("Person %+v\n", pSub)

	
	// type declaration
	var c celsius = 32.0
	f := fahrenheit(122)
	fmt.Printf("%.2f \u00b0C = %.2f \u00b0K\n", c, celToKel(c))
	fmt.Printf("%.2f \u00b0F = %.2f \u00b0C\n", c, fharToCel(f))


	// type conversion 
	var count int32 
	var actual int
	var test int32 = int32(actual) + count

	var sig signal
	var event int = int(sig)

	fmt.Println(test)
	fmt.Println(event)
}
