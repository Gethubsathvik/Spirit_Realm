#ifndef PACKET_SERVICE_H
#define PACKET_SERVICE_H

#ifdef __cplusplus
extern "C" {
#endif

// Packet data structure
typedef struct {
    unsigned char* data;
    int length;
    unsigned int src_ip;
    unsigned int dst_ip;
    unsigned short src_port;
    unsigned short dst_port;
    unsigned char protocol;
} Packet;

// Analysis result
typedef struct {
    int threat_level;  // 0 = none, 1 = low, 2 = medium, 3 = high
    int is_malicious;  // 0 = false, 1 = true
    char threat_type[64];
    double confidence;  // 0.0 to 1.0
} AnalysisResult;

// Function to analyze a packet for threats
// Returns 0 on success, -1 on error
int analyze_packet(const Packet* packet, AnalysisResult* result);

// Function to initialize the packet inspection module
// Returns 0 on success, -1 on error
int init_packet_inspector();

// Function to cleanup the packet inspection module
void cleanup_packet_inspector();

#ifdef __cplusplus
}
#endif

#endif // PACKET_SERVICE_H