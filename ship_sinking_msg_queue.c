// Ship sinking simulator using message queues.

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <signal.h>

struct my_msgbuf {
    long mtype;
    char mtext[200];
};

int msqid;

void retreat(int failure) {
    if (msgctl(msqid, IPC_RMID, NULL) == -1) {
        perror("msgctl");
        exit(1);
    }
    exit(0);
}

int main(void) {

    struct my_msgbuf buf;
    key_t key;
    char text[]="";

    key = 12341;
    
    if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1) { /* connect to the queue */
        perror("msgget");
        exit(1);
    }
    //memcpy(buf.mtext, text, strlen(text)+1);

    char array[4][4] = { {'-','o','-','-'}, {'-', 'o', '-','-'}, {'-', '-', '-', '-'}, {'-', 'o', 'o', '-'} };
    int coord[2] = {0};
    int cnt = 0;

    sigset(SIGINT, retreat);
    
    int i,j;
    for (i=0; i < 4; i++) {
    	for (j=0; j < 4; j++)
    		printf("%c ", array[i][j]);
    	printf ("\n");
    }

    while(1) {

    	if (msgrcv(msqid, (struct msgbuf *)&buf, sizeof(buf), 0, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }

        printf("\nShooting on filed: %s", buf.mtext);
        coord[0] = atoi(&buf.mtext[0]);
        coord[1] = atoi(&buf.mtext[2]);
        if (array[coord[0]][coord[1]] == 'o') {
        	cnt++;
        	if (cnt == 4) {
        		strcpy(buf.mtext, "You win");
        	    buf.mtype = 1;
        	    if (msgsnd(msqid, (struct msgbuf *)&buf, sizeof(buf), 0) == -1)
        	    	perror("msgsnd");
        		printf("You lose\n");
        		printf("Press any key ...\n");
        		getchar();
        		retreat(1);
        	}
        	else {
        	strcpy(buf.mtext, "BINGO");
        	printf("BINGO\n");
        	}
        }
        else {
        	strcpy(buf.mtext, "miss");
        	printf("miss\n");
        }
        buf.mtype = 1;

        if (msgsnd(msqid, (struct msgbuf *)&buf, sizeof(buf), 0) == -1)
                    perror("msgsnd");


        printf("FIRE ");
        buf.mtype = 1;
        fgets (text, 100, stdin);
        memcpy(buf.mtext, text, strlen(text)+1);

        if (msgsnd(msqid, (struct msgbuf *)&buf, sizeof(buf), 0) == -1)
                    perror("msgsnd");

    	if (msgrcv(msqid, (struct msgbuf *)&buf, sizeof(buf), 0, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }
    	if (strncmp(buf.mtext, "You win", 7) == 0) {
    		printf("%s\n", buf.mtext);
    		printf("Press any key ...\n");
    		getchar();
    		retreat(1);
    	}
    	else {
    		printf("%s\n", buf.mtext);
    	}
    }
    return 0;
}


