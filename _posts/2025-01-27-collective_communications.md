---
layout: post
title:  "集合通信操作学习"
date:   2025-01-27 14:29:41 +0800
categories: collective-communications
tags: collective
---


集合通信，指的是分布式进程中，多个进程同时进行某一项操作（也叫规约）时的动作。这个规约操作可以是执行加法、减法、乘法...

比如多机多gpu，执行数据的规约操作。

其中每个进程有一个唯一id，rank，以0为起始。例如2个进程，则分为rank为0和1

## 1. 规约操作分类

规约操作根据规约的形式分为几类：

1. allgather,
2. allreduce
3. reduce
4. reducescatter
5. sendrecv 

### 1.1 allgather 

收集所有进程的数据，每个进程都存储一份gather后的结果

![../_images/allgather.png](../images/../images/2025-1-27-collective_communications.assets/allgather.png)  

图片来源：https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html

```c
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_all_gather(rank, world_size):
    # 初始化分布式环境，使用NCCL后端
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

    # 设置当前进程使用的GPU
    device = torch.device(f'cuda:{rank}')
    
    tensor_size = 2  # 每个进程创建的张量大小
    dtype = torch.float32  # 确保所有张量使用相同的数据类型
    
    # 创建每个进程对应的那一部分数据，并确保数据类型一致
    input_tensor = (torch.ones(tensor_size, dtype=dtype) * (rank + 1)).to(device)
    print(f"Rank {rank} before all_gather: {input_tensor}")

    # 收集所有ranks的张量
    gather_list = [torch.empty_like(input_tensor) for _ in range(world_size)]
    dist.all_gather(gather_list, input_tensor)

    # 输出all_gather后的结果
    print(f"Rank {rank} after all_gather: {gather_list}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 示例中使用4个进程，但可以根据需要调整
    if torch.cuda.device_count() < world_size:
        print(f"This example requires at least {world_size} GPUs.")
    else:
        mp.spawn(run_all_gather,
                 args=(world_size,),
                 nprocs=world_size,
                 join=True)

if __name__ == "__main__":
    main()
```

运行结果：

```
Rank 1 before all_gather: tensor([2., 2.], device='cuda:1')
Rank 0 before all_gather: tensor([1., 1.], device='cuda:0')
Rank 3 before all_gather: tensor([4., 4.], device='cuda:3')
Rank 2 before all_gather: tensor([3., 3.], device='cuda:2')
Rank 0 after all_gather: [tensor([1., 1.], device='cuda:0'), tensor([2., 2.], device='cuda:0'), tensor([3., 3.], device='cuda:0'), tensor([4., 4.], device='cuda:0')]
Rank 2 after all_gather: [tensor([1., 1.], device='cuda:2'), tensor([2., 2.], device='cuda:2'), tensor([3., 3.], device='cuda:2'), tensor([4., 4.], device='cuda:2')]
Rank 1 after all_gather: [tensor([1., 1.], device='cuda:1'), tensor([2., 2.], device='cuda:1'), tensor([3., 3.], device='cuda:1'), tensor([4., 4.], device='cuda:1')]
Rank 3 after all_gather: [tensor([1., 1.], device='cuda:3'), tensor([2., 2.], device='cuda:3'), tensor([3., 3.], device='cuda:3'), tensor([4., 4.], device='cuda:3')]
```



### 1.2 allreduce操作

**将所有进程的数据进行规约（例如sum操作），然后广播回到每个进程**

allreduce代码：

```c
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_all_reduce(rank, world_size):
    # 初始化分布式环境，使用NCCL后端
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

    # 设置当前进程使用的GPU
    device = torch.device(f'cuda:{rank}')
    
    tensor_size = 8  # 每个进程创建的张量大小
    dtype = torch.float32  # 确保所有张量使用相同的数据类型
    
    # 创建每个进程对应的那一部分数据，并确保数据类型一致
    input_tensor = (torch.ones(tensor_size, dtype=dtype) * (rank + 1)).to(device)
    print(f"Rank {rank} before all_reduce: {input_tensor}")

    # 执行all_reduce操作（求和）
    dist.all_reduce(input_tensor, op=dist.ReduceOp.SUM)

    # 输出all_reduce后的结果
    print(f"Rank {rank} after all_reduce: {input_tensor}") 

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    if torch.cuda.device_count() < world_size:
        print(f"This example requires at least {world_size} GPUs.")
    else:
        mp.spawn(run_all_reduce,
                 args=(world_size,),
                 nprocs=world_size,
                 join=True)

if __name__ == "__main__":
    main()
```

运行结果：

```shell
Rank 3 before all_reduce: tensor([4., 4., 4., 4., 4., 4., 4., 4.], device='cuda:3')
Rank 1 before all_reduce: tensor([2., 2., 2., 2., 2., 2., 2., 2.], device='cuda:1')
Rank 0 before all_reduce: tensor([1., 1., 1., 1., 1., 1., 1., 1.], device='cuda:0')
Rank 2 before all_reduce: tensor([3., 3., 3., 3., 3., 3., 3., 3.], device='cuda:2')
Rank 0 after all_reduce: tensor([10., 10., 10., 10., 10., 10., 10., 10.], device='cuda:0')
Rank 1 after all_reduce: tensor([10., 10., 10., 10., 10., 10., 10., 10.], device='cuda:1')
Rank 3 after all_reduce: tensor([10., 10., 10., 10., 10., 10., 10., 10.], device='cuda:3')
Rank 2 after all_reduce: tensor([10., 10., 10., 10., 10., 10., 10., 10.], device='cuda:2')
```

