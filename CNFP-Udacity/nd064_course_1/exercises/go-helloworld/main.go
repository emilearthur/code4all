package main

import (
	"fmt"
	"net/http"
)

func helloWorld(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello World")
}

func healthstatus(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "result: Ok - healthy")
}

func metrics(w http.ResponseWriter, r *http.Request) {
	response := `"status:status", "code:0", "data:{"UserCount": 140, "UserCountActive": 23}"`
	fmt.Fprintf(w, response)
}

func main() {
	http.HandleFunc("/", helloWorld)
	http.HandleFunc("/status", healthstatus)
	http.HandleFunc("/metrics", metrics)
	http.ListenAndServe(":6112", nil)
}
