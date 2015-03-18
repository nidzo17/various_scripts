#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#define MAXREAD 200/* max message length*/

char *encrypt(char *a) {
	char b[200];
	strcpy(b, "Crypted::");
	strcat(b, a);
	//strcat(b, ")");
	return b;
}

char *decrypt(char *a) {
	char b[200];
	strcpy(b, "Decrypted::");
	strcat(b, a);
	//strcat(b, ")");
	return b;
}

int main(void) {
	int pfd[2], dfp[2], namespace, namespace2;
	char choice[2] = "";
	char buf[MAXREAD] = "";
	char message[100] = ""; 

	while(1) {	
		int c;
		while ((c = getchar()) != '\n' && c != EOF);
		printf("Type message: ");
		scanf("%[^\n]s", &message);
		printf("Choose (E)ncrypting ili (D)ecrypting:");
		scanf("%s", &choice);
		if (strcmp(choice,"K")==0) {
			if (pipe(pfd) == -1) /* pipeline creating */
			exit(1);
			if (pipe(dfp) == -1) /* pipeline creating */
			exit(1);
			switch (fork()) {
				case -1: /* child doesn't exist*/
					exit(1);

				case 0: /* child read */
					close(pfd[1]);/* close stdin*/
					(void) read(pfd[0], buf, MAXREAD);
					printf("\nENCRYPTING PROCEDURE\n");
					printf("Received: %s", buf);
					printf("\nSending: %s", encrypt(buf));
					close(dfp[0]); 
					(void) write(dfp[1], encrypt(buf), strlen(buf) + 13);
					exit(0);

				default: /* parent write */
					close(pfd[0]); /* close stdout*/
					(void) write(pfd[1], message, strlen(message) + 1);
					wait(NULL);
					close(dfp[1]);
					(void) read(dfp[0], buf, MAXREAD);
					printf("\n\nMaster received: %s\n\n", buf);
				}
			}

		else if (strcmp(choice,"D")==0) {
			
			unlink("./pipeline");
			unlink("./pipeline2");
		
			if (mknod("./pipeline", S_IFIFO | 00600, 0)==-1)
				exit(1);
			if (mknod("./pipeline2", S_IFIFO | 00600, 0)==-1)
				exit(1);

			switch (fork()) {
			case -1: /* child doesn't exist*/
				exit(1);

			case 0: /* child read */
				namespace = open("./pipeline", O_RDONLY);
				namespace2 = open("./pipeline", O_WRONLY);
				(void) read(namespace, buf, MAXREAD);
				printf("\nDECRYPTING PROCEDURE\n");
				printf("Received: %s", buf);
				printf("\nSending: %s", decrypt(buf));
				(void) write(namespace2, decrypt(buf), strlen(buf) + 15);
				exit(0);

			default: /* parent write */
				namespace = open("./pipeline", O_WRONLY);
				(void) write(namespace, message, strlen(message) + 1);
				wait(NULL);
				namespace2 = open("./pipeline", O_RDONLY);
				(void) read(namespace2, buf, MAXREAD);
				printf("\n\nMaster received: %s\n\n", buf);
			}
		}
		else {
			printf("Choose E for encrypting or D for decrypting:");
		}
	
	}
	exit(0);/* close all descriptors */
}

