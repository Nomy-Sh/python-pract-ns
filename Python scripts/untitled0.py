import pyopencl as cl
import numpy as np

a = np.random.rand(50000).astype(np.float32)
b = np.random.rand(50000).astype(np.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a.nbytes)

prg = cl.Program(ctx, """
__kernel void sum(__global const float *a, __global const float *b, __global float *res)
{
    int gid = get_global_id(0);
    res[gid] = a[gid] + b[gid];
}
""").build()

prg.sum(queue, a.shape, None, a_g, b_g, res_g)

res = np.empty_like(a)
cl.enqueue_copy(queue, res, res_g)

print(res[:10])
