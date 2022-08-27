---
layout: post
title:  "blockchain study"
date:   2020-05-6 22:29:41 +0800
categories: blockchain
tags: blockchain
---


## blockchains types:
1. Public blockchains: such as Bitcoin. open for anyone to participate at any leve, and have opens
2. Permissioned blockchains: such as Ripple. control roles that individuals can play within the network.
3. Private blockchains  



## 区块链技术应用场景：
1）资产： 数字资产发行、支付、交易、结算  
2）记账：股权  
3）点对点  
4）隐私：匿名交易  



## 区块链核心组成以及相关技术概念：
p2p网络协议，分布式一致性算法，加密签名算法，账户与存储模型


### p2p 网络
应用领域：流媒体，点对点通讯，文件共享到协同处理...  
p2p网络协议：bittorrent，ed2k，gnutella，tor  
p2p特点:  
1. 非传统C/S结构，去中心化：每个节点既是client，也是server。  
2. 文件分成多个资源块分散在各个节点中，每个节点既可以下载p2p网络中的资源块，也可以上传本地有的资源块。  

区块链基于TCP/IP协议，与http,smtp同一层  


比特币全节点组成的网络是一种全分布式的拓扑结构，节点与节点之间的传输过程更接近”泛洪算法“  

POW:   
计算难题解的过程     
缺点：耗能源，51%攻击   

POS：   
Hash (block_header) < Target * CoinAge    
不同矿工看到的target hash不同，币龄(持有币值不动时间)越长，难度越小    


### hash 函数  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
hash函数      
原始信息-------------> 摘要信息   



### 挖矿-工作量证明
1  一段时间内只有一个人可以记账成功  
2   Hash(上一个hash值，交易记录集) = asdf  
    Hash(上一个hash值，交易记录集，随机数) = asdfjkl  

3  共识机制  


### 非对称加密  
公钥+私钥  
               加密  
公钥+money ------------> 私钥解密

**交易流程**：私钥 保证 只有你能把属于你的钱支付出去  
比特币交易所开户： 生成比特币钱包，钱包用于存放公钥和私钥。 软件生成这两把钥匙，然后存放到钱包里  
公钥的长度512位，不方便传播---> 160位数指纹，26~35个字符   

### 交易流程
A 支付  B 10个比特币    
A需要提供数据：  
1） 上次交易的hash（where you get your coins）  
2） A 、 B 地址  
3）A的公钥  
4） 私钥生成的数字签名  


验证交易是否属实：   
1) 找到上一笔交易，确认支付方式的比特币来源     
2) 算出支付方式公钥的指纹， 确认支付方地址一致，保证公钥属实     
3) 使用公钥解开数字签名，保证私钥属实     
4) 比特币交易不能实时确认，必须至少等待一个小时     

## 数字钱包   
1.全节点钱包： 官方发行，包含完整的功能需求，挖矿，发送交易，查询交易记录，管理私钥      
2.spv轻钱包：全节点钱包简化版，挖矿、查询交易功能不包含      
3.中心化资产托管钱包：第三方服务商图托管数字货币，blockchain.info     

e.g. 以太坊系钱包imToken， 多币种钱包Jaxx，各个数字货币交易平台     





## 比特币
比特币是什么？  
数字货币 + 分布式记账系统  

### 比特币的优点：
1. 财产只受自己控制  
2. 无通胀  
3. 没有假钞  
4. 流通性好：点对点直接到账  

