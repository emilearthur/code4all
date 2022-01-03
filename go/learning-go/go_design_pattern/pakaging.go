package main

import (
	"fmt"
	"os"
)

//The Go package
// like other PL go source code files are grouped into compilable and shareable units - packages. However all Go source files
// must belong to a package (there is no default package). This strict approach allows Go to keep its compliation rules
// and package resolution rule simple by favouring convention over configuration.

// Understanding Go package
// A go package is both a physical and a logical unit of code organization used to encapsulate related concepts that can
// be reused. A group of source files stored in the same directory are considered to be part of the same package.
// a directory below
// foo
//	|-- blat.go
//	|__bazz
//		|--quux.go
//		|--qux.go

// The workspace -- refer to go/src/github.com/emilearthur/learning-go/chsix for more
// workspace is an arbitrary directory that serves as a namespace used to resolved packages during certain task such as
// compliation. By conversion, Go tools expect three specifically named subdir in a workspace directory: src, pkg and bin.
// These subdir store go source files along with all built packages artifacts respectively.
// Establish

// Name packages -- refer to go/src/github.com/emilearthur/learning-go/chsix for more
// Go expects each package in a workspace to have unique fully qualified import path. Idiomatic Go prescribes some rule for
// naming and organization of your packages to make creating and using packages simple.

// Package visibility
// regardless of  the number of source files declared to be part of a package, all source code elements(types , var, constant
// and functions), declared at package level share a common scope. Thus the complier will not allow an element identifie to be
// re-declared more than once in the entire package.

// Package member visibility
// the usefulness of a package is its ability to expose its source elements to other packages. Controlling the visibility of
// elements of a package is simple and follows this rule: capitalied identifiers are exported automatically -> This means
// types, var, const or fun with capitalized identifiers is automatically visible from outside of the package where it is
// declared.
// Eg. function R in package resistor is automaticall exported and can be accesse from other packages as: resistor.R()
// function identifier recip is in all lowercase and therefore is not exporeted. Though accessible within its own scope,
// the function will not be visible from within other packages.

// Importing package
// keyword import is used to import source code elements from an external packages. It allows the importing source to access
// exported elements found in the imported package.The form of import -> import [package name identifier] "<import path>"
// the import support an optional package identifier that can be used to explicitly name the imported package.
// import statement can be written as import block. this is useful when import two or more import packages.
// import (
//	[package name identifier] "<import path>"
// )
// the dot notation is used to access exported memebers of an imported package.
// TO specify package identifier we declare the name identifier for the import -> res "github.com/emilearthur/learning-go/chsix/resistor"

// The dot identifer
// A package can optionally be assigned a dot(peroid) as its identifier. When an import statement is uses the dot identifier(.)
// for an import path [i.e. -> import (. "github.com/emilearthur/learning-go/chsix/resistor")], it caueses members of the imported
// package to be merged in scope with that of the imported package. There imported members may be referenced without additional
// qualifiers.

// The blank identifier
// When a package is imported, it is a requirement that one of its members be referenced in the importing code at least once.
// failure for this results to compliation error.  Using the blank identifier causes the compiler to bypass this requirement.
// eg. -> import (_ "fmt")

// Creating programs
// to create a program in GO, you have to take a package and create an entry point of execution that follows:
// Declare (at least) source file to be part of the special package called main
// Declare one function name main() to be used as the entry point of the program

// Accessing program args
// go runtime makes all cmd-line args avialable as a slice via package varaible os.Args.

// Building and installing programs
// program is built as follow "GO111MODULE=off go build ."
// you can control the output of the binary using flag -o.  "GO111MODULE=off go build -o ohms"
// to install a go program run "GO111MODULE=off go install .""

func main() {
	// Accessing program args
	for _, args := range os.Args { // run "go run pakaging.go hello people  in terminal to see output
		fmt.Println(args)
	}
}
