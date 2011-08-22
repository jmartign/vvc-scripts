#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>

int main() {
  int maxid, id, shmid;
  struct shm_info shm_info;
  struct shmid_ds shmseg;
  size_t shm_total = 0 ;

  maxid = shmctl(0, SHM_INFO, (struct shmid_ds *) &shm_info) ;

  for (id = 0; id <= maxid; id++) {
    shmid = shmctl(id, SHM_STAT, &shmseg);
    if (shmid < 0) continue;
    if (shmseg.shm_nattch > 0) {
      shm_total += shmseg.shm_segsz;
    }
  }

  printf("Total shared memory in use: %ld\n",shm_total);
  return 0;
}
