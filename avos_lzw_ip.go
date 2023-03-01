package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "log"
    
)

func splitBits(b1, b2, b3 int64) (int64, int64) {
	// Convert n2 to binary string representation
	binStr1 := strconv.FormatInt(int64(b1), 2)
	binStr2 := strconv.FormatInt(int64(b2), 2)
	binStr3 := strconv.FormatInt(int64(b3), 2)

	// Pad the binary string with leading zeros to ensure it has an even length
	if len(binStr2)%2 != 0 {
		binStr2 = "0" + binStr2
	}

	// Split the binary string in half
	half := len(binStr2) / 2
	firstHalf := binStr2[:half]
	secondHalf := binStr2[half:]

    binStr1 += firstHalf
    binStr3 = secondHalf + binStr3
    r1, err1 := strconv.ParseInt(binStr1, 2, 64)
    r2, err2 := strconv.ParseInt(binStr3, 2, 64)
    fmt.Println(r1)
    if err1 != nil || err2 != nil{
        log.Fatal(err1)
    }
    return r1, r2


}


func main() {
    var file string
    fmt.Print("Enter a string: ")
    fmt.Scanln(&file)
    inputFile, err := os.Open(file)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error opening input file: %v\n", err)
        os.Exit(1)
    }
    defer inputFile.Close()

    // read in the compressed data from the file
    scanner := bufio.NewScanner(inputFile)
    scanner.Split(bufio.ScanBytes)
    compressedData := make([]byte, 0)
    for scanner.Scan() {
        compressedData = append(compressedData, scanner.Bytes()...)
    }

    fmt.Print(compressedData)
    // initialize the dictionary with all possible one-byte values
    dictionary := make(map[int]string)
    for i := 0; i < 256; i++ {
        dictionary[i] = string(i)
    }

    fmt.Print(splitBits(int64(compressedData[0]), int64(compressedData[1]), int64(compressedData[2])))

    // create a new array to store the results
    var compressedDataMerged []int64

    // iterate through the array in steps of 3
    for i := 0; i < len(compressedData); i += 3 {
        // call the splitBytes function with 3 consecutive elements
        res1, res2 := splitBits(int64(compressedData[i]), int64(compressedData[i+1]), int64(compressedData[i+2]))
        // append the results to the new array
        compressedDataMerged = append(compressedDataMerged, make([]int64,res1)...)
        compressedDataMerged = append(compressedDataMerged, make([]int64,res2)...)
    }

    // print the results
    fmt.Println(compressedDataMerged)

    // decode the compressed data using the LZW algorithm
    var result string
    var prevCode int
    for _, currByte := range compressedData {
        currCode := int(currByte)
        if value, ok := dictionary[currCode]; ok {
            result += value
            if prevCode != -1 {
                dictionary[len(dictionary)] = dictionary[prevCode] + value[:1]
            }
            prevCode = currCode
        } else {
            result += dictionary[prevCode] + dictionary[prevCode][:1]
            dictionary[len(dictionary)] = dictionary[prevCode] + dictionary[prevCode][:1]
            prevCode = -1
        }
    }

    // output the decoded data to standard output
    fmt.Println(result)
}
