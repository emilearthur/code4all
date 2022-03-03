package main

import (
	"bufio"
	"fmt"
	"net"
	"time"
)

var hostI, portI = "127.0.0.1", "4040"
var addrI = net.JoinHostPort(hostI, portI)
var deadline = time.Now().Add(time.Millisecond * 700)

const prompt = "curr"
const buffLen = 1024

func main() {
	// A TCP API server --> code check tcpServer.go

	// Connecting to the TCP server with Go
	// Name sure tcpServer.go is runs before.

	connC, err := net.Dial("tcp", addrI)
	if err != nil {
		fmt.Println("Error Connecting", err)
		return
	}
	defer connC.Close()
	fmt.Println("Connected to Global Currency Service")
	var cmd, param string

	// repl - interactive shell for client
	for {
		fmt.Print(prompt, "> ")
		_, err = fmt.Scanf("%s %s", &cmd, &param) // scan for input
		if err != nil {
			fmt.Println("Usage: GET <search string or *>")
			continue
		}
		// send command line.
		cmdLine := fmt.Sprintf("%s %s", cmd, param)
		if n, err := connC.Write([]byte(cmdLine)); n == 0 || err != nil {
			fmt.Println(err)
			return
		}

		// stream and display response
		connC.SetReadDeadline(time.Now().Add(time.Second * 5000))

		// for {
		// 	buff := make([]byte, buffLen)
		// 	n, err := connC.Read(buff) // read output
		// 	if err != nil {
		// 		break
		// 	}
		// 	fmt.Print(string(buff[0:n]))
		// 	connC.SetReadDeadline(time.Now().Add(time.Millisecond * 700))
		// }

		// streaming the incoming bytes from the sever using buffer IO.
		conbuf := bufio.NewReaderSize(connC, buffLen)
		for {
			str, err := conbuf.ReadString('\n')
			if err != nil {
				break
			}
			fmt.Print(str)
			connC.SetReadDeadline(time.Now().Add(time.Millisecond * 700))
		}
	}

}
