package pb

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// Generated-like minimal stubs for the proto messages and service so the module builds.
// These are intended to behave like protoc output (names/types/getters), but are hand-written
// and minimal. Replace with real generated .pb.go/.pb_grpc.go from protoc when available.

// PacketRequest mirrors the fields in packet.proto.
type PacketRequest struct {
	SourceIp      string
	DestinationIp string
	SourcePort    uint32
	DestinationPort uint32
	Protocol      string
	Data          []byte
	Timestamp     int64
}

func (p *PacketRequest) GetSourceIp() string {
	if p == nil {
		return ""
	}
	return p.SourceIp
}

func (p *PacketRequest) GetDestinationIp() string {
	if p == nil {
		return ""
	}
	return p.DestinationIp
}

func (p *PacketRequest) GetSourcePort() uint32 {
	if p == nil {
		return 0
	}
	return p.SourcePort
}

func (p *PacketRequest) GetDestinationPort() uint32 {
	if p == nil {
		return 0
	}
	return p.DestinationPort
}

// PacketResponse mirrors packet.proto response.
type PacketResponse struct {
	Processed bool
	Timestamp int64
	Result    string
}

// Empty placeholder
type Empty struct{}

// StatsResponse mirrors packet.proto
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

// UnimplementedPacketServiceServer can be embedded for forward compatibility.
type UnimplementedPacketServiceServer struct{}

func (*UnimplementedPacketServiceServer) ProcessPacket(ctx context.Context, req *PacketRequest) (*PacketResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ProcessPacket not implemented")
}

func (*UnimplementedPacketServiceServer) GetStats(ctx context.Context, req *Empty) (*StatsResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetStats not implemented")
}

// RegisterPacketServiceServer is intentionally minimal to satisfy main.go registration call.
// A real generated file registers service descriptors so gRPC can route calls; this shim
// leaves registration as a no-op. Replace with generated registration when available.
func RegisterPacketServiceServer(s grpc.ServiceRegistrar, srv PacketServiceServer) {}
