package main

import (
	"fmt"
	"math"
)

// Go methods
// a go function can be defined with a scope narrowed to that of a specific type. when a function is scoped to a type or attached
// to the type, it is know as a method. a method is defined like a go function. However, its definition include a method reciever,
// which is an extra parameter palced before the method;s name, used to specifiy the host ype to which the method is attached.

type gallon float64 // Base type
type quart float64

// method
func (g gallon) quart() quart { // (g gallom) --> reciever.
	return quart(g * 4)
}

// at runtime, the reciever parameter provides access to the value assigned to the base type of the method.
// nb: base type for method receiver cannot be a pointer (nor an interface). eg. type gallo *float64 --> will not compile
// implmentation of a liquid volume conversion program. each volumetric type receives it respective method to expose a behaviors
// attributed to that type
type ounce float64

func (o ounce) cup() cup {
	return cup(o * 0.1250)
}

type cup float64

func (c cup) quartC() quartC {
	return quartC(c * 02.25)
}

func (c cup) ounce() ounce {
	return ounce(c * 8.0)
}

type quartC float64

func (q quartC) gallonC() gallonC {
	return gallonC(q * 0.25)
}

func (q quartC) cup() cup {
	return cup(q * 4.0)
}

type gallonC float64

func (g gallonC) quartC() quartC {
	return quartC(g * 4)
}

// method set -> the number of methods attached to a type via the receiver parameters. this includes both concrete and pointer
// value receivers. the concept of a method set is important in determining type equality, interface implmentation and support
// notion of the empth empty method set for the empty infterface.

// Value and pointer receivers
// receivers are normal function parameters. they folow the ass-by-value mechanism of go functions. this means, invoked methods
// get a copy of the original value from the declared type. Receiver params can be passed as either values of or pointers of the
// base type.
type gallonVP float64

func (g gallonVP) quart() float64 {
	return float64(g * 4)
}
func (g gallonVP) half() {
	g = gallonVP(g * 0.5)
}
func (g *gallonVP) double() { // taking the pointer
	*g = gallonVP(*g * 2) // dereferencing updating the pointer
}

// pointer receiver parameters are widely used in Go. this is becuase they make it possile to express object-like primitives
// that carry both state and behaviours.

// Objects in Go
// go was not designed to function as traditional OO language. there is no object or class keywords defined in go. go supports
// object idioms and the pratice of OOP without the heavy baggage of classical hierarchies and complex inheritance structures
// found in other OO langes.

// The struct as object
// nearly all go types can play the roles of an object by storing states and exposing methods that are capable of accessing and
// modifying those states. the struct type however offers all the features that are traditionally attributed to objects in other
// langauages such as i. ability to host methods ii. ability to be extended via composition iii. Ability to be sub-types (with
// the help from the Go interface type)

// Object Composition
// demonstrat how the struct type may be used as an object that can achieve polymorphic composition.
type fuel int

const (
	// GASOLINE fuel
	GASOLINE fuel = iota
	// BIO constant
	BIO
	// ELECTRIC constant
	ELECTRIC
	// JET constant
	JET
)

type vechile struct {
	make  string
	model string
}

type engine struct {
	fuel   fuel
	thrust int
}

func (e *engine) start() {
	fmt.Println("Engine started.")
}

type truck struct {
	vechile
	engine
	axels  int
	wheels int
	class  int
}

func (t *truck) drive() {
	fmt.Printf("Truck %s %s, on the go!\n", t.make, t.model)
}

type plane struct {
	vechile
	engine
	engineCount int
	fixedWings  bool
	maxAltitude int
}

func (p *plane) fly() {
	fmt.Printf("Aircraft %s %s clear for takeoff!\n", p.make, p.model)
}

// components and thier relationships below
// vehicle		engine 		fuel
// truck 					plane
// -vehicle 				-vehicle
// -engine 					-engine
// --fuel 					--fuel

// go uses the composition over inheritance priciniple to achieve polymorphism using the type embedding mechanism supported by the
// the struct type. there is no support for polymorphism via type inheritance.

// The constructor function
// since go does not support classes, there is no such concept as constructor. However, one conventional idiom you will encounter
// in go is the use of a factory funtion to create and initialize values for a type.
// in the code below , we use the constructor function for creating nw vales of plane and truck types

func newTruck(mk, mdl string) *truck {
	return &truck{vechile: vechile{mk, mdl}}
}

