package pb

import (
	"context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// Generated-like protobuf and gRPC bindings for packet.proto.
// These are hand-written but follow the layout protoc generates so builds succeed
// and gRPC registration works. Replace with true protoc output when available.

// Messages
type PacketRequest struct {
	SourceIp        string
	DestinationIp   string
	SourcePort      uint32
	DestinationPort uint32
	Protocol        string
	Data            []byte
	Timestamp       int64
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

type PacketResponse struct {
	Processed bool
	Timestamp int64
	Result    string
}

type Empty struct{}

type StatsResponse struct {
	PacketsProcessed uint64
	PacketsDropped   uint64
	BytesProcessed   uint64
	LastUpdated      int64
}

// Service interface
type PacketServiceServer interface {
	ProcessPacket(ctx context.Context, req *PacketRequest) (*PacketResponse, error)
	GetStats(ctx context.Context, req *Empty) (*StatsResponse, error)
}

// Unimplemented server
type UnimplementedPacketServiceServer struct{}

func (*UnimplementedPacketServiceServer) ProcessPacket(ctx context.Context, req *PacketRequest) (*PacketResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ProcessPacket not implemented")
}

func (*UnimplementedPacketServiceServer) GetStats(ctx context.Context, req *Empty) (*StatsResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetStats not implemented")
}

// Register helper
func RegisterPacketServiceServer(s grpc.ServiceRegistrar, srv PacketServiceServer) {
	s.RegisterService(&PacketService_ServiceDesc, srv)
}

// gRPC handlers (match protoc-generated shape)
func _PacketService_ProcessPacket_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	req := new(PacketRequest)
	if err := dec(req); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PacketServiceServer).ProcessPacket(ctx, req)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/packet.PacketService/ProcessPacket",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PacketServiceServer).ProcessPacket(ctx, req.(*PacketRequest))
	}
	return interceptor(ctx, req, info, handler)
}

func _PacketService_GetStats_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	req := new(Empty)
	if err := dec(req); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PacketServiceServer).GetStats(ctx, req)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/packet.PacketService/GetStats",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PacketServiceServer).GetStats(ctx, req.(*Empty))
	}
	return interceptor(ctx, req, info, handler)
}

// Service descriptor
var PacketService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "packet.PacketService",
	HandlerType: (*PacketServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "ProcessPacket",
			Handler:    _PacketService_ProcessPacket_Handler,
		},
		{
			MethodName: "GetStats",
			Handler:    _PacketService_GetStats_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "packet.proto",
}
