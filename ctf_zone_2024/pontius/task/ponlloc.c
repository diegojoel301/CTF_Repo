#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stddef.h>

struct poncache_chunk_struct
{
    struct poncache_chunk_struct* left;
    struct poncache_chunk_struct* right;
    size_t chunk_size;
    size_t data_size;
    size_t is_free;
    char data[1];
} typedef poncache_chunk;

poncache_chunk arena;
void* heap_addr = 0;
void* top_chunk = 0;

#define GET_REAL_SIZE(x) (x + sizeof(poncache_chunk)) & (~sizeof(size_t) + 1)
#define HEADER_SIZE (sizeof(poncache_chunk) - sizeof(size_t))
#define HEAP_SIZE 0x21000

poncache_chunk* find_chunk_by_size(size_t size)
{
    poncache_chunk* prev_chunk = &arena;
    poncache_chunk* current_chunk = &arena;
    while (current_chunk && current_chunk->chunk_size != size)
    {
        if (current_chunk != prev_chunk)
            prev_chunk = current_chunk;

        if (size >= current_chunk->chunk_size)
            current_chunk = current_chunk->right;
        else
            current_chunk = current_chunk->left;
    }
    if (!current_chunk) return prev_chunk;
    return current_chunk;
}

void* ponlloc(size_t size)
{
    if (size > 0x420)
        return (void*)-2;
    if (!heap_addr)
    {
        heap_addr = mmap(0, HEAP_SIZE, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
        top_chunk = heap_addr;
    }
    size_t chunk_size = GET_REAL_SIZE(size);
    poncache_chunk* found_chunk = find_chunk_by_size(chunk_size);
    if (found_chunk->data_size == size && !found_chunk->is_free)
        return (void*)-1;
    if (found_chunk->data_size == size)
    {
        found_chunk->is_free = 0;
        return (char*)found_chunk + HEADER_SIZE;
    }
    if (chunk_size + top_chunk > heap_addr + HEAP_SIZE)
        return (void*)-3;
    if (chunk_size >= found_chunk->chunk_size)
        found_chunk->right = (poncache_chunk*)top_chunk;
    else
        found_chunk->left = (poncache_chunk*)top_chunk;
    poncache_chunk* new_chunk = (poncache_chunk*)top_chunk;
    top_chunk = (char*)top_chunk + chunk_size;
    new_chunk->left = 0;
    new_chunk->right = 0;
    new_chunk->chunk_size = chunk_size;
    new_chunk->data_size = size;
    new_chunk->is_free = 0;
    return (void*)((char*)new_chunk + HEADER_SIZE);
}

void ponfree(void* chunk)
{
    size_t chunk_size = *((size_t*)(chunk + offsetof(poncache_chunk, chunk_size) - offsetof(poncache_chunk, data)));
    poncache_chunk* found_chunk = find_chunk_by_size(chunk_size);
    if (found_chunk->chunk_size == chunk_size)
        found_chunk->is_free = 1;
}