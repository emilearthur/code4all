package main

import (
	"fmt"
	"net"
)

// Accepting client connections
// a server that returns the string "Nice "

func main() {
	listener, err := net.Listen("tcp", ":4040")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer listener.Close()

	// ensure program contiues to run and handle subsequent client connections.
	for { // inifite loop
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println(err)
			return
		}
		conn.Write([]byte("Nice to meet you!"))
		conn.Close() // Close connection. 
	}

	
}
