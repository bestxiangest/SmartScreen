-- 为users表添加专业、班级、头像URL字段
-- 执行时间: 2024-01-01
-- 描述: 添加三个非必填字段：专业(major)、班级(class)、头像URL(avatar_url)

ALTER TABLE `users` 
ADD COLUMN `major` VARCHAR(100) NULL COMMENT '专业' AFTER `full_name`, 
ADD COLUMN `class` VARCHAR(50) NULL COMMENT '班级' AFTER `major`, 
ADD COLUMN `avatar_url` VARCHAR(255) NULL COMMENT '头像图片URL' AFTER `face_data`;

-- 验证字段添加成功
DESC users;