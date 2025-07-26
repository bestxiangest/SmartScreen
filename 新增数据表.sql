-- --------------------------------------------------------
-- Smart Laboratory Database Schema for New Features (Simplified Version)
-- Version: 2.1
-- --------------------------------------------------------

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- 模块一: 仓库物料管理
-- ----------------------------

-- 1. 物料分类表 (保留)
DROP TABLE IF EXISTS `material_categories`;
CREATE TABLE `material_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL COMMENT '分类名称',
  `description` TEXT COMMENT '分类描述',
  `parent_id` INT NULL COMMENT '父分类ID，用于层级结构',
  `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序值',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`parent_id`) REFERENCES `material_categories`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='仓库物料分类表';

-- 2. 物料主表 (保留)
DROP TABLE IF EXISTS `materials`;
CREATE TABLE `materials` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(50) NOT NULL UNIQUE COMMENT '物料编码，唯一',
  `name` VARCHAR(150) NOT NULL COMMENT '物料名称',
  `category_id` INT NOT NULL COMMENT '物料分类ID',
  `description` TEXT COMMENT '物料描述',
  `unit` VARCHAR(20) NOT NULL COMMENT '计量单位',
  `stock_quantity` INT NOT NULL DEFAULT 0 COMMENT '当前库存数量',
  `min_stock` INT COMMENT '最小安全库存',
  `max_stock` INT COMMENT '最大库存',
  `unit_price` DECIMAL(10, 2) COMMENT '单价',
  `location` VARCHAR(100) COMMENT '存放位置 (例如: A区-01-03)',
  `supplier` VARCHAR(150) COMMENT '供应商',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`category_id`) REFERENCES `material_categories`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='仓库物料主表';

-- 3. 物料申领表 (简化)
-- 合并了申领主表和详情表
DROP TABLE IF EXISTS `material_requests`;
CREATE TABLE `material_requests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `request_number` VARCHAR(50) NOT NULL UNIQUE COMMENT '申领单号 (例如: REQ202401150001)',
  `user_id` INT NOT NULL COMMENT '申领人ID',
  `project_name` VARCHAR(150) COMMENT '关联的项目名称',
  `status` ENUM('pending', 'approved', 'rejected', 'issued', 'returned', 'overdue') NOT NULL DEFAULT 'pending' COMMENT '申领状态',
  `materials` JSON NOT NULL COMMENT '申领的物料列表, 例如: [{"material_id": 1, "quantity": 2, "purpose": "项目制作"}]',
  `approved_materials` JSON COMMENT '批准的物料列表, 例如: [{"material_id": 1, "approved_quantity": 2}]',
  `expected_return_date` DATE COMMENT '预期归还日期',
  `notes` TEXT COMMENT '申领备注',
  `approver_id` INT COMMENT '审批人ID',
  `approved_at` TIMESTAMP NULL COMMENT '审批时间',
  `approval_comment` TEXT COMMENT '审批意见',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`approver_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='物料申领表 (简化版)';

-- 4. 物料出入库记录表 (保留)
DROP TABLE IF EXISTS `material_transactions`;
CREATE TABLE `material_transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `material_id` INT NOT NULL COMMENT '物料ID',
  `transaction_type` ENUM('in', 'out', 'return', 'adjust') NOT NULL COMMENT '交易类型',
  `quantity` INT NOT NULL COMMENT '变动数量',
  `before_quantity` INT NOT NULL COMMENT '变动前库存',
  `after_quantity` INT NOT NULL COMMENT '变动后库存',
  `user_id` INT COMMENT '操作人ID',
  `request_id` INT COMMENT '关联的申领单ID',
  `notes` TEXT COMMENT '备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`material_id`) REFERENCES `materials`(`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`request_id`) REFERENCES `material_requests`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='物料出入库记录表';


-- ----------------------------
-- 模块二: 维修工单管理
-- ----------------------------

