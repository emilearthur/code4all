package main

import (
	"fmt"
	"sort"
)

func main() {
	var maxUint32 uint32 = 4294967295 // + 1 raises an error // Max uint32 size
	fmt.Println(maxUint32)
	myBool := 5 > 8 // boolean
	fmt.Println(myBool)
	a := `Say "hello" to Go!`
	fmt.Println(a)
	b := `Say "hello" to Go!\n` // backslash has no special meaning inside of raw string literals
	fmt.Println(b)
	c := `
	This string is on 
	multiple line
	within a singe back
	quote on either side.`
	fmt.Println(c)
	d := "say \"hello\" to go!" // string li
	fmt.Println(d)
	fmt.Println()

	// go support UTF-8 characters
	k := "Hello, 世界"
	for i, c := range k { // loop in go. in python would have been for i,c in enumerate(k)
		fmt.Printf("%d: %s\n", i, string(c))
	}
	fmt.Println("lenght of 'Hello, 世界': ", len(k))
	fmt.Println()

	fmt.Println("floats")
	var pi float64 = 3.14
	var week float64 = 7
	fmt.Println(pi, week)
	fmt.Println()

	fmt.Println("Array")
	coral := [3]string{"blue coral", "staghorn coral", "pillar coral"} // array
	// [3] => number of elements in array, string => data type in array, {} => array
	fmt.Println(coral)
	fmt.Println()

	fmt.Println("Slices")
	nums := []int{-3, -2, -1, 0, 1, 2, 3} // slices of array. Slices are dynamic and not fixed length size.
	flts := []float64{3.14, 9.23, 111.11, 312.12, 1.05}
	seaCreatures := []string{"shark", "cuttlefish", "squid", "mantis shrimp"}
	fmt.Println(nums)
	fmt.Println(flts)
	fmt.Println(seaCreatures)
	seaCreatures = append(seaCreatures, "seahorse") // adding item to a slice
	fmt.Println(seaCreatures)
	fmt.Println()

	/*
		Maps: maps is hash or dictionary type. Maps use keys and values as a pair to store data.
		key and values pairs are used to loop values by index or key.
		map[key]value{}
		e.g. map[string]string{"name": "Sammy", "animal": "shark", "color": "blue", "location": "ocean"}
		keys are comparable types; are primitive types like strings, ints, etc.
		primitive types is defined by the language and not built from combining any other types.
		while they can be user-defined type, its considered best practice to keep them simple to avoid prog. errors.
		keys in eg above are name, animal, color and location.
	*/
	sammy := map[string]string{"name": "Sammy", "animal": "shark", "color": "blue", "location": "ocean"}
	fmt.Println(sammy)
	fmt.Println(sammy["color"]) // getting key from dict.

	for key, value := range sammy { // iterating the key, value dict.
		fmt.Printf("%q is the key for the value %q\n", key, value)
	}

	keys := []string{}
	for key := range sammy { // getting key from dict and appending to keys list.
		keys = append(keys, key)
	}
	sort.Strings(keys) // sort string
	fmt.Printf("keys are: %q", keys)
	fmt.Println()

	// The make built-in function allocates and initializes an object of type slice, map, or chan (only).
	items := make([]string, len(sammy)) // The make function allocates a zeroed array and returns a slice that refers to that array
	var i int
	for _, v := range sammy {
		items[i] = v
		i++
	}
	fmt.Printf("%q", items)
	fmt.Println()

	counts := map[string]int{}
	fmt.Println(counts["sammy"])

	if count, ok := counts["sammy"]; ok {
		fmt.Printf("Sammy has a count of %d\n", count)
	} else {
		fmt.Println("Sammy was not found")
	}

	usernames := map[string]string{"Sammy": "sammy-shark", "Jamie": "mantisshrimp54"}
	usernames["Drew"] = "squidly"
	fmt.Printf ("%q", usernames)
	fmt.Println()

	followers := map[string]int{"drew": 300, "mary": 428, "cindy": 911}
	followers["drew"] = 360
	fmt.Println(followers)

	permissions := map[int]string{1: "read", 2: "write", 4: "delete", 8: "create", 16: "modify"}
	delete(permissions, 16) // deleting value from a dict.
	fmt.Println(permissions)

}
