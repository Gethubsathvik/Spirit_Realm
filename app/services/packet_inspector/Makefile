CC = gcc
CFLAGS = -Wall -Wextra -fPIC -O2
LDFLAGS = -shared
TARGET = libpacket_service.so
SRC = packet_service.c
HDR = packet_service.h

all: $(TARGET)

$(TARGET): $(SRC) $(HDR)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: all clean