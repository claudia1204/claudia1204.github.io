---
layout: post
title:  "Operating System study"
date:   2023-10-27 22:00:41 +0800
categories: operating system study
tags: operating system study

---

《Computer Systems: A Programmer's Perspective》 reading records



### 1.7 operating systems 2 primary purposes

1）protect the hardware form misuse by applications

2）provide applications with simple and uniform mechanisms for manipulating hardware devices

### 1.7.1 Processes

![image-20231027150242608](../images/2023-10-27-operating_systems_study.assets/image-20231027150242608.png)  

### 1.7.2 Threads

process can be consist of multiple threads.

it's easier to share data between multiple threads than between multiple processes.

### 1.7.3 Virtual Memory

Each process has same uniform view of memory, which known as its virtual address space.  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027150751863.png" alt="image-20231027150751863" style="zoom: 50%;" /> 

Program code and data： code start from same fixed address for all processes.

Heap: not fixed size. dynamically at run time as a result of calls to c lib such as  malloc and free.

### 1.7.4 Files

All I/O devices are modeled as files.

### 1.9 Concurrency and parrallelism





### 2.3 Two's-complement Encodings

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027101213270.png" alt="image-20231027101213270" style="zoom: 50%;" />  



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027111140688.png" alt="image-20231027111140688" style="zoom:50%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027111637345.png" alt="image-20231027111637345" style="zoom:50%;" />    



mystore.c

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027153418370.png" alt="image-20231027153418370" style="zoom:50%;" />  



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027153653877.png" alt="image-20231027153653877" style="zoom:50%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027153733554.png" alt="image-20231027153733554" style="zoom: 50%;" />   



.o file and binary file:

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027154004951.png" alt="image-20231027154004951" style="zoom:67%;" /> 

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027154019564.png" alt="image-20231027154019564" style="zoom:67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027153151171.png" alt="image-20231027153151171" style="zoom: 67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027153849027.png" alt="image-20231027153849027" style="zoom: 67%;" />  

 <img src="../images/2023-10-27-operating_systems_study.assets/image-20231027104441738.png" alt="image-20231027104441738" style="zoom:67%;" /> 

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027104533733.png" alt="image-20231027104533733" style="zoom:67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027104602555.png" alt="image-20231027104602555" style="zoom:67%;" />  

![image-20231027140935835](../images/2023-10-27-operating_systems_study.assets/image-20231027140935835.png)

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027141609636.png" alt="image-20231027141609636" style="zoom:67%;" /> 

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027142005775.png" alt="image-20231027142005775" style="zoom:67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027150751437.png" alt="image-20231027150751437" style="zoom:67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027161318575.png" alt="image-20231027161318575" style="zoom:67%;" /> 



## 7 Linking

### 7.1 Compiler Drivers



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027145731936.png" alt="image-20231027145731936" style="zoom:67%;" />   

```shell
linux> gcc -Og -o prog main.c sum.c
```

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027145701129.png" alt="image-20231027145701129" style="zoom:80%;" />  

compile steps:

```shell
cpp [other arguments] main.c /tmp/main.i  # replace include with file content
cc1 /tmp/main.i -Og [other arguments] -o /tmp/main.s #translate it into an ASCII assembly-language file
as [other arguments] -o /tmp/main.o /tmp/main.s #assembler translate main.s to main.o
ld -o prog [system object files and args] /tmp/main.o /tmp/sum.o #combine main.o and sum.o, along with system the necessary system object files, to create bin exe object file
linux> ./prog
```



### 7.2 static linking

take as input a collection of relocatable object files and command-line arguments and generate as a output a fully linked executable object file that can be loaded and run.

linker build executable with 2 steps:

1. **Symbol resolution**: associate each symbol reference with exactly one symbol definition
2. **Relocation**: linker relocates sections(code, data) by associating memory location with each symbol definition, and then modifying all of the references to those symbols so that they point to this memory location.

### 7.3 Relocatable Object files

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027152416834.png" alt="image-20231027152416834" style="zoom:80%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027152532805.png" alt="image-20231027152532805" style="zoom:67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027152553562.png" alt="image-20231027152553562" style="zoom:67%;" />  

### 7.5 Symbols and symbol tables









## 9 Virtual memory

### 9.1 Physical and Virtual Address

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027164047574.png" alt="image-20231027164047574" style="zoom:67%;" />  



Virtual address--> dedicated hardware on CPU chip called MMU(memory management unit)--->Physical address



### 9.3 VM as a Tool for Caching

#### 9.3.4 Page Faults

swapping/paging: transfer a page between disk and Dram

swapped in: pages are swapped in from disk to DRAM

swapping out: pases are swapped out from DRAM to disk

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027094014806.png" alt="image-20231027094014806" style="zoom:67%;" />  



#### 9.3.5 Allocating pages

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027094710388.png" alt="image-20231027094710388" style="zoom:67%;" />  

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027094802509.png" alt="image-20231027094802509" style="zoom:67%;" />  



