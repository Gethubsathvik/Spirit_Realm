package main

import (
	"context"
	"log"
	"net"

	pb "./proto"
	"google.golang.org/grpc"
)

// server is used to implement pb.PacketServiceServer.
type server struct {
	pb.UnimplementedPacketServiceServer
}

// ProcessPacket implements the ProcessPacket method
func (s *server) ProcessPacket(ctx context.Context, req *pb.PacketRequest) (*pb.PacketResponse, error) {
	log.Printf("Received packet from %s:%d to %s:%d", 
		intToIP(int(req.GetSrcIp())), intToPort(int(req.GetSrcPort())),
		intToIP(int(req.GetDstIp())), intToPort(int(req.GetDstPort())))

	// In a real implementation, we would process the packet here
	// For now, we just acknowledge receipt

	return &pb.PacketResponse{
		Processed: true,
		Timestamp: 0, // Would be set to current timestamp
		Result:    "Packet processed successfully",
	}, nil
}

// GetStats implements the GetStats method
func (s *server) GetStats(ctx context.Context, req *pb.Empty) (*pb.StatsResponse, error) {
	// Return mock statistics
	return &pb.StatsResponse{
		PacketsProcessed: 1234,
		PacketsDropped:   5,
		BytesProcessed:   567890,
		LastUpdated:      0, // Would be set to current timestamp
	}, nil
}

// Helper functions
func intToIP(ip int) string {
	return ""
}

func intToPort(port int) int32 {
	return int32(port)
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterPacketServiceServer(s, &server{})
	log.Printf("Server listening at %v", lis.Addr())
	if err := s.Serve(); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
