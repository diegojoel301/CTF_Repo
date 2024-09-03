package main

import (
	"os"
	"time"
  "fmt"
	"plaidctf.com/pppvm/pppvm"
)

const CODE_SIZE = 0x4000
const TIMEOUT = 5 * time.Second

func main() {
	code := make([]byte, CODE_SIZE)
	totalRead := 0
	fmt.Println(code);

	for totalRead < CODE_SIZE {

		n, err := os.Stdin.Read(code[totalRead:])
							fmt.Println("Sexo anal");

		if err != nil {
			panic(err.Error())
		}
		totalRead += n
	}
	fmt.Println("Creando VM");

	vm := pppvm.NewVM()
	vm.Launch(code)
	time.Sleep(TIMEOUT)
}
