import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from inspire_sdkpy import inspire_dds

if __name__ == "__main__":
    # 初始化 DDS 工厂（同 Publisher）
    import sys
    if len(sys.argv) > 1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)

    # 订阅左右手 topic
    topic_l = "rt/inspire_hand/ctrl/l"
    topic_r = "rt/inspire_hand/ctrl/r"

    sub_l = ChannelSubscriber(topic_l, inspire_dds.inspire_hand_ctrl)
    sub_l.Init()

    sub_r = ChannelSubscriber(topic_r, inspire_dds.inspire_hand_ctrl)
    sub_r.Init()

    print("Subscriber started. Press Ctrl+C to stop.")

    try:
        count = 0
        while True:
            data_l = sub_l.Read()
            data_r = sub_r.Read()

            if data_l:
                print(f"[{count}] L-hand angle_set: {data_l.angle_set}, mode: {data_l.mode}")
            else:
                print(f"[{count}] L-hand: No message yet")

            if data_r:
                print(f"[{count}] R-hand angle_set: {data_r.angle_set}, mode: {data_r.mode}")
            else:
                print(f"[{count}] R-hand: No message yet")

            count += 1
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Subscriber stopped by user.")
