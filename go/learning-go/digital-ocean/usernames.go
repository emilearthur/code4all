package main

import (
	"fmt"
	"strings"
)

func main() {
	usernames := map[string]string{"sammy": "sammy-shark", "emile": "emilextrig19"}
	for {
		fmt.Println("Enter a name:")

		var name string
		_, err := fmt.Scanln(&name) // ask of name
		if err != nil {
			panic(err)
		}
		name = strings.TrimSpace(name) // remove space from name

		if u, ok := usernames[name]; ok { // check if name name exits
			fmt.Printf("%q is the username of %q\n", u, name)
			continue // continue the program.
		}
		fmt.Printf("i don't have %v's username, what is it?\n", name) // print name should not exist

		var username string
		_, err = fmt.Scanln(&username) // enter username
		if err != nil {
			panic(err)
		}
		username = strings.TrimSpace(username) // remove space from name
		usernames[name] = username             // update dict with new name.
		fmt.Println("Data updated.")

	}
}
