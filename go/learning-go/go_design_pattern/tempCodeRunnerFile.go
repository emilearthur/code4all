// The http.Client type
	// // retriveing the text of the Beowulf from Projoect Gutenberg using http.Client type and print content
	// client := http.Client{}
	// resp, err := client.Get("http://gutenberg.org/cache/epub/16328/pg16328.txt")
	// if err != nil {
	// 	fmt.Println("Error Connecting", err)
	// 	return
	// }
	// defer resp.Body.Close()
	// io.Copy(os.Stdout, resp.Body)

	// // Using Http instead of Http.Client{}
	// resp, err = http.Get("http://gutenberg.org/cache/epub/16328/pg16328.txt")
	// if err != nil {
	// 	fmt.Println("Error Connecting", err)
	// 	return
	// }
	// defer resp.Body.Close()
	// io.Copy(os.Stdout, resp.Body)