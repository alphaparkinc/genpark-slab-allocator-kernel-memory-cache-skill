"""Slab Memory Allocator Engine.
100% Python Standard Library.
"""

class SlabAllocator:
    """Kernel-style Slab allocator managing fixed-size object caches."""
    class Slab:
        def __init__(self, obj_size, capacity=4):
            self.obj_size = obj_size
            self.capacity = capacity
            self.free_list = [f"obj_{i}@{id(self)}" for i in range(capacity)]
            self.allocated = set()

        def is_full(self):
            return len(self.free_list) == 0

        def is_empty(self):
            return len(self.allocated) == 0

    def __init__(self, obj_size=64, slab_capacity=4):
        self.obj_size = obj_size
        self.slab_capacity = slab_capacity
        self.slabs = []

    def allocate(self):
        for slab in self.slabs:
            if not slab.is_full():
                obj = slab.free_list.pop()
                slab.allocated.add(obj)
                return obj
        new_slab = self.Slab(self.obj_size, self.slab_capacity)
        obj = new_slab.free_list.pop()
        new_slab.allocated.add(obj)
        self.slabs.append(new_slab)
        return obj

    def free(self, obj):
        for slab in self.slabs:
            if obj in slab.allocated:
                slab.allocated.remove(obj)
                slab.free_list.append(obj)
                return True
        return False
