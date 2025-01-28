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

```
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_all_gather(rank, world_size):
    # 初始化分布式环境
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

    # 创建一个随机张量作为起始值
    tensor = torch.tensor([rank + 1.0], device=torch.device('cpu'))  # 使用CPU以简化配置
    print(f"Rank {rank} before all_gather: {tensor}")

    # 准备接收结果的张量列表
    gather_list = [torch.zeros_like(tensor) for _ in range(world_size)]

    # 执行all_gather操作
    dist.all_gather(gather_list, tensor)

    # 输出all_gather后的结果
    print(f"Rank {rank} after all_gather: {gather_list}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    mp.spawn(run_all_gather,
             args=(world_size,),
             nprocs=world_size,
             join=True)

if __name__ == "__main__":
    main()
```

运行结果：

```
Rank 0 before all_gather: tensor([1.])
Rank 1 before all_gather: tensor([2.])
Rank 2 before all_gather: tensor([3.])
Rank 3 before all_gather: tensor([4.])
Rank 0 after all_gather: [tensor([1.]), tensor([2.]), tensor([3.]), tensor([4.])]
Rank 1 after all_gather: [tensor([1.]), tensor([2.]), tensor([3.]), tensor([4.])]
Rank 2 after all_gather: [tensor([1.]), tensor([2.]), tensor([3.]), tensor([4.])]
Rank 3 after all_gather: [tensor([1.]), tensor([2.]), tensor([3.]), tensor([4.])]
```



### 1.2 allreduce操作

**将所有进程的数据进行规约（例如sum操作），然后广播回到每个进程**

allreduce代码：

```
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_all_reduce(rank, world_size):
    # 初始化分布式环境
    dist.init_process_group("gloo", rank=rank, world_size=world_size) # 初始化分布式环境，gloo作为后端。如果有多个gpu可用可以改为nccl

    # 创建一个随机张量作为起始值
    tensor = torch.tensor([rank + 1.0], device=torch.device('cpu'))  # 使用CPU以简化配置
    print(f"Rank {rank} before all_reduce: {tensor}")

    # 执行all_reduce操作（求和）
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)

    # 输出all_reduce后的结果
    print(f"Rank {rank} after all_reduce: {tensor}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    mp.spawn(run_all_reduce,
             args=(world_size,),
             nprocs=world_size,
             join=True)

if __name__ == "__main__":
    main()
```

运行结果：

```
Rank 0 before all_reduce: tensor([1.])
Rank 1 before all_reduce: tensor([2.])
Rank 2 before all_reduce: tensor([3.])
Rank 3 before all_reduce: tensor([4.])
Rank 0 after all_reduce: tensor([10.])
Rank 1 after all_reduce: tensor([10.])
Rank 2 after all_reduce: tensor([10.])
Rank 3 after all_reduce: tensor([10.])
```

### 1.3 reduce操作

所有进程执行reduce操作，最终结果发送到根进程

```
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_reduce(rank, world_size):
    # 初始化分布式环境
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

    # 创建一个随机张量作为起始值
    tensor = torch.tensor([rank + 1.0], device=torch.device('cpu'))  # 使用CPU以简化配置
    print(f"Rank {rank} before reduce: {tensor}")

    # 指定根进程为0
    root_rank = 0

    # 执行reduce操作（求和）
    if rank == root_rank:
        print(f"Rank {rank} is the root.")
        dist.reduce(tensor, dst=root_rank, op=dist.ReduceOp.SUM)
        print(f"Rank {rank} after reduce: {tensor}")
    else:
        dist.reduce(tensor, dst=root_rank, op=dist.ReduceOp.SUM)
        print(f"Rank {rank} after reduce: (unchanged) {tensor}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    mp.spawn(run_reduce,
             args=(world_size,),
             nprocs=world_size,
             join=True)

if __name__ == "__main__":
    main()
```

运行结果：

```
Rank 0 before reduce: tensor([1.])
Rank 1 before reduce: tensor([2.])
Rank 2 before reduce: tensor([3.])
Rank 3 before reduce: tensor([4.])
Rank 0 is the root.
Rank 0 after reduce: tensor([10.])
Rank 1 after reduce: (unchanged) tensor([2.])
Rank 2 after reduce: (unchanged) tensor([3.])
Rank 3 after reduce: (unchanged) tensor([4.])
```

### 1.4 reducescatter 操作

每个进程拥有相同大小的张量数据，reducescatter会先对所有数据执行reduce 操作，然后每个进程接收一部分结果

![../_images/reducescatter.png](../images/../images/2025-1-27-collective_communications.assets/reducescatter.png)  

图片来源：https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html



```
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def run_reduce_scatter(rank, world_size):
    # 初始化分布式环境
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

    # 创建一个初始张量列表，每个进程都有相同大小的部分
    tensor_size = 2  # 每个进程创建的张量大小
    input_tensor = torch.ones(tensor_size * world_size) * (rank + 1)
    print(f"Rank {rank} before reduce_scatter: {input_tensor}")

    # 准备接收结果的张量
    output_tensor = torch.empty(tensor_size)

    # 执行reduce_scatter操作（求和）
    dist.reduce_scatter(output_tensor, [input_tensor], op=dist.ReduceOp.SUM)

    # 输出reduce_scatter后的结果
    print(f"Rank {rank} after reduce_scatter: {output_tensor}")

    # 清理资源
    dist.destroy_process_group()

def main():
    world_size = 4  # 模拟4个进程
    mp.spawn(run_reduce_scatter,
             args=(world_size,),
             nprocs=world_size,
             join=True)

if __name__ == "__main__":
    main()
    
```

运行结果：

````
Rank 0 before reduce_scatter: tensor([1., 1., 1., 1., 1., 1., 1., 1.])
Rank 1 before reduce_scatter: tensor([2., 2., 2., 2., 2., 2., 2., 2.])
Rank 2 before reduce_scatter: tensor([3., 3., 3., 3., 3., 3., 3., 3.])
Rank 3 before reduce_scatter: tensor([4., 4., 4., 4., 4., 4., 4., 4.])
Rank 0 after reduce_scatter: tensor([10., 10.])
Rank 1 after reduce_scatter: tensor([10., 10.])
Rank 2 after reduce_scatter: tensor([10., 10.])
Rank 3 after reduce_scatter: tensor([10., 10.])
````

