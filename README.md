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


### 程序结构

当前的 Workflow 为主要包括三大部分：

1. 模型、材质等要素的导入；
2. 参数的随机化；
3. 渲染出图、自动化标注；



## Configuration

### 模型导入

prefab_loader.py 将会从 `/blend_files/base/models.blend` 导入目标检测对象模型，并附加在 `base.blend` 文件中的 `targets` 集合中。

由于在生成 BBX 时，打标签的依据是物体实例的名称，为了标签的准确性，物体的命名规则为：`[标签名].[物体名].[其他]`。生成 BBX 的过程不关心 label 以外的任何其他信息，所以只要第一个 . 前的标签名正确即可。

