package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	curr "github.com/vladimirvivien/learning-go/ch11/curr1"
)

var currencies = curr.Load("./data.csv")

func currs(resp http.ResponseWriter, req *http.Request) {
	// decode request
	var currRequest curr.CurrencyRequest
	dec := json.NewDecoder(req.Body)
	if err := dec.Decode(&currRequest); err != nil {
		resp.WriteHeader(http.StatusBadRequest)
		fmt.Println(err)
		return
	}
	result := curr.Find(currencies, currRequest.Get)
	// encode data output
	enc := json.NewEncoder(resp)
	if err := enc.Encode(&result); err != nil {
		fmt.Println(err)
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/currency", currs)
	if err := http.ListenAndServe(":4040", mux); err != nil {
		fmt.Println("Error starting Server", err)
	}
}
