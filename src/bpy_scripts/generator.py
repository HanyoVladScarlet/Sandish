import os
import bpy
import time
import math
import config as config
import bpy_extras
from mathutils import Vector


import bpy_scripts.prefab_loader as pfl


# TODO: 添加到配置文件当中
OUTPUT_PATH_BASE = 'outputs/dataset_'


class SampleGenerator():
    '''
    使用此类型来完成数据集的输出.
    使用单例模式.
    '''
    _instance = None
    def __init__(self) -> None:
        ''''''
        self.initialize()


    def output_one(self):
        ''''''
        time_str = time.strftime("%Y-%m-%d_%H-%M-%S")
        # 输出图像
        name = f'{self.output_path_base}/dataset/sample_{time_str}.png'
        self.render_one(name)
        name = f'{self.output_path_base}/dataset/sample_{time_str}.txt'
        self.label_one(name)


    def initialize(self):
        '''
        检查输出文件夹是否存在, 对应文件夹结构:
        + description.txt
        + amydata.yml
        + dataset/
            + classes.txt
            + sample_1.png
            + sample_1.txt
            + ...
        + train_res/
            + exp_1
            + exp_2
            + ...
        + val_res/
            + exp_1
            + ...
        '''
        # 本轮实验输出的根目录
        self.output_path_base = os.path.abspath(f'{OUTPUT_PATH_BASE}{time.strftime("%Y-%m-%d_%H-%M-%S")}/')
        if not os.path.exists(self.output_path_base):
            os.makedirs(self.output_path_base)
        # 本轮实验输出的完整数据集
        path = f'{self.output_path_base}/dataset/'
        if not os.path.exists(path):
            os.makedirs(path)
        # 本轮实验的训练结果
        path = f'{self.output_path_base}/train_res/'
        if not os.path.exists(path):
            os.makedirs(path)
        # 本轮实验的预测结果
        path = f'{self.output_path_base}/val_res/'
        if not os.path.exists(path):
            os.makedirs(path)
        # 本轮实验的标签列表，主要用于 labelimg 预览
        path = f'{self.output_path_base}/dataset/classes.txt'
        with open(path, 'w') as f:
            f.write('\n'.join(pfl.LABELS))
        # amydata.yml, 用于yolo训练
        # TODO: 修正文件内容
        path = f'{self.output_path_base}/amydata.yml'
        with open(path, 'w') as f:
            f.write('\n'.join(pfl.LABELS))
        # 本轮实验的参数列表, 比如烟雾浓度, 实例数量等等.
        # TODO: 修正文件内容
        path = f'{self.output_path_base}/description.txt'
        with open(path, 'w') as f:
            f.write('\n'.join(pfl.LABELS))


    @staticmethod 
    def get_sample_generator(initialize=False):
        '''
        使用单例模式.
        '''
        if SampleGenerator._instance is None:
            SampleGenerator._instance = SampleGenerator()
        if initialize:
            SampleGenerator._instance.initialize()
        return SampleGenerator._instance


    def render_one(self, name):
        renderer = bpy.context.scene.render
        renderer.filepath = name
        renderer.resolution_x = config.get_output_width()
        renderer.resolution_y = config.get_output_height()
        renderer.image_settings.file_format = config.get_output_format()
        bpy.context.scene.cycles.samples = config.get_max_sample()
        renderer.engine = config.get_render_engine()
        bpy.ops.render.render(write_still = True)
        
        return


    # TODO: 使用蒙特卡洛方法重构遮挡判定算法
    def label_one(self, name):
        '''
        这里的one指的是一张图片，包含了若干框
        '''
        alternates = []
        labels = pfl.get_labels()
        for col in pfl.get_instance_col().children:
            for o_name in col.objects.keys():
                # cx, cy, w, h, dep
                yolo_res = self.get_bounding_box(o_name)
                if yolo_res is None:
                    continue
                for i in range(len(labels)):
                    if o_name.startswith(labels[i]):
                        alternates.append(yolo_res + (i,))

        items = []
        ban_hash = set()
        max_overlap = float(config.CONFIG['label']['max_overlap'])

        for i in range(len(alternates)):
            cxi = alternates[i][0]
            cyi = alternates[i][1]
            wi = alternates[i][3]
            hi = alternates[i][2]
            di = alternates[i][4]

            # if i in ban_hash:
            #     continue

            # if di < 0:
            #     ban_hash.add(i)
            #     continue

            for j in range(i + 1, len(alternates)):
                cxj = alternates[j][0]
                cyj = alternates[j][1]
                wj = alternates[j][3]
                hj = alternates[j][2]
                dj = alternates[j][4]

                # 利用对称性归一化
                cxj = cxj if cxi < cxj else cxi * 2 - cxj
                cyj = cyj if cyi < cyj else cyi * 2 - cyj
                delta_ax = cxi - cxj + (wj + wi) / 2
                delta_ay = cyi - cyj + (hj + hi) / 2

                # 判断为不相关
                if delta_ax <= 0 or delta_ay <= 0:
                    continue
                
                overlap = min(delta_ax, wj, wi) * min(delta_ay, hj, hi)

                # 判断前后关系，物体一在前
                if di <= dj:
                    base_area = wj * hj
                    if max_overlap < overlap / base_area:
                        ban_hash.add(j)
                # 判断前后关系，物体二在前
                else:
                    base_area = wi * hi
                    if max_overlap < overlap / base_area:
                        ban_hash.add(i)

            # 当物体出现在图片边缘时
            if wi / hi < .3 or wi / hi > 3:
                ban_hash.add(i)

        # 逐条添加标签
        for idx in range(len(alternates)):
            if idx in ban_hash:
                continue
            item = ' '.join((str(alternates[idx][5]), str(alternates[idx][0]), str(alternates[idx][1]), str(alternates[idx][2]), str(alternates[idx][3]),))
            items.append(item)

        text = '\n'.join(items)
        with open(name, 'w') as f:
            f.write(text)
        return items

    # 数据集请将label和image放在同一目录下，并且创建classes.txt文件
    # 这里出现鬼框的原因是如下：
    # 1. 物体在摄像机之后也会被计入屏幕空间，因为投影是不分方向的
    # 2. 物体的中心点在摄像机面前，但是物体距离摄像机过近导致物体投影将屏幕空间完全包围，并且无法渲染到屏幕
    def get_bounding_box(self, obj_name, cam_name = 'Camera'):
        '''
        @return: []
        '''
        scene = bpy.context.scene
        obj = bpy.data.objects[obj_name]
        cam = bpy.data.objects[cam_name]

        d_pos = obj.location - cam.location
        cam_forward = cam.matrix_world.to_quaternion() @ Vector((0,0,-1))

        # 用于抑制第一种鬼框，将所有摄像机后半个空间上的物体排除掉
        if Vector.angle(d_pos, cam_forward) > math.pi / 2:
            return

        depth = d_pos.magnitude
        vertices = obj.data.vertices
        max_overlap = float(config.CONFIG['label']['max_overlap'])

        max_h = float('-inf')
        max_v = float('-inf')
        min_h = float('inf')
        min_v = float('inf')

        for v in vertices:
            # 这里的@是做内积，矩阵乘以向量，将局部坐标转换为世界坐标
            co_final = obj.matrix_world @ v.co
            co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, co_final)

            # 这里加入clip检测
            # 如果物体只有一部分在图像内则不画框
            max_h = max(co_2d.x, max_h)
            max_v = max(co_2d.y, max_v)
            min_h = min(co_2d.x, min_h)
            min_v = min(co_2d.y, min_v)

        base_area = (max_h - min_h) * (max_v - min_v)

        max_h = min(max_h, 1)
        max_v = min(max_v, 1)
        min_h = max(min_h, 0)
        min_v = max(min_v, 0)

        height = max_v - min_v
        width = max_h - min_h
        actual_area = height * width

        if actual_area <= 0 or base_area / actual_area < max_overlap:
            return

        if width < 0 or height < 0:
            return
        # if max_h == min_h or max_v == min_v:
        #     return

        # 用非精确的方式抑制第二种鬼框
        if height > .998 and width > .998:
            return

        # Yolo's y-coordinate begins at upper bound
        # Use one minus node
        center_y = 1 - (max_v + min_v) / 2  
        center_x = (max_h + min_h) / 2

        return center_x, center_y, width, height, depth
