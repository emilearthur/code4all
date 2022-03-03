package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
)

// The net package
// the net package is a rich API that handles low-level networking primitives as well as application-level
// protocols such as HTTP. Each logical component of a network is represented by a go type inluding
// hardware interfaces, networks, packaets, addresses, protocols and connections. Further, each type exposes
// magnitude of methods for networking programming suppport for both IPv4 and IPv6.
// addressing --> net package uses string for addressing (i.e. "127.0.0.1"). also can add port to address
// '127.0.0.1:80'. support IPv6 literal addressing "::1" or "[2607:f8b0:4002:c06::65]:80" (i.e.) IPv6 port 80.
// net.Conn Type --> represents a generic connection established between two nodes on the network. It
// implments io.Reader and io.Writer interfaces which allows connected nodes to exchange data using steaming
// IO primitivies.
// Dialing a connection --> client programs use the net.Dail function. uses the signature to connect to a
// host service over the network ==> func Dial(network, address string) (Conn, error). network parameter
// specifies the network protocol for the connection 1. tcp, tcp4, tcp: tcp defaults to tcp4
// 2. udp, udp4, udp6:udp defaults to udp4 3. ip, ip4, ip6:ip defaults to ip4
// 4. unix, unixgram, unixpacket: for Unix domain sockets.

// Listening for incoming connections
// when creating a service program, first step is to announce the port which the service will listen to for
// incoming requests from the network. this is done using the net.Listen function which is
// ==> func Listen(network, laddr string) (net.Listener, error). network parameter specifies the protocol
// with valid values. e.g. "tcp", "tcp4",  "tcp6", "unix" or "unixpacket". laddr parameter is the local
// address and can be specified without an IP address as "":4040". asl you could bound to a specific
// network hardware interface by specifying the network address "10.20.130.240:4040".
// a successful call to the net.Listen function returns a value of the net.Listener type (or
// a non-nil error if it fails). The net.Listener interface exposes methods used to manage the
// life cycle of incoming client connections. Depending on the value of the network parameter
// ("tcp", "tcp4", "tcp6", and so on.), net.Listen will return either a net.TCPListener
// or net.UnixListener, both of which are concrete implementations of the net.Listener
// interface.

// Accepting client connections
// the net.Listener interfaces uses the Accept method to block indefinetely until a new connection arrives
// from a client.

// A TCP API server
// look into tcp.go file. A TCP API server --> code check tcpServer.go
// Connecting to the TCP server with Go.  checks tcpServer.go and tcpServerListenr.go

// The HTTP package
// net/http package provides code to implement both HTTP clients and HTTP servers.

// The http.Client type
// the http.Client struct represents an HTTP client and is used to create HTTP requests and retrieves
// responses from a server.
// http methods:
// Client.Get ==> Get(url string,) (resp *http.Response, err error)
// Client.Post ==> Post(url string, bodyType string, body io.Reader,) (resp *http.Response, err error)
// Client.PostForm ==> PostForm(url string, data url.Values) (resp *http.Response, err error). post method but with key/value pairs
// Client.Head ==> Head(url string,) (resp *http.Response, err error). method that issues HTTP head  method to the remote server specified by the url parameter.
// Client.Do ==> This method generalizes the request and response interaction with a remote HTTP server.

// Handling client requests and responses
// An http.Request value can be explicitly created using the http.NewRequest function. A request value can
// be used to configure HTTP settings, add headers and specify the content body of the request.

// A simple HTTP server
// the HTTP package provides two main components to accept HTTP requests and serve responses:
// * the http.Handler interface ** http.Server type.
// refer to httpserver.go .

// Routing requests with http.ServeMux
// the http.ServeMux handler receives a request associaed with a URL path and it dispatches a function
// that is mapped to the URL.
// refer to httpserver.go .

// A JSON API server
// design goals * User HTTP as the transport protocol ** use JSON for structured communication between
// client and server *** Client query the server for currency information using JSON-formatted requests.
// **** the server respond using JSON-formatted responses.

func main() {
	// dail a 'tcp' network at the host address, www.gutenberg.org:80, which returns a TCP connection of
	// the *net.TCPConn type.
	host, port := "www.gutenberg.org", "80"
	addr := net.JoinHostPort(host, port)
	httpRequest := "GET /cache/epub/16328/pg16328.txt HTTP/1.1\n" + "Host: " + host + "\n\n"

	// connect to server using TCP
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		fmt.Println("Error Connection to: "+addr, err)
		return
	}
	defer conn.Close()

	// sends HTTP request to the server.
	if _, err = conn.Write([]byte(httpRequest)); err != nil {
		fmt.Println(err)
		return
	}

	file, err := os.Create("beowulf.txt")
	if err != nil {
		fmt.Println("Error Creating file: ", err)
		return
	}
	defer file.Close()

	// response is copied to file.
	io.Copy(file, conn)
	fmt.Println("Text copied to file", file.Name())
	fmt.Print("\n")

	// The http.Client type
	// retriveing the text of the Beowulf from Projoect Gutenberg using http.Client type and print content
	client := http.Client{}
	resp, err := client.Get("http://gutenberg.org/cache/epub/16328/pg16328.txt")
	if err != nil {
		fmt.Println("Error Connecting", err)
		return
	}
	defer resp.Body.Close()
	io.Copy(os.Stdout, resp.Body)

	// Using Http instead of Http.Client{}
	resp, err = http.Get("http://gutenberg.org/cache/epub/16328/pg16328.txt")
	if err != nil {
		fmt.Println("Error Connecting", err)
		return
	}
	defer resp.Body.Close()
	io.Copy(os.Stdout, resp.Body)

	// Handling client requests and responses
	clientH := &http.Client{}
	reqH, err := http.NewRequest("GET", "https://www.rfc-editor.org/rfc/rfc7550.txt", nil)
	reqH.Header.Add("Accept", "text/plain")
	reqH.Header.Add("User-Agent", "SampleClient/1.0")

	respH, err := clientH.Do(reqH)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer respH.Body.Close()
	io.Copy(os.Stdout, respH.Body)

}
