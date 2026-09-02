package pb

import (
	"context"
	"google.golang.org/grpc"
)

// Minimal, hand-written stubs to satisfy builds until real generated protobuf code is added.
// These replicate only the symbols used by app/services/packet_service/main.go.

// PacketRequest is a minimal request type with getters used by main.go.
type PacketRequest struct {
	SrcIp  int32
	SrcPort int32
	DstIp  int32
	DstPort int32
}

func (p *PacketRequest) GetSrcIp() int32 {
	if p == nil {
		return 0
	}
	return p.SrcIp
}

func (p *PacketRequest) GetSrcPort() int32 {
	if p == nil {
		return 0
	}
	return p.SrcPort
}

func (p *PacketRequest) GetDstIp() int32 {
	if p == nil {
		return 0
	}
	return p.DstIp
}

func (p *PacketRequest) GetDstPort() int32 {
	if p == nil {
		return 0
	}
	return p.DstPort
}

// PacketResponse is the response type expected by main.go.
type PacketResponse struct {
	Processed bool
	Timestamp int64
	Result    string
}

// Empty is a placeholder for an empty request.
type Empty struct{}

// StatsResponse is the response type expected by main.go.
type StatsResponse struct {
	PacketsProcessed uint64
	PacketsDropped   uint64
	BytesProcessed   uint64
	LastUpdated      int64
}

// PacketServiceServer is the server API for PacketService.
type PacketServiceServer interface {
	ProcessPacket(ctx context.Context, req *PacketRequest) (*PacketResponse, error)
	GetStats(ctx context.Context, req *Empty) (*StatsResponse, error)
}

// UnimplementedPacketServiceServer can be embedded to have forward compatible implementations.
type UnimplementedPacketServiceServer struct{}

func (*UnimplementedPacketServiceServer) ProcessPacket(ctx context.Context, req *PacketRequest) (*PacketResponse, error) {
	return nil, grpc.Errorf(grpc.Code(), "method ProcessPacket not implemented")
}

func (*UnimplementedPacketServiceServer) GetStats(ctx context.Context, req *Empty) (*StatsResponse, error) {
	return nil, grpc.Errorf(grpc.Code(), "method GetStats not implemented")
}

// RegisterPacketServiceServer is a minimal registration function used by main.go.
// It intentionally does nothing — for a real server, generate code from the .proto and use that.
func RegisterPacketServiceServer(s grpc.ServiceRegistrar, srv PacketServiceServer) {}
