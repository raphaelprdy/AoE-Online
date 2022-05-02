#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>

#define MAXLINE 1024
#define MAXCLI 3
#define PORT 5001
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
void accept_client(int sockfd, struct sockaddr_in cliaddr, int position, char* bienvenue);
int client_inList(struct sockaddr_in);
void envoie_c(int sockfd, struct sockaddr_in cliaddr);
void afficher_client();
int isListFull(int *position);
char *serialize_client();
int getMyIP(int fd, char* ifname,  u_int32_t * ipaddr);


int main(){

    //declare variables needed
    int sockfd, i, longueur, valread, position;
    int *pos = &position;
    struct sockaddr_in server, cliaddr, python, addr_envoie, serverprincipal;
    char bienvenue[9] = "/liste";
    char conn[18] = "already connected";
    char full[21] = "la partie est pleine";


    //initialize every client to a "null client"
    for(i = 0; i < MAXCLI; i++){
        strncpy(client_struct[i].address, "0.0.0.0", 8);
        client_struct[i].port = 0;
    }

    //create the socket that communicate with python and others c
    sockfd = create_socket(INADDR_ANY, PORT);

    u_int32_t nip;

    getMyIP(sockfd, "eth0", &nip);
    struct in_addr in;
    in.s_addr = nip;
    char *cip = inet_ntoa(in);
    printf("my ip is: %s\n", cip); 


    serverprincipal.sin_family = AF_INET;
    serverprincipal.sin_addr.s_addr = inet_addr("25.45.38.157");
    serverprincipal.sin_port = htons(5001);

    printf("Listening on port %d\n", PORT);

    longueur = sizeof(cliaddr);

    while(1){
        
        printf("\033[31mDébut de boucle\033[37m\n");
        memset(buffer, 0, sizeof(buffer));
        afficher_client();

        if((valread = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&cliaddr, &longueur)) < 0){
            printf("recvfrom failed");
        }
            
        else{
            buffer[strlen(buffer)] = '\0';
            printf("New connection, IP: %s, PORT: %d\n", inet_ntoa(cliaddr.sin_addr), ntohs(cliaddr.sin_port));
            
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
                        sendto(sockfd, conn, sizeof(conn), 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
                    }
                    else if(isListFull(pos)){

                        // si la partie est pleine, prévenir l'utilisateur
                        sendto(sockfd, full, sizeof(full), 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
                    }
                    else{
                        accept_client(sockfd, cliaddr, position, bienvenue);
                    
                    }
                }
            }
            else{
                // le python envoie au c
                if(!strncmp(inet_ntoa(cliaddr.sin_addr), inet_ntoa(python.sin_addr), strlen(inet_ntoa(python.sin_addr)))
                && ntohs(cliaddr.sin_port) == ntohs(python.sin_port)){
                    printf("c'est le python, j'envoie aux autres client c\n");
                    envoie_c(sockfd, cliaddr);
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


void accept_client(int sockfd, struct sockaddr_in cliaddr, int position, char* bienvenue){
    
    struct sockaddr_in addr_envoie;

    // enregistre l'adresse et le port de la socket qui a envoyé le message
    char *address_cli = inet_ntoa(cliaddr.sin_addr);
    int port_cli = htons(cliaddr.sin_port);
    
    printf("J'accepte le client %d ,address : %s, port : %d\n", position, address_cli, port_cli);

    // copie les infos du clients dans la structure
    strncpy(client_struct[position].address, address_cli, strlen(address_cli));
    client_struct[position].address[strlen(address_cli) + 1] = '\0';
    client_struct[position].port = port_cli;

    // prépare l'envoie de l'acquitement
    addr_envoie.sin_addr.s_addr = inet_addr(client_struct[position].address);
    addr_envoie.sin_port = htons(client_struct[position].port);
    addr_envoie.sin_family = AF_INET;

    char *liste = serialize_client();
    char final[50];
    sprintf(final, "%s %s", bienvenue, liste);

    sendto(sockfd, final, strlen(final) + 1, 0, (struct sockaddr *)&addr_envoie, sizeof(addr_envoie));
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

void envoie_c(int sockfd, struct sockaddr_in cliaddr){
    struct sockaddr_in addr_envoie;

    // enregistre l'adresse et le port de la socket qui a envoyé le message
    int port_cli = htons(cliaddr.sin_port);
    char *address_cli = inet_ntoa(cliaddr.sin_addr);
    printf("address : %s, port : %d\n", address_cli, port_cli);

    printf("envoie possible\n");
    for(int i = 0; i < MAXCLI; i++){

        //printf("address : %s, port : %d\n", client_struct[i].address, client_struct[i].port);

        if(strncmp(client_struct[i].address, "0.0.0.0", 8) &&
        (strncmp(client_struct[i].address, address_cli, sizeof(client_struct[i].address)) && (client_struct[i].port != port_cli))){
                    
            // associe les coordonnées du client à la structure qui permettra l'envoie des données
            addr_envoie.sin_addr.s_addr = inet_addr(client_struct[i].address);
            addr_envoie.sin_port = htons(client_struct[i].port);
            addr_envoie.sin_family = AF_INET;

            printf("j'envoie à client: PORT: %d, address: %s\n", ntohs(addr_envoie.sin_port), inet_ntoa(addr_envoie.sin_addr));
                        
            // envoie les données au client par la socket
            sendto(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&addr_envoie, sizeof(addr_envoie));
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
        if(strncmp(client_struct[i].address, "0.0.0.0", strlen("0.0.0.0"))){
            sprintf(ajout, "%s,%d",client_struct[i].address, client_struct[i].port);
            sprintf(liste, "%s %s", liste, ajout);
            memset(ajout, 0, sizeof(ajout));
        }
    }
    printf("serialisé: %s\n", liste);
    return liste;
}


int getMyIP(int fd, char* ifname,  u_int32_t * ipaddr) {
  /* fd: opened file descriptor
   * ifname: if name eg: "eth0"
   */
#define	IFNAMSIZ 16
struct ifreq
{
    char	ifr_name[IFNAMSIZ];
    struct	sockaddr ifr_addr;
};
  struct ifreq ifr;
  memcpy(ifr.ifr_name,ifname,IFNAMSIZ);
  if(ioctl(fd,SIOCGIFADDR,&ifr) == -1){
    perror("getMyIP: ioctl" );
    exit(-1);
}
  memcpy(ipaddr,&ifr.ifr_addr.sa_data[2],4);
  return 0;
}