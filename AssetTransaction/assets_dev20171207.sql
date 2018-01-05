/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : assets_dev

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-12-07 14:39:54
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for sl_asset
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset`;
CREATE TABLE `sl_asset` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `asset_no` varchar(255) DEFAULT NULL COMMENT '资产编号',
  `img_url` varchar(255) DEFAULT NULL COMMENT '资产宣传图',
  `subject` varchar(255) DEFAULT NULL COMMENT '资产主题',
  `type` varchar(50) DEFAULT NULL COMMENT '资产类型 1-股权，2-实物资产，3-不动产；4-其他',
  `industry` varchar(255) DEFAULT NULL COMMENT '所属行业',
  `region` varchar(11) DEFAULT NULL COMMENT '所属地区',
  `address` varchar(255) DEFAULT NULL COMMENT '地址 所在地区：辽宁省营口市西市区',
  `transfer_price` decimal(10,2) DEFAULT NULL COMMENT '转让价格(万) -1 面议',
  `transfer_rate` double(10,2) DEFAULT NULL COMMENT '转让份额：百分比',
  `description` text COMMENT '项目描述',
  `remark` text COMMENT '备注',
  `information` text COMMENT '资料',
  `total_review` bigint(20) DEFAULT '0' COMMENT '总浏览量',
  `contact_name` varchar(50) DEFAULT NULL COMMENT '联系人姓名',
  `contact_phone` varchar(50) DEFAULT NULL COMMENT '联系人电话',
  `contact_email` varchar(50) DEFAULT NULL COMMENT '联系人邮箱',
  `contact_address` varchar(50) DEFAULT NULL COMMENT '联系人地址',
  `valuation` decimal(10,0) DEFAULT NULL COMMENT '资产估价 -1=面议',
  `release_time` datetime DEFAULT NULL COMMENT '发布时间',
  `user_id` int(11) DEFAULT NULL COMMENT '资产发布者Id',
  `status` tinyint(3) DEFAULT '1' COMMENT '状态： 1-进行中，2-结束；3-禁用',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sn` (`asset_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of sl_asset
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_consult_log
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_consult_log`;
CREATE TABLE `sl_asset_consult_log` (
  `id` bigint(20) NOT NULL,
  `asset_id` bigint(20) DEFAULT NULL COMMENT '资产Id',
  `asset_no` varchar(255) DEFAULT NULL COMMENT '资产编号',
  `user_id` bigint(20) DEFAULT NULL COMMENT '会员Id',
  `user_mobile` varchar(255) DEFAULT NULL COMMENT '会员手机号码',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态 0-未处理；1-已处理',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资产咨询记录';

-- ----------------------------
-- Records of sl_asset_consult_log
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_item_entity
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_item_entity`;
CREATE TABLE `sl_asset_item_entity` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `asset_no` varchar(255) DEFAULT NULL COMMENT '资产编号',
  `category` varchar(255) DEFAULT NULL COMMENT '实物类型',
  `trade_type` varchar(255) DEFAULT NULL COMMENT '交易方式',
  `num` int(255) DEFAULT NULL COMMENT '数量',
  `life` int(255) DEFAULT NULL COMMENT '年限',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sn` (`asset_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实物资产';

-- ----------------------------
-- Records of sl_asset_item_entity
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_item_house
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_item_house`;
CREATE TABLE `sl_asset_item_house` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `asset_no` varchar(255) DEFAULT NULL COMMENT '资产编号',
  `category` varchar(255) DEFAULT NULL COMMENT '分类',
  `trade_type` varchar(255) DEFAULT NULL COMMENT '交易方式',
  `area` double(255,2) DEFAULT NULL COMMENT ' 房屋面积(平方米):',
  `use_area` varchar(255) DEFAULT NULL COMMENT '使用权面积(平方米)',
  `owner` varchar(255) DEFAULT NULL COMMENT '房屋所有权人',
  `located` varchar(255) DEFAULT NULL COMMENT '房屋坐落',
  `use_type` varchar(255) DEFAULT NULL COMMENT '土地用途:分类为土地or房屋+土地时显示',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sn` (`asset_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='不动产';

-- ----------------------------
-- Records of sl_asset_item_house
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_item_ore
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_item_ore`;
CREATE TABLE `sl_asset_item_ore` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `asset_no` varchar(255) DEFAULT NULL COMMENT '资产编号',
  `category` varchar(255) DEFAULT NULL COMMENT '分类',
  `report_store` int(255) DEFAULT NULL COMMENT '报告储量',
  `fact_store` int(255) DEFAULT NULL COMMENT '实际储量',
  `have_store` int(255) DEFAULT NULL COMMENT '保有储量',
  `explore_card` varchar(255) DEFAULT NULL COMMENT '探矿权证',
  `mining_card` varchar(255) DEFAULT NULL COMMENT '采矿权证',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sn` (`asset_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='矿产';

-- ----------------------------
-- Records of sl_asset_item_ore
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_spread
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_spread`;
CREATE TABLE `sl_asset_spread` (
  `id` int(11) NOT NULL,
  `asset_id` bigint(11) DEFAULT NULL COMMENT '资产Id',
  `level` tinyint(3) DEFAULT '0' COMMENT '优先级',
  `img_url` varchar(255) DEFAULT NULL COMMENT '资产宣传图',
  `subject` varchar(255) DEFAULT NULL COMMENT '资产主题',
  `type` int(11) DEFAULT NULL COMMENT '资产类型 1-股权，2-实物资产，3-不动产；4-其他',
  `status` tinyint(3) DEFAULT '1' COMMENT '状态： 0-禁用；2-启用',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目推广';

-- ----------------------------
-- Records of sl_asset_spread
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_spread_key
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_spread_key`;
CREATE TABLE `sl_asset_spread_key` (
  `id` int(11) NOT NULL,
  `asset_id` bigint(11) DEFAULT NULL COMMENT '资产Id',
  `level` tinyint(3) DEFAULT '0' COMMENT '优先级',
  `img_url` varchar(255) DEFAULT NULL COMMENT '资产宣传图',
  `subject` varchar(255) DEFAULT NULL COMMENT '资产主题',
  `type` int(11) DEFAULT NULL COMMENT '资产类型 1-股权，2-实物资产，3-不动产；4-其他',
  `status` tinyint(3) DEFAULT '1' COMMENT '状态： 0-禁用；2-启用',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='重点项目';

-- ----------------------------
-- Records of sl_asset_spread_key
-- ----------------------------

-- ----------------------------
-- Table structure for sl_asset_spread_recommend
-- ----------------------------
DROP TABLE IF EXISTS `sl_asset_spread_recommend`;
CREATE TABLE `sl_asset_spread_recommend` (
  `id` int(11) NOT NULL,
  `asset_id` bigint(11) DEFAULT NULL COMMENT '资产Id',
  `level` tinyint(3) DEFAULT '0' COMMENT '优先级',
  `img_url` varchar(255) DEFAULT NULL COMMENT '资产宣传图',
  `subject` varchar(255) DEFAULT NULL COMMENT '资产主题',
  `region` varchar(11) DEFAULT NULL COMMENT '所属地区',
  `type` int(11) DEFAULT NULL COMMENT '资产类型 1-股权，2-实物资产，3-不动产；4-其他',
  `transfer_price` decimal(10,2) DEFAULT NULL COMMENT '转让价格 -1 面议',
  `status` tinyint(3) DEFAULT '1' COMMENT '状态： 0-禁用；2-启用',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目推荐';

-- ----------------------------
-- Records of sl_asset_spread_recommend
-- ----------------------------

-- ----------------------------
-- Table structure for sl_banner
-- ----------------------------
DROP TABLE IF EXISTS `sl_banner`;
CREATE TABLE `sl_banner` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `link_url` varchar(256) DEFAULT NULL COMMENT '页面跳转url',
  `img_url` varchar(256) DEFAULT NULL COMMENT '图片url',
  `level` tinyint(3) DEFAULT '0' COMMENT '优先级',
  `position` tinyint(4) DEFAULT NULL COMMENT 'banner位置 1-首页顶部',
  `platform_id` bigint(11) DEFAULT NULL COMMENT '平台编号',
  `introduction` varchar(256) DEFAULT NULL COMMENT '介绍',
  `status` tinyint(3) DEFAULT '1' COMMENT '状态： 0-禁用；2-启用',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='banner表';

-- ----------------------------
-- Records of sl_banner
-- ----------------------------

-- ----------------------------
-- Table structure for sl_partner
-- ----------------------------
DROP TABLE IF EXISTS `sl_partner`;
CREATE TABLE `sl_partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '合作伙伴名称',
  `logo` varchar(500) DEFAULT NULL COMMENT '合作伙伴logo',
  `link_url` varchar(500) DEFAULT NULL COMMENT '合作伙伴页面跳转链接',
  `level` int(255) DEFAULT NULL COMMENT '优先级',
  `introduction` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT '介绍',
  `status` tinyint(3) DEFAULT '1' COMMENT '状态： 0-禁用；2-启用',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='合作机构';

-- ----------------------------
-- Records of sl_partner
-- ----------------------------

-- ----------------------------
-- Table structure for sl_user
-- ----------------------------
DROP TABLE IF EXISTS `sl_user`;
CREATE TABLE `sl_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `user_name` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT '登录用户名',
  `password` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT '密码',
  `nick` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '昵称',
  `avetor_url` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '头像',
  `mobile` varchar(16) CHARACTER SET utf8 NOT NULL COMMENT '手机号',
  `name` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '姓名',
  `id_card` varchar(32) CHARACTER SET utf8 DEFAULT NULL COMMENT '身份证',
  `gender` char(1) CHARACTER SET utf8 DEFAULT '0' COMMENT '性别：0未知、1代表男、2代表女',
  `latitude` decimal(10,5) DEFAULT NULL COMMENT '经度',
  `longitude` decimal(10,5) DEFAULT NULL COMMENT '纬度',
  `address` varchar(255) DEFAULT NULL COMMENT '地址',
  `status` char(1) CHARACTER SET utf8 NOT NULL DEFAULT '0' COMMENT '用户状态：0代表正常、1禁止使用',
  `type` int(11) DEFAULT '1' COMMENT '注册类型 1-手机号码',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_mobile` (`mobile`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- Records of sl_user
-- ----------------------------

-- ----------------------------
-- Table structure for sl_user_reg_log
-- ----------------------------
DROP TABLE IF EXISTS `sl_user_reg_log`;
CREATE TABLE `sl_user_reg_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户ID',
  `reg_account` varchar(16) CHARACTER SET utf8 DEFAULT NULL COMMENT '注冊信息 手机号/邮箱/用户名/微信/QQ',
  `reg_ip` varchar(255) DEFAULT NULL COMMENT '注册IP',
  `device_sn` varchar(255) DEFAULT NULL COMMENT '注册设备编号 1-Android；2-ios; 3-web',
  `latitude` decimal(10,5) DEFAULT NULL COMMENT '经度',
  `longitude` decimal(10,5) DEFAULT NULL COMMENT '纬度',
  `address` varchar(255) DEFAULT NULL COMMENT '地址',
  `type` int(11) DEFAULT '1' COMMENT '注册类型 1-手机号码',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_mobile` (`reg_account`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- Records of sl_user_reg_log
-- ----------------------------
