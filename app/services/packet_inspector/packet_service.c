#include "packet_service.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static const unsigned char sql_injection_pattern[] = {
    0x27, 0x20, 0x4f, 0x52, 0x20, 0x31, 0x3d, 0x20, 0x31
};

static int check_sql_injection(const unsigned char* data, int length) {
    if (data == NULL || length <= 0) {
        return 0;
    }
    int pattern_len = sizeof(sql_injection_pattern);
    for (int i = 0; i <= length - pattern_len; i++) {
        int match = 1;
        for (int j = 0; j < pattern_len; j++) {
            if (data[i + j] != sql_injection_pattern[j]) {
                match = 0;
                break;
            }
        }
        if (match) {
            return 1;
        }
    }
    return 0;
}

int analyze_packet(const Packet* packet, AnalysisResult* result) {
    if (packet == NULL || result == NULL) {
        return -1;
    }

    result->threat_level = 0;
    result->is_malicious = 0;
    result->threat_type[0] = '\0';
    result->confidence = 0.0;

    if (packet->data == NULL || packet->length <= 0) {
        return 0;
    }

    if (check_sql_injection(packet->data, packet->length)) {
        result->threat_level = 3;
        result->is_malicious = 1;
        strncpy(result->threat_type, "SQL_INJECTION", sizeof(result->threat_type) - 1);
        result->threat_type[sizeof(result->threat_type) - 1] = '\0';
        result->confidence = 0.95;
        return 0;
    }

    return 0;
}

int init_packet_inspector() {
    printf("Packet inspector initialized\n");
    return 0;
}

void cleanup_packet_inspector() {
    printf("Packet inspector cleaned up\n");
}
