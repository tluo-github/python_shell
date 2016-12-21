/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : spider

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2016-12-21 18:11:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jsh_app_cheap_room2
-- ----------------------------
DROP TABLE IF EXISTS `jsh_app_cheap_room2`;
CREATE TABLE `jsh_app_cheap_room2` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '二手房id',
  `cheap_room_name` varchar(255) DEFAULT NULL COMMENT '二手房名称（标题）',
  `cheap_room_image` varchar(255) DEFAULT NULL COMMENT '二手房图片',
  `cheap_room_releasetime` varchar(255) DEFAULT NULL COMMENT '发布时间',
  `cheap_room_price` varchar(255) DEFAULT NULL COMMENT '二手房售价',
  `cheap_room_unit` varchar(255) DEFAULT NULL COMMENT '二手房户型（一室一厅）',
  `cheap_room_acreage` varchar(255) DEFAULT NULL COMMENT '二手房面积',
  `cheap_room_label` varchar(255) DEFAULT NULL COMMENT '二手房标签（急售、黄金楼层）',
  `cheap_room_unit_price` varchar(255) DEFAULT NULL COMMENT '二手房单价',
  `cheap_room_towards` varchar(255) DEFAULT NULL COMMENT '二手房朝向',
  `cheap_room_floor` varchar(255) DEFAULT NULL COMMENT '二手房楼层',
  `cheap_room_decoration` varchar(255) DEFAULT NULL COMMENT '二手房装修类型',
  `cheap_room_area` varchar(255) DEFAULT NULL COMMENT '区域',
  `cheap_room_decade` varchar(255) DEFAULT NULL COMMENT '房龄',
  `cheap_room_cell` varchar(255) DEFAULT NULL COMMENT '小区',
  `cheap_room_description` text COMMENT '房源描述',
  `cheap_room_promulgator` varchar(255) DEFAULT NULL COMMENT '发布者',
  `cheap_room_telephone` varchar(255) DEFAULT NULL COMMENT '发布者电话',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4814 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for jsh_app_qq
-- ----------------------------
DROP TABLE IF EXISTS `jsh_app_qq`;
CREATE TABLE `jsh_app_qq` (
  `id` int(14) NOT NULL AUTO_INCREMENT,
  `property_name` varchar(255) DEFAULT NULL COMMENT '名称',
  `property_image` varchar(255) DEFAULT NULL COMMENT '图片',
  `property_area` varchar(255) DEFAULT NULL COMMENT '区域',
  `property_label` varchar(255) DEFAULT NULL COMMENT '标签',
  `property_price` varchar(255) DEFAULT NULL COMMENT '价格',
  `property_address` varchar(255) DEFAULT NULL COMMENT '楼盘地址',
  `property_opentime` varchar(255) DEFAULT NULL COMMENT '开盘时间',
  `property_deliverytime` varchar(255) DEFAULT NULL COMMENT '入住时间',
  `property_type` varchar(255) DEFAULT NULL COMMENT '物业类别',
  `property_chuanquaninanxian` varchar(255) DEFAULT NULL COMMENT '产权年限',
  `property_zhuangxiu` varchar(255) DEFAULT NULL COMMENT '装修情况',
  `property_jianzhu_type` varchar(255) DEFAULT NULL COMMENT '建筑类别',
  `property_households_number` varchar(255) DEFAULT NULL COMMENT '总户数',
  `property_zhandimianji` varchar(255) DEFAULT NULL COMMENT '占地面积',
  `property_jianzhummianji` varchar(255) DEFAULT NULL COMMENT '建筑面积',
  `property_greening_rate` varchar(255) DEFAULT NULL COMMENT '绿化率',
  `property_volume_rate` varchar(255) DEFAULT NULL COMMENT '容积率',
  `property_developers` varchar(255) DEFAULT NULL COMMENT '开发商',
  `property_yushouzheng` varchar(255) DEFAULT NULL COMMENT '预售证',
  `property_costs` varchar(255) DEFAULT NULL COMMENT '物业公司',
  `property_introduce` text COMMENT '楼盘简介',
  `property_parking_space` varchar(255) DEFAULT NULL COMMENT '停车位',
  `property_tel` varchar(255) DEFAULT NULL COMMENT '售楼处电话',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=346 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for jsh_app_test
-- ----------------------------
DROP TABLE IF EXISTS `jsh_app_test`;
CREATE TABLE `jsh_app_test` (
  `id` int(14) NOT NULL AUTO_INCREMENT,
  `property_name` varchar(255) DEFAULT NULL COMMENT '名称',
  `property_image` varchar(255) DEFAULT NULL COMMENT '图片',
  `property_tel` varchar(255) DEFAULT NULL COMMENT '售楼处电话',
  `property_address` varchar(255) DEFAULT NULL COMMENT '楼盘地址',
  `property_price` varchar(255) DEFAULT NULL COMMENT '价格',
  `property_deliverytime` varchar(255) DEFAULT NULL COMMENT '入住时间',
  `property_salesoffices` varchar(255) DEFAULT NULL COMMENT '售楼处',
  `property_type` varchar(255) DEFAULT NULL COMMENT '物业类型',
  `property_volume_rate` varchar(255) DEFAULT NULL COMMENT '容积率',
  `property_greening_rate` varchar(255) DEFAULT NULL COMMENT '绿化',
  `property_developers` varchar(255) DEFAULT NULL COMMENT '开发商',
  `property_costs` varchar(255) DEFAULT NULL COMMENT '物业费',
  `property_introduce` text COMMENT '项目简介',
  `property_households_number` varchar(255) DEFAULT NULL COMMENT '规划户数',
  `property_parking_space` varchar(255) DEFAULT NULL COMMENT '停车位',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=402 DEFAULT CHARSET=utf8;
