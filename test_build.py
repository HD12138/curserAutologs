import unittest
import os
import platform
import shutil
from unittest.mock import patch, MagicMock
from build import LoadingAnimation, build, filter_output

class TestBuild(unittest.TestCase):
    def setUp(self):
        # 测试前的设置
        self.test_output_dir = f"dist/{platform.system().lower()}"
        self.test_config = "config.ini.example"
        self.test_env = ".env.example"

    def tearDown(self):
        # 测试后清理
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        
    def test_filter_output(self):
        # 测试输出过滤功能
        test_output = """
        普通信息
        Error: 这是一个错误
        一般日志
        Failed: 这是一个失败
        Directory: /path/to/dir
        Completed: 任务完成
        """
        filtered = filter_output(test_output)
        self.assertIn("Error:", filtered)
        self.assertIn("Failed:", filtered)
        self.assertIn("Directory:", filtered)
        self.assertNotIn("普通信息", filtered)
        self.assertNotIn("一般日志", filtered)

    def test_loading_animation(self):
        # 测试加载动画
        loading = LoadingAnimation()
        loading.start("测试中")
        loading.stop()
        self.assertFalse(loading.is_running)

    @patch('subprocess.run')
    def test_build_success(self, mock_run):
        # 模拟成功的构建过程
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        # 创建测试用的配置文件
        with open(self.test_config, 'w') as f:
            f.write("test config")
        with open(self.test_env, 'w') as f:
            f.write("test env")

        try:
            build()
            
            # 验证输出目录是否创建
            self.assertTrue(os.path.exists(self.test_output_dir))
            
            # 验证 PyInstaller 是否被正确调用
            mock_run.assert_called()
            
        finally:
            # 清理测试文件
            if os.path.exists(self.test_config):
                os.remove(self.test_config)
            if os.path.exists(self.test_env):
                os.remove(self.test_env)

    @patch('subprocess.run')
    def test_build_failure(self, mock_run):
        # 模拟构建失败的情况
        mock_run.side_effect = FileNotFoundError()
        
        with self.assertRaises(SystemExit):
            build()

    def test_output_directory_creation(self):
        # 测试输出目录创建
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
            
        with patch('subprocess.run'):
            build()
            
        self.assertTrue(os.path.exists(self.test_output_dir))

if __name__ == '__main__':
    unittest.main() 