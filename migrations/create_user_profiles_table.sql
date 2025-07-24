-- 创建用户个人资料表
-- 执行时间: 2024-01-01
-- 描述: 为小程序端个人主页功能创建用户个人资料表

DROP TABLE IF EXISTS `user_profiles`;

CREATE TABLE `user_profiles` (
  `user_id` INT NOT NULL COMMENT '用户ID，关联users表的主键，同时也是本表主键',
  `gender` ENUM('男', '女', '保密') NULL DEFAULT '保密' COMMENT '性别',
  `birth_date` DATE NULL COMMENT '出生日期',
  `position` VARCHAR(100) NULL COMMENT '职务（例如：项目组长、成员、2023级负责人）',
  `dormitory` VARCHAR(100) NULL COMMENT '宿舍信息（例如：2栋305室）',
  `tech_stack` JSON NULL COMMENT '技术栈，使用JSON数组存储，例如：["Python", "Vue.js", "MySQL"]',
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_user_profiles_to_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户个人资料表';

-- 验证表创建成功
DESC user_profiles;

-- 插入示例数据（可选）
INSERT INTO `user_profiles` (`user_id`, `gender`, `birth_date`, `position`, `dormitory`, `tech_stack`) VALUES
(1, '男', '2000-01-15', '实验室负责人', '1栋101室', '["Python", "Flask", "MySQL", "Vue.js"]'),
(2, '女', '2001-03-20', '项目组长', '2栋205室', '["Java", "Spring Boot", "React", "PostgreSQL"]'),
(3, '保密', '1999-12-10', '技术成员', '3栋308室', '["JavaScript", "Node.js", "MongoDB", "Express"]');

-- 查看插入的数据
SELECT * FROM user_profiles;