from client import SlabAllocator

alloc = SlabAllocator(obj_size=128, slab_capacity=3)
objs = [alloc.allocate() for _ in range(5)]
print(f"Allocated 5 objects across {len(alloc.slabs)} slabs: {objs}")

freed = alloc.free(objs[0])
print(f"Freed first object: {freed}")
