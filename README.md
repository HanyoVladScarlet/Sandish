# Sandish
Dataset production workflow oriented for object detection in adversial weather conditions.

## History

最初版本为 2024 年四月傻子节更新的版本，此版本修复了数据集鬼框的问题。

## 关于 Flask 服务器

Flask 服务器存在的首要目的是为了避免 Blender Commandline 输出过多无效信息而影响有效信息输出。其次，它还服务于以下功能：

1. 修改并保存 config 文件；
2. 集成 LabelImg，免得每次都要到另一个软件里查看效果；
3. 避免每次开始数据集生成都需要在控制台手敲命令；
4. 实现 OD 模型的图形操作界面；

Flask 将作为之后程序的入口，包括数据集生成和目标检测两个部分。

Flask 服务器将通过 Redis 实现与 Blender 进程的通讯。

以下是在 Docker 部署 Redis 容器的命令。

```dotnetcli
docker run --restart=always --log-opt max-size=100m --log-opt max-file=2 -p 6379:6379 --name myredis -v C:/Users/hanyo/Documents/GitHub/Sandish/redis/myredis/myredis.conf:/etc/redis/redis.conf -v C:/Users/hanyo/Documents/GitHub/Sandish/redis/myredis/data:/data -d redis redis-server /etc/redis/redis.conf  --appendonly yes  --requirepass 114514
```

服务器的消息推送采用了 `flask_sse`，这个组件同样依赖于 `Redis`，采用事件/触发器模式替代原来的前端服务器轮询模式，主动向前端发送事件更新消息。

> 采用事件订阅模式单纯是为了避免轮询带来的资源消耗。

在网页初始化时，会通过服务器的接口请求 `Redis` 当中的数据来获得服务器当前的状态信息。

### 程序结构

当前的 Workflow 为主要包括三大部分：

1. 模型、材质等要素的导入；
2. 参数的随机化；
3. 渲染出图、自动化标注；

## Configuration

### 模型导入

prefab_loader.py 将会从 `/blend_files/base/models.blend` 导入目标检测对象模型，并附加在 `base.blend` 文件中的 `targets` 集合中。

由于在生成 BBX 时，打标签的依据是物体实例的名称，为了标签的准确性，物体的命名规则为：`[标签名].[物体名].[其他]`。生成 BBX 的过程不关心 label 以外的任何其他信息，所以只要第一个 . 前的标签名正确即可。

## 随机化的实现方法

### 随机散布算法

首先将物体随机放置在棋盘格上，之后按照贴图的梯度场进行位移。

$$
\begin{aligned}
\rho &= e^{-0.008h + 0.9d}  \\
H_b &= e^{-0.008h} - 0.15\\
s_e &= 0.2e^{-0.72d} \\
H_e &= (0.02 \times d ^ {0.67} - \Delta H) \times 0.12
\end{aligned}
$$