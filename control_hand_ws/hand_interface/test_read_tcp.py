from pymodbus.client import ModbusTcpClient

# ===== 配置 =====
HAND_IP = "192.168.123.210"
HAND_PORT = 6000
ANGLE_ACT_REG = 1032   # 六自由度角度寄存器
BASE_ADDR = 1000        # 文档基地址
NUM_FREEDOMS = 6       # 六个自由度

# ===== 连接灵巧手 =====
client = ModbusTcpClient(HAND_IP, port=HAND_PORT)
if not client.connect():
    print("连接失败，请检查 IP 和端口")
    exit(1)

print("连接成功，读取角度实际值...")

# ===== 读取寄存器 =====
addr = ANGLE_ACT_REG - BASE_ADDR
result = client.read_holding_registers(addr, NUM_FREEDOMS)
if result.isError():
    print("读取失败:", result)
else:
    angles = result.registers
    print("实际角度值:", angles)

# ===== 关闭连接 =====
client.close()
