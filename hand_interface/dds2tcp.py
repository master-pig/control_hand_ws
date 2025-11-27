from http import client
import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from inspire_sdkpy import inspire_dds
from pymodbus.client import ModbusTcpClient

# ====== Modbus 配置 ======
HAND_IP = "192.168.123.211"   # 灵巧手 IP
HAND_PORT = 6000
ANGLE_SET = 1486
FORCE_SET = 1498
class DDSHandler():
    def __init__(self, client):
        # ====== 连接灵巧手 ======
        self.client = ModbusTcpClient(HAND_IP, port=HAND_PORT)
        if not self.client.connect():
            print("连接灵巧手失败，请检查 IP 和端口")
            exit(1)
        print("✅ Modbus 已连接")
            # ====== DDS 初始化 ======
        ChannelFactoryInitialize(0)   # 可以根据需要传入配置文件路径
        topic = "rt/inspire_hand/ctrl/l"  # 订阅左手控制话题

        sub = ChannelSubscriber(topic, inspire_dds.inspire_hand_ctrl)
        sub.Init(handler=self.on_dds_message, queueLen=5)
        print(f"✅ 已订阅 DDS 话题: {topic}")


    def on_dds_message(self, msg:inspire_dds.inspire_hand_touch):
        angles = msg.angle_set[:6]
        print(f"📡 收到角度: {angles}")
        self.client.write_registers(ANGLE_SET, angles)
        print(f"已写入 Modbus: {angles}")


def main():
    handler = DDSHandler(None)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()