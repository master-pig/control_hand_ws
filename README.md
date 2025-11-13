📦 hand_control_ws/          ← ROS2 工作空间
 ├── src/
 │   ├── camera_hand_tracker/    ← 手部关键点检测节点（Python）
 │   ├── hand_motion_mapper/     ← 关键点到机械手指令映射节点（Python / C++）
 │   └── inspire_hand_driver/    ← 灵巧手DDS通信节点（基于Inspire官方SDK）
 ├── install/
 ├── build/
 └── README.md

+---------------------+          +-------------------------+          +---------------------------+
|  camera_hand_tracker |  --->    |   hand_motion_mapper   |  --->    |  inspire_hand_driver      |
|  (发布关键点Topic)     |          | (计算目标姿态)           |          | (发送DDS控制命令)           |
| /camera/hand_keypoint|          | /hand/target_pose      |          | rt/inspire_hand/ctrl/r    |
+---------------------+          +-------------------------+          +---------------------------+
