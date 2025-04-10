[Python versions]: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue

 1. 将 requirements.txt 文件中需要的模块先下载到本地，建议单独创建一个虚拟环境。

   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

2. 运行 detect_rec_plate.py 脚本即可执行车牌检测+车牌识别程序，检测图片或视频放在【T_T_imgs】文件夹，
    结果将会输出到【T_T_result】文件夹。

3. 运行 GUI.py 可以使用图形化界面进行车牌识别。