#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>

int main() {
    const char *filename = "bin/dummy";

    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        perror("open");
        return -1;
    }

    struct stat sb;
    if (fstat(fd, &sb) == -1) {
        perror("fstat");
        close(fd);
        return -1;
    }

    off_t foo_offset = 0x1106; 

    void *file_map = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (file_map == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return -1;
    }

    size_t func_size = 78; 

    void *exec_mem = mmap(NULL, func_size, PROT_EXEC | PROT_READ | PROT_WRITE,
                          MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (exec_mem == MAP_FAILED) {
        perror("mmap");
        munmap(file_map, sb.st_size);
        close(fd);
        return -1;
    }

    memcpy(exec_mem, file_map + foo_offset, func_size);

    munmap(file_map, sb.st_size);
    close(fd);

    (*(void(*)()) exec_mem)();

    munmap(exec_mem, func_size);

    return 0;
}

