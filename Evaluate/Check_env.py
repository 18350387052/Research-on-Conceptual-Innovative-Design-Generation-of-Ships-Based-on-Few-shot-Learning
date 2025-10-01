import importlib
import sys
import platform

def check_deep_learning_env():
    print("Python 版本:", sys.version)
    print("操作系统:", platform.platform())
    print("CPU 信息:", platform.processor())
    print("-" * 40)

    # 检查常用深度学习库
    libs = ['torch', 'tensorflow', 'torchvision', 'numpy', 'scipy', 'sklearn']
    for lib in libs:
        try:
            mod = importlib.import_module(lib)
            version = getattr(mod, '__version__', '未知')
            print(f"{lib} 已安装，版本: {version}")
        except ImportError:
            print(f"{lib} 未安装")

    # 检查 CUDA 和 GPU
    try:
        import torch
        print("PyTorch CUDA 可用性:", torch.cuda.is_available())
        if torch.cuda.is_available():
            print("GPU 数量:", torch.cuda.device_count())
            print("当前 GPU:", torch.cuda.get_device_name(0))
    except ImportError:
        print("未检测到 PyTorch，无法检测 CUDA")

    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        print("TensorFlow 检测到的 GPU 数量:", len(gpus))
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"GPU {i}: {gpu}")
    except ImportError:
        print("未检测到 TensorFlow，无法检测 GPU")

    # 检查 CUDA 驱动
    try:
        import subprocess
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        print("CUDA 驱动信息:\n", result.stdout)
    except Exception:
        print("未检测到 nvcc 或 CUDA 驱动")

    print("-" * 40)
    print("环境检测完成。")

# 使用方法
if __name__ == "__main__":
    check_deep_learning_env()