-- 5. 维修工单表 (简化)
-- 合并了工单主表和备件使用表
DROP TABLE IF EXISTS `maintenance_orders`;
CREATE TABLE `maintenance_orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_number` VARCHAR(50) NOT NULL UNIQUE COMMENT '工单号 (例如: MO202401150001)',
  `device_id` INT NOT NULL COMMENT '报修设备ID',
  `fault_type` ENUM('hardware', 'software', 'network', 'power', 'other') NOT NULL COMMENT '故障类型',
  `fault_description` TEXT NOT NULL COMMENT '故障描述',
  `images` JSON COMMENT '故障图片URL列表',
  `priority` ENUM('low', 'medium', 'high', 'urgent') NOT NULL DEFAULT 'medium' COMMENT '优先级',
  `status` ENUM('pending', 'assigned', 'in_progress', 'completed', 'cancelled') NOT NULL DEFAULT 'pending' COMMENT '工单状态',
  `reporter_id` INT NOT NULL COMMENT '报修人ID',
  `assignee_id` INT COMMENT '维修人员ID',
  `reported_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报修时间',
  `assigned_at` TIMESTAMP NULL COMMENT '分配时间',
  `expected_completion` DATETIME COMMENT '预期完成时间',
  `actual_completion` DATETIME COMMENT '实际完成时间',
  `solution_description` TEXT COMMENT '解决方案描述',
  `maintenance_notes` TEXT COMMENT '维修备注',
  `completion_images` JSON COMMENT '维修完成图片URL列表',
  `parts_used` JSON COMMENT '使用的零件列表, 例如: [{"part_name": "激光头", "quantity": 1, "cost": 500.00}]',
  PRIMARY KEY (`id`),
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`id`),
  FOREIGN KEY (`reporter_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`assignee_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='维修工单表 (简化版)';


-- ----------------------------
-- 模块三: 值班调度管理
-- ----------------------------

-- 6. 值班安排与日志表 (简化)
-- 合并了值班安排和值班日志表
DROP TABLE IF EXISTS `duty_schedules`;
CREATE TABLE `duty_schedules` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL COMMENT '值班人员ID',
  `duty_date` DATE NOT NULL COMMENT '值班日期',
  `shift_type` ENUM('morning', 'afternoon', 'evening', 'night') NOT NULL COMMENT '班次类型',
  `start_time` TIME NOT NULL COMMENT '开始时间',
  `end_time` TIME NOT NULL COMMENT '结束时间',
  `location` VARCHAR(100) COMMENT '值班地点',
  `responsibilities` JSON COMMENT '职责列表',
  `status` ENUM('scheduled', 'completed', 'absent', 'leave', 'substituted') NOT NULL DEFAULT 'scheduled' COMMENT '值班状态',
  `substitute_id` INT COMMENT '替班人ID',
  `notes` TEXT COMMENT '安排备注',
  `check_in_time` TIMESTAMP NULL COMMENT '签到时间',
  `check_in_location` VARCHAR(100) COMMENT '签到地点',
  `check_in_notes` TEXT COMMENT '签到备注',
  `check_out_time` TIMESTAMP NULL COMMENT '签退时间',
  `summary` TEXT COMMENT '工作总结',
  `issues` JSON COMMENT '遇到的问题列表',
  `handover_notes` TEXT COMMENT '交接班备注',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`substitute_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='值班安排与日志表 (简化版)';


SET FOREIGN_KEY_CHECKS = 1;

-- --------------------------------------------------------
-- 插入示例数据 (用户ID已更新)
-- --------------------------------------------------------

-- 1. 物料分类数据
INSERT INTO `material_categories` (`id`, `name`, `description`, `parent_id`, `sort_order`) VALUES
(1, '电子元件', '各类电子元器件', NULL, 1),
(2, '开发板与模块', '各种MCU、SBC开发板及功能模块', NULL, 2),
(3, '工具耗材', '焊接工具、导线、3D打印耗材等', NULL, 3),
(4, '传感器', '用于感知环境的各类传感器', 1, 1),
(5, '无源器件', '电阻、电容、电感等', 1, 2);