func newPlane(mk, mdl string) *plane {
	pl := &plane{}
	pl.make = mk
	pl.model = mdl
	return pl
}

// while not required, providing a function to help with the initializaiton of composite values such as struct increases the
// usabilit of the code. it provides a place to encapsulate repeatable initializaiton logic that can be enforce validation
// requirements.  both newTruct and newPlance are passed the make and model information to create and initialize their respective
// values.

// The interface type
// interface is a set of methods that serves as a template to describe a behavior. a go interface is a type specified by the
// interface{} literal, which is used to list a set of methods that satisfies the interface.
// eg below shape declared as interface
var shape interface {
	area() float64
	perim() float64
}

// rewriting the shape using interface type. using idiomatic go.
type shapeT interface {
	area() float64
	perim() float64
}

var s shapeT

// Implementating an interface
// implementating a go interface is done implicitly. there is no seperate element or keyword required to indicate the intent of
// implmentation. Any type ethat defines the method set of an interface type automatically satisfies its implementation.
type rect struct {
	name           string
	length, height float64
}

func (r *rect) area() float64 {
	return r.length * r.height
}

func (r *rect) perim() float64 {
	return 2*r.length + 2*r.height
}

func (r *rect) String() string {
	return fmt.Sprintf(
		"%s[lenght:%.2f height:%.2f]",
		r.name, r.length, r.height,
	)
}

// Subtyping with Go interfaces
type triangle struct {
	name    string
	a, b, c float64
}

func (t *triangle) area() float64 {
	return 0.5 * (t.a * t.b)
}

func (t *triangle) perim() float64 {
	return t.a + t.b + math.Sqrt((t.a*t.a)+(t.b*t.b))
}

func (t *triangle) String() string {
	return fmt.Sprintf(
		"%s [sides: a=%.2f b=%.2f c=%.2f]", t.name, t.a, t.b, t.c,
	)
}

func shapeInfo(s shapeT) string {
	return fmt.Sprintf(
		"Area = %.2f, Perim = %.2f", s.area(), s.perim(),
	)
}

// Implmenting multiple interfaces
// implicit mechanism of interfaces allows any named type to satify multiple interface types at once. this is achieved simply
// by having the method set of a given type intersect with the methods of each interface type to be implemented.
// reimplmenting shape into shape and polygon.
type shapeI interface {
	area() float64
}

type polygon interface {
	perim()
}

type curved interface {
	circonf()
}

type circle struct {
	name string
	rad  float64
}

func (c *circle) area() float64 {
	return math.Pi * (c.rad * c.rad)
}

func (c *circle) circonf() float64 {
	return 2 * math.Pi * c.rad
}

func (c *circle) String() string {
	return fmt.Sprintf(
		"%s[rad: a=%.2f diam=%.2f]",
		c.name, c.rad, (2 * c.rad),
	)
}

func shapeInfoI(s shapeI) string {
	return fmt.Sprintf("Area = %.2f", s.area())
}

// Interface embedding
// interface types support type embedding (similar to struct type). this gives the flexibility to stucture your types in ways
// that maximize type resuse.

type polygonI interface {
	shapeI
	perim()
}

type curvedI interface {
	shapeI
	circonf()
}

// when embedding interface types, the enclosing type will inherit the method set of embedding types. the complier will complain
// if the embedded type causes method signatures to clash.

// The empty interface type
// interface{} type or the empty interface type  is  the literal representation of an interface type with an empty method set.
// all types implement the empty interface since all types can have a method set with zero or more member. when a variable is
// assigned the interface{} type, the compiler relaxes it build-time type checks. the variable still carries type information
// that can be queried at runtime.
func printAnyType(val interface{}) {
	fmt.Println(val)
}

// an empty interface is crucially important for idiomatic go. it make it feels more dyanamic without sacrificing strong typing.

// Type assertion
// when an interface (empty or not) is assigned to a variable, it carries type information that can be queried at runtime. type
// assertion idiomatically narrow a variable(of interface type) down to a concrete type and value that are stored in the variable
// in the eg. below we use type assertion in the eat function to select the food type to select.
// the general form for type assertion expression is <interface_variable>.(concrete type name)
// the type assertino expression can return two values: one the concrete value (extracted from the interface) and second boolean
// indicating the success of the assertion -> value, boolean := <interface_variable>.(concrete type name)
type food interface {
	eat()
}

