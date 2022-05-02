#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAXLINE 1024
#define SERVER "192.168.11.128"
#define MAXCLI 3
#define PORT 5005
#define TRUE 1
#define FALSE 0


typedef struct{
    int port;
    char address[50];
}client;


client client_struct[MAXCLI];
char buffer[MAXLINE + 1];
int acceptPossible = FALSE;
int envoiePossible = FALSE;



void stop(char *msg);
int create_socket(char *address, int port);
void enregistrer_client_python(struct sockaddr_in *python, struct sockaddr_in *cliaddr);
void accept_client(int sockfd, struct sockaddr_in cliaddr, int position);
int client_inList(struct sockaddr_in);
void envoie_c(int sockfd, struct sockaddr_in cliaddr, char *message);
void afficher_client();
int isListFull(int *position);
char *serialize_client();
void enregistrer_autres_c(int *pos);


int main(){

    //declare variables needed
    int sockfd, i, longueur, valread, position;
    int *pos = &position;
    struct sockaddr_in server, cliaddr, python, addr_envoie, serverprincipal;
    char connect[9] = "/connect";
    char conn[18] = "already connected";
    char full[21] = "la partie est pleine";


    //initialize every client to a "null client"
    for(i = 0; i < MAXCLI; i++){
        strncpy(client_struct[i].address, "0.0.0.0", 8);
        client_struct[i].port = 0;
    }

    //create the socket that communicate with python and others c
    sockfd = create_socket(INADDR_ANY, PORT);

    serverprincipal.sin_family = AF_INET;
    serverprincipal.sin_addr.s_addr = inet_addr("192.168.11.128");
    serverprincipal.sin_port = htons(5001);


    

    printf("Listening on port %d\n", PORT);

    longueur = sizeof(cliaddr);

    //pour initier la connection
    sendto(sockfd, connect, strlen(connect) + 1, 0, (struct sockaddr *)&serverprincipal, sizeof(serverprincipal));

    while(1){
        
        printf("\033[31mDébut de boucle\033[37m\n");
        memset(buffer, 0, sizeof(buffer));
        afficher_client();

        if((valread = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&cliaddr, &longueur)) < 0){
            printf("recvfrom failed");
        }
            
        else{
            //buffer[strlen(buffer) + 1] = '\0';
            printf("New connection, IP: %s, PORT: %d\n", inet_ntoa(cliaddr.sin_addr), ntohs(cliaddr.sin_port));
            printf("buffer: %s\n", buffer);
            if(!strncmp(buffer, "/connect", strlen("/connect"))){
                // c'est notre python
                if(!strncmp(inet_ntoa(cliaddr.sin_addr), "127.0.0.1", strlen("127.0.0.1"))){
                    enregistrer_client_python(&python, &cliaddr);
                    printf("client python: address: %s, port: %d\n", inet_ntoa(python.sin_addr), htons(python.sin_port));
                }
                // c'est un client c
                else{
                    //le client est déjà enregistré
                    if(client_inList(cliaddr)){
                        //continue;
                        sendto(sockfd, conn, sizeof(conn), 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
                    }
                    else if(isListFull(pos)){

                        // si la partie est pleine, prévenir l'utilisateur
                        sendto(sockfd, full, sizeof(full), 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
                    }
                    else{
                        accept_client(sockfd, cliaddr, position);
                    
                    }
                }
            }
            else if(!strncmp(buffer, "/liste", strlen("/liste"))){
                printf("le serveur principal m'envoie la liste des clients\n");
                accept_client(sockfd, cliaddr, position);
                enregistrer_autres_c(pos);
                envoie_c(sockfd, cliaddr, connect);
            }
            else{
                // le python envoie au c
                if(!strncmp(inet_ntoa(cliaddr.sin_addr), inet_ntoa(python.sin_addr), strlen(inet_ntoa(python.sin_addr)))
                && ntohs(cliaddr.sin_port) == ntohs(python.sin_port)){
                    printf("c'est le python, j'envoie aux autres client c\n");
                    envoie_c(sockfd, cliaddr, buffer);
                }
                // un c envoie au python
                else if(client_inList(cliaddr)){
                    printf("c'est un client c, j'envoie au python\n");
                    sendto(sockfd, buffer, strlen(buffer) + 1, 0, (struct sockaddr *)&python, sizeof(python));
                }
            }           
        }
    }    
}


void stop(char *msg){
    perror(msg);
    exit(EXIT_FAILURE);
}


int create_socket(char *address, int port){
    //create the socket that communicate with python and others c
    int sockfd;
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    //type of socket created
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY; // "0.0.0.0"
    server.sin_port = htons(PORT);

    //bind the socket to localhost port 5000
    if(bind(sockfd, (struct sockaddr *) &server, sizeof(server)) < 0){
        stop("bind failed");
    }

    return sockfd;
}


void enregistrer_client_python(struct sockaddr_in *python, struct sockaddr_in *cliaddr){
    char *address_cli = inet_ntoa(cliaddr->sin_addr);
    python->sin_addr.s_addr = inet_addr(address_cli);
    python->sin_port = cliaddr->sin_port;
    python->sin_family = AF_INET;
}


void accept_client(int sockfd, struct sockaddr_in cliaddr, int position){
    
    struct sockaddr_in addr_envoie;

    // enregistre l'adresse et le port de la socket qui a envoyé le message
    char *address_cli = inet_ntoa(cliaddr.sin_addr);
    int port_cli = htons(cliaddr.sin_port);
    
    printf("J'accepte le client %d ,address : %s, port : %d\n", position, address_cli, port_cli);

    // copie les infos du clients dans la structure
    strncpy(client_struct[position].address, address_cli, strlen(address_cli));
    client_struct[position].address[strlen(address_cli) + 1] = '\0';
    client_struct[position].port = port_cli;
}


int client_inList(struct sockaddr_in cliaddr){
    for(int i = 0; i < MAXCLI; i++){

        // regarde si la socket n'est pas dans la liste de client, si c'est le cas quitte la boucle
        if((!strncmp(client_struct[i].address, inet_ntoa(cliaddr.sin_addr), sizeof(inet_ntoa(cliaddr.sin_addr)))
        && (client_struct[i].port == htons(cliaddr.sin_port)))){
            return 1;
            printf("client déjà enregistré\n");
            break;
        }
    }
    return 0;
}


int client_AP_inList(char *address, int port){
    for(int i=0; i < MAXCLI; i++){
        if(!strncmp(client_struct[i].address, address, sizeof(address)) && (client_struct[i].port == port)){
            return 1;
        }
    }
    return 0;
}


void envoie_c(int sockfd, struct sockaddr_in cliaddr, char *message){
    struct sockaddr_in addr_envoie;

    // enregistre l'adresse et le port de la socket qui a envoyé le message
    int port_cli = htons(cliaddr.sin_port);
    char *address_cli = inet_ntoa(cliaddr.sin_addr);
    printf("address : %s, port : %d\n", address_cli, port_cli);

    printf("envoie possible\n");
    for(int i = 0; i < MAXCLI; i++){

        //printf("address : %s, port : %d\n", client_struct[i].address, client_struct[i].port);

        if(strncmp(client_struct[i].address, "0.0.0.0", 8) &&
        (strncmp(client_struct[i].address, address_cli, sizeof(client_struct[i].address)) || (client_struct[i].port != port_cli))){
                    
            // associe les coordonnées du client à la structure qui permettra l'envoie des données
            addr_envoie.sin_addr.s_addr = inet_addr(client_struct[i].address);
            addr_envoie.sin_port = htons(client_struct[i].port);
            addr_envoie.sin_family = AF_INET;

            printf("j'envoie à client: PORT: %d, address: %s\n", ntohs(addr_envoie.sin_port), inet_ntoa(addr_envoie.sin_addr));
                        
            // envoie les données au client par la socket
            sendto(sockfd, message, strlen(message) + 1, 0, (struct sockaddr *)&addr_envoie, sizeof(addr_envoie));
        }
    }
}


void afficher_client(){
    printf("            \033[33mListe des clients\033[37m\n");
    for(int i = 0; i < MAXCLI; i++){
        if(strncmp(client_struct[i].address, "0.0.0.0", 7)){
            printf("client %d, address : %s, port : %d \n", i, client_struct[i].address, client_struct[i].port);
        }
    }
    printf("\033[33m********************************************************\033[37m\n");
}


int isListFull(int *pos){
    for(int i = 0; i < MAXCLI; i++){
        if(!strncmp(client_struct[i].address, "0.0.0.0", 7)){
            *pos = i;
            printf("position : %d\n", *pos);
            return 0;
        }
    }
    return 1;
}


char *serialize_client(){
    char *liste = malloc(MAXCLI * sizeof(client));
    char ajout[100];
    memset(ajout, 0, sizeof(ajout));
    memset(liste, 0, sizeof(liste));
    for(int i = 0; i < MAXCLI; i++){
        if(strncmp(client_struct[i].address, "0.0.0.0", strlen("0.0.0.0") + 1)){
            sprintf(ajout, "%s,%d ",client_struct[i].address, client_struct[i].port);
            strncat(liste, ajout, strlen(ajout) + 1);
        }
    }
    printf("serialisé: %s\n", liste);
    return liste;
}


void enregistrer_autres_c(int *pos){

    char **coords_cli = malloc(MAXCLI * sizeof(client));
    memset(coords_cli, 0, sizeof(coords_cli));
    char delim[2] = " ";
    int position = 0;
    char *token;
    token = strtok(buffer, delim);

    for (token = strtok(NULL, delim); token; token = strtok(NULL, delim)){
        //printf("token=%s\n", token);
        coords_cli[position] = token;
        position++;
    }
    // traite chaque address,port
    for(int i = 0; i < MAXCLI; i++){
        if(coords_cli[i] != NULL){

            // separate adress and port
            char *address;
            int port;
            address = strtok(coords_cli[i], ",");
            port = atoi(strtok(NULL, ","));
            printf("strtok: address: %s, port: %d\n", address, port);  


            if(strncmp(address, SERVER, strlen(SERVER)) || port != PORT){
                if(!isListFull(pos)){
                    printf("liste non pleine\n");
                    // si le client n'est pas dans la liste
                    if(!client_AP_inList(address, port)){
                        printf("le client n'est pas dans la liste\n");
                        strncpy(client_struct[*pos].address, address, strlen(address) + 1);
                        client_struct[*pos].port = port;
                        printf("j'accepte le client %d\n", *pos);
                        break;
                    }
                } 
            }        
        }
    }
}