-- 2. 物料主数据
INSERT INTO `materials` (`id`, `code`, `name`, `category_id`, `description`, `unit`, `stock_quantity`, `min_stock`, `location`, `supplier`) VALUES
(1, 'MAT001', 'Arduino Uno R3', 2, '经典款Arduino开发板', '块', 25, 5, 'A区-01-03', 'Arduino官方'),
(2, 'MAT002', '树莓派4B 4GB', 2, 'Raspberry Pi 4 Model B 4GB内存版', '块', 10, 2, 'A区-01-04', 'Raspberry Pi基金会'),
(3, 'RES10K', '10K欧姆电阻', 5, '1/4W 5%精度碳膜电阻', '个', 500, 100, 'B区-元件盒-01', '电子元件供应商'),
(4, 'PLA001', '白色PLA打印耗材', 3, '1.75mm直径，1KG装', '卷', 8, 2, 'C区-3D打印区', '3D打印耗材商');

-- 3. 物料申领数据
INSERT INTO `material_requests` (`id`, `request_number`, `user_id`, `project_name`, `status`, `materials`, `approved_materials`, `expected_return_date`, `notes`, `approver_id`, `approved_at`, `approval_comment`) VALUES
(1, 'REQ202507260001', 6, '智能家居控制系统', 'approved', '[{"material_id": 1, "quantity": 2, "purpose": "项目原型制作"}, {"material_id": 3, "quantity": 50, "purpose": "电路焊接"}]', '[{"material_id": 1, "approved_quantity": 2}, {"material_id": 3, "approved_quantity": 50}]', '2025-09-01', '用于毕业设计项目', 7, '2025-07-26 09:30:00', '审批通过，请注意节约使用。');

-- 4. 物料出入库记录数据
INSERT INTO `material_transactions` (`material_id`, `transaction_type`, `quantity`, `before_quantity`, `after_quantity`, `user_id`, `request_id`, `notes`) VALUES
(1, 'in', 20, 5, 25, 8, NULL, '新采购入库'),
(1, 'out', 2, 25, 23, 6, 1, '申领单REQ202507260001出库'),
(3, 'out', 50, 500, 450, 6, 1, '申领单REQ202507260001出库');

-- 5. 维修工单数据 (假设设备ID=4存在)
INSERT INTO `maintenance_orders` (`id`, `order_number`, `device_id`, `fault_type`, `fault_description`, `images`, `priority`, `status`, `reporter_id`, `assignee_id`, `reported_at`, `assigned_at`, `expected_completion`, `actual_completion`, `solution_description`, `parts_used`) VALUES
(1, 'MO202507260001', 4, 'power', '设备无法开机，电源指示灯不亮。', '["/uploads/fault_image1.jpg"]', 'high', 'completed', 9, 10, '2025-07-25 14:00:00', '2025-07-25 14:30:00', '2025-07-26 18:00:00', '2025-07-26 11:00:00', '更换了内部电源模块，并对接口进行加固。', '[{"part_name": "电源模块-XYZ型", "quantity": 1, "cost": 150.00}]');

-- 6. 值班安排与日志数据
INSERT INTO `duty_schedules` (`id`, `user_id`, `duty_date`, `shift_type`, `start_time`, `end_time`, `location`, `responsibilities`, `status`, `substitute_id`, `notes`, `check_in_time`, `check_out_time`, `summary`) VALUES
(1, 11, '2025-07-26', 'morning', '08:00:00', '12:00:00', '通信电子创新基地A区', '["设备巡检", "安全监督"]', 'completed', NULL, '重点关注3D打印机运行状态', '2025-07-26 07:58:00', '2025-07-26 12:05:00', '上午值班期间无异常，完成所有设备巡检。'),
(2, 6, '2025-07-26', 'afternoon', '14:00:00', '18:00:00', '通信电子创新基地B区', '["实验指导", "物料管理"]', 'scheduled', NULL, '下午有新生参观，请做好引导。', NULL, NULL, NULL);