#### 9.3.6 Address Translating

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027095817348.png" alt="image-20231027095817348" style="zoom:67%;" />  



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027100551934.png" alt="image-20231027100551934" style="zoom:67%;" /> 



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027100745368.png" alt="image-20231027100745368" style="zoom:67%;" />  



### 9.5 VM as a Tool for Memory Protection

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027101047108.png" alt="image-20231027101047108" style="zoom:67%;" />  





### 9.8 Memory mapping

Virtual memory areas can be mapped to one of **two types of objects:**

- Regular file in the Linux file system

such as executable object file. The file section is divided into page-size pieces, with each piece containing the initial contents of a virtual page.

- Anonymous file

created by kernel, that contains all binary zeros.

the first time the CPU touches a virtual page in such an area, the kernel finds an appropriate victim page in physical memory, swaps out the victim page if it is dirty, overwrites the page with binary zeros, and update page table to mark the page as resident.



**swap space**(maintained by the kernel) bounds the total amount of virtual pages that can be allocated by the currently running processes.



#### 9.8.1 shared objects revisited

An object can be mapped into an area of virtual memory as either a **shared object** or a **private object**.

**shared object**: any process make change to the object, other process will see the change.

**private object**: any process make change to the object, other process can not see the change.

 



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027110555019.png" alt="image-20231027110555019" style="zoom:67%;" /> 

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027110615193.png" alt="image-20231027110615193" style="zoom:67%;" /> 



copy-on-write: different process share a same object with read only permission. When one process want to write on this object, then copy a new one and write to new object.

#### 9.8.2 The fork Function revisited

current process-->fork: create copies of current porcess's **mm_struct, area structs, and page tables.**

#### 9.8.3 The execve Function revisited

```
execve("a.out", NULL, NULL);
```



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027112606841.png" alt="image-20231027112606841" style="zoom:67%;" /> 

1. delete existing user areas

2. map private areas

3. map shared areas

4. set the program counter(PC)

   

#### 9.8.4 User-level memory mapping with the mmap function

Linux process can use mmap to map an object into a new area of virtual memory

 <img src="../images/2023-10-27-operating_systems_study.assets/image-20231027142418698.png" alt="image-20231027142418698" style="zoom:67%;" />  

start: start address is merely a hint. and is usually specified as NULL.

port: permission of mapped virtual memory area.

- PROT_EXEC: pages in the area consist of instructions that may be executed by the CPU
- PROT_READ: Pages in the area may be read.
- PROT_WRITE: Pages in the area may be written.
- PROT_NONE: Pages in the area cannnot be accessed.

flags: the type of mapped object.

- MAP_ANON: anonymous object, virtual pages are demand-zero.
- MAP_PRIVATE: private copy-on-write object
- MAP_SHARED: shared object

```
bufp = Mmap(NULL, size, PROT_READ, MAP_PRIVATE|MAP_ANON, 0, 0);
```

delete the area: munmap delete the area starting at virtual address start with length bytes.

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027143430622.png" alt="image-20231027143430622" style="zoom:67%;" /> 





### 9.9 Dynamic memroy allocation

A dynamic memory allocator maintains an area of process's virtual memory known as heap.

**heap:** an area of demand-zero memory that begins immediately after the uninitialized data and grows upward(toward higher addresses.) 

for each process, the kernel maintains a variable **brk** that points to the top of the heap.

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027150521036.png" alt="image-20231027150521036" style="zoom:67%;" />  



Allocators come in two basic styles:

Explicit allocators:  malloc and free. new and delete(c++)

Implicit allocators:  garbage collectors.

#### 9.9.1 The malloc and free Functions

<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027151222990.png" alt="image-20231027151222990" style="zoom:67%;" />  

**malloc:** return **at least size bytes** that is suitably aligned for any kind of data object that might be contained in the block.

**malloc:** does not initialize the memory it returns.

**calloc**: a thin wrapper around the malloc function that **initializes the allocated memory to zero**.

**realloc:** change size of previously allocated block

**sbrk:** grows or shrinks the heap by adding incr to the kernel's brk pointer.



<img src="../images/2023-10-27-operating_systems_study.assets/image-20231027151921552.png" alt="image-20231027151921552" style="zoom: 67%;" /> 

#### 9.9.2 why dynamic memory allocation?



#### 9.9.4 Fragmentation











### 9.12 Summary 

Virtual memory, 3 important capabilities:

1) **caches** recently used contents of the virtual address space stored on disk in main memory

   **page fault:**  a reference to a page on disk triggers a page fault that transfers control to a fault handler in the operating system.

2. **simplifies memory management**, which in turn simplifies linking, sharing data between processes, the allocation of memory for processes, and program loading.

3.  **simplifies memory protection** by incorporating protection bits into every page table entry.

   

**mmap**: create and delete areas of virtual memory.

**malloc**: manages memory in an area of the virutal address space called the **heap**

dynamic memory allocators are application-level programs with a system-level feel, directly manipulating memory without much help from the type system.

**Allocators** come in two flavors: **Explicit allocators/ Implicit allocators**

