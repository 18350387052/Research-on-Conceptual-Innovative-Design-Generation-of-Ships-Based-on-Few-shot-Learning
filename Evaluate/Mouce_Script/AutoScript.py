import pyautogui
import time
import random
import threading
import sys
from datetime import datetime


class AutoMouseClicker:
    def __init__(self):
        self.running = False
        self.click_x = 500  # 默认点击位置X坐标
        self.click_y = 300  # 默认点击位置Y坐标
        self.base_interval = 190  # 基础间隔时间(秒)
        self.click_count = 0
        self.target_clicks = 0  # 目标点击次数

        # 禁用pyautogui的安全功能(可选)
        pyautogui.FAILSAFE = True  # 鼠标移到屏幕左上角可以停止程序
        pyautogui.PAUSE = 0.1  # 每次操作后的暂停时间

    def set_target_clicks(self, count):
        """设置目标点击次数"""
        self.target_clicks = count
        print(f"目标点击次数已设置为: {count} 次")

    def set_click_position(self, x, y):
        """设置点击位置"""
        self.click_x = x
        self.click_y = y
        print(f"点击位置已设置为: ({x}, {y})")

    def get_current_mouse_position(self):
        """获取当前鼠标位置"""
        pos = pyautogui.position()
        print(f"当前鼠标位置: ({pos.x}, {pos.y})")
        return pos.x, pos.y

    def simulate_human_click(self):
        """模拟人类点击行为"""
        try:
            # 在目标位置周围添加小幅随机偏移(±3像素)
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)

            actual_x = self.click_x + offset_x
            actual_y = self.click_y + offset_y

            # 移动到目标位置(添加缓动效果)
            pyautogui.moveTo(actual_x, actual_y, duration=random.uniform(0.1, 0.3))

            # 随机延迟一小段时间
            time.sleep(random.uniform(0.05, 0.15))

            # 执行点击
            pyautogui.click()

            self.click_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] 第 {self.click_count} 次点击完成，位置: ({actual_x}, {actual_y})")
            print(f"进度: {self.click_count}/{self.target_clicks}")

            # 检查是否完成目标次数
            if self.click_count >= self.target_clicks:
                print(f"\n🎉 已完成目标点击次数 {self.target_clicks} 次！")
                self.running = False
                return True  # 返回True表示正常完成

        except Exception as e:
            print(f"点击时发生错误: {e}")
            return False

    def calculate_next_interval(self):
        """计算下次点击的间隔时间，添加随机变化模拟人类行为"""
        # 在基础间隔时间上添加±10秒的随机变化
        variation = random.uniform(-10, 10)
        next_interval = self.base_interval + variation

        # 确保间隔时间不少于240秒
        next_interval = max(self.base_interval-10, next_interval)

        return next_interval

    def start_clicking(self):
        """开始自动点击"""
        if self.running:
            print("程序已在运行中...")
            return

        if self.target_clicks <= 0:
            print("请先设置目标点击次数！")
            return

        self.running = True
        self.click_count = 0

        print("=== 自动鼠标点击程序启动 ===")
        print(f"点击位置: ({self.click_x}, {self.click_y})")
        print(f"目标点击次数: {self.target_clicks} 次")
        print(f"基础间隔: {self.base_interval} 秒 (±10秒随机变化)")
        print("按 Ctrl+C 可以停止程序")
        print("鼠标移动到屏幕左上角也可以紧急停止")
        print("-" * 40)

        try:
            while self.running and self.click_count < self.target_clicks:
                # 执行点击
                click_result = self.simulate_human_click()

                # 如果已完成目标次数，退出循环
                if click_result or self.click_count >= self.target_clicks:
                    break

                # 计算下次点击间隔
                next_interval = self.calculate_next_interval()

                remaining_clicks = self.target_clicks - self.click_count
                print(f"剩余 {remaining_clicks} 次点击，下次点击将在 {next_interval:.1f} 秒后执行...")
                print("-" * 40)

                # 分段等待，以便可以响应停止信号
                wait_time = 0
                while wait_time < next_interval and self.running and self.click_count < self.target_clicks:
                    time.sleep(1)
                    wait_time += 1

        except pyautogui.FailSafeException:
            print("\n检测到鼠标移动到屏幕角落，程序已停止")
        except KeyboardInterrupt:
            print("\n接收到停止信号，程序已停止")
        except Exception as e:
            print(f"\n程序运行时发生错误: {e}")
        finally:
            self.running = False
            if self.click_count >= self.target_clicks:
                print(f"\n✅ 任务完成！成功点击了 {self.click_count} 次，程序将自动退出")
                return True  # 返回True表示任务完成
            else:
                print(f"\n程序已停止，完成了 {self.click_count}/{self.target_clicks} 次点击")
                return False  # 返回False表示未完成任务

    def stop_clicking(self):
        """停止自动点击"""
        self.running = False
        print("正在停止程序...")


def main():
    clicker = AutoMouseClicker()

    print("=== 自动鼠标点击程序 ===")

    while True:
        print("\n请选择操作:")
        print("1. 获取当前鼠标位置")
        print("2. 设置点击位置")
        print("3. 设置点击次数")
        print("4. 开始自动点击")
        print("5. 退出程序")

        choice = input("请输入选项 (1-5): ").strip()

        if choice == "1":
            clicker.get_current_mouse_position()

        elif choice == "2":
            try:
                print("当前鼠标位置:", end=" ")
                clicker.get_current_mouse_position()

                x = int(input("请输入X坐标 (或按回车使用当前鼠标X位置): ") or clicker.get_current_mouse_position()[0])
                y = int(input("请输入Y坐标 (或按回车使用当前鼠标Y位置): ") or clicker.get_current_mouse_position()[1])

                clicker.set_click_position(x, y)
            except ValueError:
                print("请输入有效的数字!")

        elif choice == "3":
            try:
                count = int(input("请输入目标点击次数: "))
                if count > 0:
                    clicker.set_target_clicks(count)
                else:
                    print("点击次数必须大于0!")
            except ValueError:
                print("请输入有效的数字!")

        elif choice == "4":
            if clicker.target_clicks <= 0:
                print("请先设置点击次数！")
                continue

            print(f"\n即将开始自动点击:")
            print(f"位置: ({clicker.click_x}, {clicker.click_y})")
            print(f"次数: {clicker.target_clicks} 次")
            print(f"预计总耗时: 约 {(clicker.target_clicks - 1) * clicker.base_interval / 60:.1f} 分钟")

            confirm = input("确认开始吗？(y/n): ").lower().strip()

            if confirm == 'y' or confirm == 'yes':
                try:
                    # 开始点击，如果完成任务则自动退出程序
                    task_completed = clicker.start_clicking()
                    if task_completed:
                        print("\n程序将在3秒后自动退出...")
                        time.sleep(3)
                        sys.exit(0)  # 自动退出程序
                except KeyboardInterrupt:
                    clicker.stop_clicking()
            else:
                print("已取消")

        elif choice == "5":
            print("程序已退出")
            break

        else:
            print("无效选项，请重新选择")


if __name__ == "__main__":
    main()