### 1.3 reduce操作

所有进程执行reduce操作，最终结果发送到根进程

```c
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_reduce(rank, world_size):
    # 初始化分布式环境，使用NCCL后端
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

    # 设置当前进程使用的GPU
    device = torch.device(f'cuda:{rank}')
    
    tensor_size = 8  # 每个进程创建的张量大小
    dtype = torch.float32  # 确保所有张量使用相同的数据类型
    
    # 创建每个进程对应的那一部分数据，并确保数据类型一致
    input_tensor = (torch.ones(tensor_size, dtype=dtype) * (rank + 1)).to(device)
    print(f"Rank {rank} before reduce: {input_tensor}")

    # 执行reduce操作（求和），并将结果放在根rank上
    dist.reduce(input_tensor, dst=0, op=dist.ReduceOp.SUM)

    if rank == 0:
        # 根rank上的输出张量现在包含了所有ranks的归约结果
        print(f"Root Rank {rank} after reduce: {input_tensor}")
    else:
        print(f"Rank {rank} remains unchanged after reduce: {input_tensor}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    if torch.cuda.device_count() < world_size:
        print(f"This example requires at least {world_size} GPUs.")
    else:
        mp.spawn(run_reduce,
                 args=(world_size,),
                 nprocs=world_size,
                 join=True)

if __name__ == "__main__":
    main()
```

运行结果：

```c
Rank 1 before reduce: tensor([2., 2., 2., 2., 2., 2., 2., 2.], device='cuda:1')
Rank 0 before reduce: tensor([1., 1., 1., 1., 1., 1., 1., 1.], device='cuda:0')
Rank 2 before reduce: tensor([3., 3., 3., 3., 3., 3., 3., 3.], device='cuda:2')
Rank 3 before reduce: tensor([4., 4., 4., 4., 4., 4., 4., 4.], device='cuda:3')
Rank 1 remains unchanged after reduce: tensor([2., 2., 2., 2., 2., 2., 2., 2.], device='cuda:1')
Rank 2 remains unchanged after reduce: tensor([3., 3., 3., 3., 3., 3., 3., 3.], device='cuda:2')
Root Rank 0 after reduce: tensor([10., 10., 10., 10., 10., 10., 10., 10.], device='cuda:0')
Rank 3 remains unchanged after reduce: tensor([4., 4., 4., 4., 4., 4., 4., 4.], device='cuda:3')
```

### 1.4 reducescatter 操作

每个进程拥有相同大小的张量数据，reducescatter会先对所有数据执行reduce 操作，然后每个进程接收一部分结果

![../_images/reducescatter.png](../images/../images/2025-1-27-collective_communications.assets/reducescatter.png)  

图片来源：https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html



```c
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_reduce_scatter(rank, world_size):
    # 初始化分布式环境，使用NCCL后端
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

    # 设置当前进程使用的GPU
    device = torch.device(f'cuda:{rank}')
    
    tensor_size = 8  # 每个进程创建的张量大小
    dtype = torch.float32  # 确保所有张量使用相同的数据类型
    
    # 创建每个进程对应的那一部分数据，并确保数据类型一致
    input_tensor = (torch.ones(tensor_size, dtype=dtype) * (rank + 1)).to(device)
    print(f"Rank {rank} before reduce_scatter: {input_tensor}")

    # 准备接收结果的张量，并确保其数据类型与输入张量一致
    output_tensor = torch.empty(tensor_size // world_size, dtype=dtype).to(device)

    # 执行reduce_scatter操作（求和）
    dist.reduce_scatter(output_tensor, [input_tensor], op=dist.ReduceOp.SUM)

    # 输出reduce_scatter后的结果
    print(f"Rank {rank} after reduce_scatter: {output_tensor}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    if torch.cuda.device_count() < world_size:
        print(f"This example requires at least {world_size} GPUs.")
    else:
        mp.spawn(run_reduce_scatter,
                 args=(world_size,),
                 nprocs=world_size,
                 join=True)

if __name__ == "__main__":
    main()
    
```

运行结果：

````shell
Rank 1 before reduce_scatter: tensor([2., 2., 2., 2., 2., 2., 2., 2.], device='cuda:1')
Rank 2 before reduce_scatter: tensor([3., 3., 3., 3., 3., 3., 3., 3.], device='cuda:2')
Rank 3 before reduce_scatter: tensor([4., 4., 4., 4., 4., 4., 4., 4.], device='cuda:3')
Rank 0 before reduce_scatter: tensor([1., 1., 1., 1., 1., 1., 1., 1.], device='cuda:0')
Rank 1 after reduce_scatter: tensor([10., 10.], device='cuda:1')
Rank 3 after reduce_scatter: tensor([10., 10.], device='cuda:3')
Rank 2 after reduce_scatter: tensor([10., 10.], device='cuda:2')
Rank 0 after reduce_scatter: tensor([10., 10.], device='cuda:0')
````

