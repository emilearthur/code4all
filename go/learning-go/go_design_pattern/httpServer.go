package main

import (
	"fmt"
	"net/http"
)

type msg string

func (m msg) ServeHTTP(resp http.ResponseWriter, req *http.Request) {
	resp.Header().Add("Content-Type", "text/html")
	resp.WriteHeader(http.StatusOK)
	fmt.Fprint(resp, m)
}

func main() {
	// // defaults
	// msgHandler := msg("Hello from this tiny Server")
	// server := http.Server{Addr: ":4040",
	// 	Handler:      msgHandler,
	// 	ReadTimeout:  time.Second * 5,
	// 	WriteTimeout: time.Second * 5}
	// server.ListenAndServe()

	// applying http.ServeMux
	mux := http.NewServeMux()
	hello := func(resp http.ResponseWriter, req *http.Request) {
		resp.Header().Add("Content-Type", "text/html")
		resp.WriteHeader(http.StatusOK)
		fmt.Fprint(resp, "Hello from this tiny Server")
	}
	goodbye := func(resp http.ResponseWriter, req *http.Request) {
		resp.Header().Add("Content-Type", "text/html")
		resp.WriteHeader(http.StatusOK)
		fmt.Fprint(resp, "Goodbye, See you again!")
	}

	mux.HandleFunc("/hello", hello)
	mux.HandleFunc("/goodbye", goodbye)

	http.ListenAndServe(":4040", mux)

}
