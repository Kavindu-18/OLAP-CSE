 package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"time"

	"github.com/segmentio/kafka-go"
)

// The Data Model
type Trade struct {
	Symbol    string  `json:"symbol"`
	Price     float64 `json:"price"`
	Volume    int     `json:"volume"`
	Timestamp string  `json:"timestamp"`
}

var companies = []string{"JKH", "SAMP", "COMB", "HNB", "DIAL"}

func main() {
	// 1. Connect to Kafka (running on localhost:9092)
	writer := &kafka.Writer{
		Addr:     kafka.TCP("localhost:9092"),
		Topic:    "cse_trades",
		Balancer: &kafka.LeastBytes{},
	}
	defer writer.Close()

	fmt.Println("🚀 Starting Real-Time Trade Stream...")

	for {
		// 2. Generate Random Trade
		trade := Trade{
			Symbol:    companies[rand.Intn(len(companies))],
			Price:     50.0 + rand.Float64()*150.0, // Price between 50 and 200
			Volume:    rand.Intn(1000) + 1,
			Timestamp: time.Now().Format(time.RFC3339),
		}

		tradeJSON, _ := json.Marshal(trade)

		// 3. Write to Kafka
		err := writer.WriteMessages(context.Background(),
			kafka.Message{
				Key:   []byte(trade.Symbol), // Key ensures order per stock
				Value: tradeJSON,
			},
		)

		if err != nil {
			log.Printf("Failed to write message: %v", err)
		} else {
			fmt.Printf("Sent: %s - %.2f\n", trade.Symbol, trade.Price)
		}

		// 4. Sleep to simulate real-time (2 trades per second)
		time.Sleep(500 * time.Millisecond)
	}
}