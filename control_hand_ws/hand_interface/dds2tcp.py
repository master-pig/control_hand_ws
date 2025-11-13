import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from inspire_sdkpy import inspire_dds
from pymodbus.client import ModbusTcpClient

# ====== Modbus 配置 ======
HAND_IP = "192.168.123.210"   # 灵巧手 IP
HAND_PORT = 6000
ANGLE_SET = 1486
FORCE_SET = 1498

# ====== 连接灵巧手 ======
client = ModbusTcpClient(HAND_IP, port=HAND_PORT)
if not client.connect():
    print("连接灵巧手失败，请检查 IP 和端口")
    exit(1)
print("✅ Modbus 已连接")

# ====== DDS 初始化 ======
ChannelFactoryInitialize(0)   # 可以根据需要传入配置文件路径
topic = "rt/inspire_hand/ctrl/l"  # 订阅左手控制话题

sub = ChannelSubscriber(topic, inspire_dds.inspire_hand_ctrl)
sub.Init()
print(f"✅ 已订阅 DDS 话题: {topic}")

# ====== 主循环 ======
try:
    count = 0
    while True:
        msg = sub.Read()
        if msg:
            # DDS 控制消息中通常有 angle_set 和 mode 等字段
            angles = msg.angle_set[:6]  # 取前6个关节角度
            print(f"[{count}] 收到控制命令: {angles}")

            # 通过 Modbus 写入角度
            client.write_registers(ANGLE_SET, angles)
            print(f"已通过 Modbus 发送角度指令: {angles}")
        else:
            print(f"[{count}] 暂无新DDS消息")

        count += 1
        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 停止")
finally:
    client.close()
    print("🔌 已关闭 Modbus 连接")