type veggies string

func (v veggies) eat() {
	fmt.Println("Eating", v)
}

type meat string

func (m meat) eat() {
	fmt.Println("Eating tasty", m)
}

func eat(f food) {
	veg, ok := f.(veggies)
	if ok {
		if veg == "okra" {
			fmt.Println("Nope, not eating ", veg)
		} else {
			veg.eat()
		}
		return
	}
	mt, ok := f.(meat)
	if ok {
		if mt == "beef" {
			fmt.Println("Nope, not eating ", mt)
		} else {
			mt.eat()
		}
		return
	}
	fmt.Println("Not eating whatever that is: ", f)
}

// using switch statment
func eatS(f food) {
	switch morsel := f.(type) {
	case veggies:
		if morsel == "okra" {
			fmt.Println("Nope, not eating ", morsel)
		} else {
			morsel.eat()
		}
	case meat:
		if morsel == "beef" {
			fmt.Println("Nope, not eating ", morsel)
		} else {
			morsel.eat()
		}
	default:
		fmt.Println("Not eating whatever that is: ", f)
	}
}

func main() {
	gal := gallon(5)
	fmt.Println(gal.quart())

	gal1 := gallonC(5)
	fmt.Printf("%.2f gallons = %.2f quarts\n", gal1, gal1.quartC())
	ozs := gal1.quartC().cup().ounce()
	fmt.Printf("%.2f gallons = %.2f ounces\n", gal1, ozs)

	// Value and pointer receivers
	var gal2 gallonVP = 5
	gal2.half()
	fmt.Println(gal2) //
	gal2.double()
	fmt.Println(gal2)

	// Field and method promotion
	t := &truck{
		vechile: vechile{"Ford", "F750"},
		engine:  engine{GASOLINE + BIO, 700},
		axels:   2,
		wheels:  6,
		class:   3,
	}
	t.start() // since engine is embedded in truck, the start() method is promoted in scope to enclosing type and thus accessible.
	t.drive()

	// struct type embedding mechanism promotes fields and methods when accessed using dot notation.
	p := &plane{}
	p.make = "HondaJet"
	p.model = "HA-420"
	p.fuel = JET
	p.thrust = 2050
	p.engineCount = 2
	p.fixedWings = true
	p.maxAltitude = 43000
	p.start()
	p.fly()

	// The constructor function
	tC := newTruck("Ford", "F150")
	tC.axels = 2
	tC.wheels = 6
	tC.class = 3
	tC.start()
	tC.drive()

	pC := newPlane("HondaJet", "HK-500")
	pC.fuel = JET
	pC.thrust = 2050
	pC.engineCount = 2
	pC.fixedWings = true
	pC.maxAltitude = 43000
	pC.start()
	pC.fly()

	// Subtyping with Go interfaces
	rt := &rect{
		name:   "Square",
		length: 4.0,
		height: 4.0}
	fmt.Println(*rt, "=>", shapeInfo(rt))

	ta := &triangle{
		name: "Right Triangle",
		a:    1,
		b:    2,
		c:    3}
	fmt.Println(*ta, "=>", shapeInfo(ta))

	// Implmenting multiple interfaces
	rti := &rect{"Square", 4.0, 4.0}
	fmt.Println(rti, "=>", shapeInfoI(rti))

	tai := &triangle{"Right Triangle", 1, 2, 3}
	fmt.Println(tai, "=>", shapeInfoI(tai))

	ci := &circle{"Small circle", 20}
	fmt.Println(ci, "=>", shapeInfoI(ci))

	// Interface embedding
	rtii := &rect{"Square", 4.0, 4.0}
	fmt.Println(rtii, "=>", shapeInfoI(rtii))

	taii := &triangle{"Right Triangle", 1, 2, 3}
	fmt.Println(taii, "=>", shapeInfoI(taii))

	cii := &circle{"Small circle", 20}
	fmt.Println(cii, "=>", shapeInfoI(cii))

	// The empty interface type
	var anyType interface{}
	anyType = 77.0
	fmt.Println(anyType)
	anyType = "I am a string now"
	fmt.Println(anyType)

	printAnyType("The car is slow")
	m := map[string]string{"ID": "12345", "name": "Merry"}
	printAnyType(m)
	printAnyType(1234859998882) // as we can see various values/types are assigned to type interface{} without complaints
	// from the compiler

}
