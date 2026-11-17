#include <stdio.h> 
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdlib.h>

#define PORT 8932

void send_event(const char *message) {
    int s = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (s < 0)
        exit(-1);
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0) {
        close(s);
        exit(-1);
    }

    send(s, message, strlen(message), 0);
    close(s);
}

int main() {
    while(1) {
        printf("[sudo] password for user: ");
        char input[50];
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = '\0';
        char* pass = "helloworld";

        send_event("1");
        for (int i = 0; i < strlen(pass); i++) {
            sleep(1);
            if (input[i] != pass[i])
                break;
        }
        send_event("0");

        if (strcmp(input, pass) == 0) {
            printf("yey");
            return 0;
        }
    }
}