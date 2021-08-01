CREATE TABLE `wh_loupan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT '楼盘名称',
  `lp_type` varchar(255) NOT NULL DEFAULT '' COMMENT '类型，商业/住宅',
  `image` varchar(255) NOT NULL DEFAULT '' COMMENT '缩略图',
  `block` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '区域',
  `address` varchar(255) NOT NULL DEFAULT '' COMMENT '地址',
  `room_type` varchar(255) NOT NULL DEFAULT '' COMMENT '户型',
  `spec` varchar(255) NOT NULL DEFAULT '' COMMENT '建面',
  `ava_price` varchar(20) NOT NULL DEFAULT '' COMMENT '均价 xxx/㎡',
  `total_range` varchar(255) NOT NULL DEFAULT '' COMMENT '总价范围',
  `tags` varchar(255) NOT NULL DEFAULT '' COMMENT '标记',
  `detail_url` varchar(255) NOT NULL DEFAULT '' COMMENT '详情链接',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;