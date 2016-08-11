-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2016-08-11 19:45:06
-- 服务器版本： 10.1.13-MariaDB
-- PHP Version: 5.6.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `howie`
--

-- --------------------------------------------------------

--
-- 表的结构 `get_news`
--

CREATE TABLE `get_news` (
  `news_id` varchar(20) NOT NULL,
  `news_link` varchar(200) DEFAULT NULL,
  `source` varchar(20) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(50) NOT NULL,
  `abstract` varchar(500) NOT NULL,
  `tag` varchar(20) NOT NULL,
  `text_content` mediumtext NOT NULL,
  `html_content` mediumtext NOT NULL,
  `image` varchar(1000) DEFAULT NULL,
  `keyword` varchar(100) NOT NULL,
  `is_old` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `news_comment`
--

CREATE TABLE `news_comment` (
  `news_id` varchar(20) NOT NULL,
  `comment` varchar(20000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `news_feedback`
--

CREATE TABLE `news_feedback` (
  `user_id` varchar(10) NOT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `getTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `reply` varchar(200) DEFAULT NULL,
  `replyTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `isReply` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `news_feedback`
--

INSERT INTO `news_feedback` (`user_id`, `feedback`, `getTime`, `reply`, `replyTime`, `isReply`) VALUES
('000002', 'Good', '2016-06-14 13:19:23', NULL, '0000-00-00 00:00:00', 0),
('000002', 'Good', '2016-06-14 13:25:15', NULL, '0000-00-00 00:00:00', 0);

-- --------------------------------------------------------

--
-- 替换视图以便查看 `news_hot`
--
CREATE TABLE `news_hot` (
`news_id` varchar(20)
,`time` timestamp
,`image` varchar(1000)
,`abstract` varchar(500)
,`source` varchar(20)
,`title` varchar(50)
,`tag` varchar(20)
,`love_times` int(11)
,`read_times` int(11)
,`comment_times` int(11)
);

-- --------------------------------------------------------

--
-- 表的结构 `news_mess`
--

CREATE TABLE `news_mess` (
  `news_id` varchar(20) NOT NULL,
  `tag` varchar(20) NOT NULL,
  `read_times` int(11) NOT NULL DEFAULT '0',
  `love_times` int(11) NOT NULL DEFAULT '0',
  `comment_times` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `news_nums`
--

CREATE TABLE `news_nums` (
  `tag` varchar(20) NOT NULL,
  `nums` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 替换视图以便查看 `news_nums_view`
--
CREATE TABLE `news_nums_view` (
`tag` varchar(20)
,`count` bigint(21)
);

-- --------------------------------------------------------

--
-- 表的结构 `news_recommend`
--

CREATE TABLE `news_recommend` (
  `user_id` varchar(10) NOT NULL,
  `news_score` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `news_tag_chinese`
--

CREATE TABLE `news_tag_chinese` (
  `news_society` varchar(20) DEFAULT NULL,
  `news_entertainment` varchar(20) DEFAULT NULL,
  `news_tech` varchar(20) DEFAULT NULL,
  `news_car` varchar(20) DEFAULT NULL,
  `news_sports` varchar(20) DEFAULT NULL,
  `news_finance` varchar(20) DEFAULT NULL,
  `news_military` varchar(20) DEFAULT NULL,
  `news_world` varchar(20) DEFAULT NULL,
  `news_fashion` varchar(20) DEFAULT NULL,
  `news_travel` varchar(20) DEFAULT NULL,
  `news_discovery` varchar(20) DEFAULT NULL,
  `news_baby` varchar(20) DEFAULT NULL,
  `news_regimen` varchar(20) DEFAULT NULL,
  `news_story` varchar(20) DEFAULT NULL,
  `news_essay` varchar(20) DEFAULT NULL,
  `news_game` varchar(20) DEFAULT NULL,
  `news_history` varchar(20) DEFAULT NULL,
  `news_food` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `news_tag_chinese`
--

INSERT INTO `news_tag_chinese` (`news_society`, `news_entertainment`, `news_tech`, `news_car`, `news_sports`, `news_finance`, `news_military`, `news_world`, `news_fashion`, `news_travel`, `news_discovery`, `news_baby`, `news_regimen`, `news_story`, `news_essay`, `news_game`, `news_history`, `news_food`) VALUES
('社会', '娱乐', '科技', '汽车', '体育', ' 财经', '军事', '国际', '时尚', '旅游', '探索', '育儿', '养生', '故事', '美文', '游戏', '历史', '美食');

-- --------------------------------------------------------

--
-- 表的结构 `news_tag_deep`
--

CREATE TABLE `news_tag_deep` (
  `news_id` varchar(20) NOT NULL,
  `news_society` double DEFAULT NULL,
  `news_entertainment` double DEFAULT NULL,
  `news_tech` double DEFAULT NULL,
  `news_car` double DEFAULT NULL,
  `news_sports` double DEFAULT NULL,
  `news_finance` double DEFAULT NULL,
  `news_military` double DEFAULT NULL,
  `news_world` double DEFAULT NULL,
  `news_fashion` double DEFAULT NULL,
  `news_travel` double DEFAULT NULL,
  `news_discovery` double DEFAULT NULL,
  `news_baby` double DEFAULT NULL,
  `news_regimen` double DEFAULT NULL,
  `news_story` double DEFAULT NULL,
  `news_essay` double DEFAULT NULL,
  `news_game` double DEFAULT NULL,
  `news_history` double DEFAULT NULL,
  `news_food` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `n_admin`
--

CREATE TABLE `n_admin` (
  `id` int(11) NOT NULL,
  `name` varchar(10) NOT NULL,
  `pass` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `n_admin`
--

INSERT INTO `n_admin` (`id`, `name`, `pass`) VALUES
(2, 'admin', 'b49515ad6e147d962c8696f31694ad8d');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `user_id` varchar(10) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `passwd` varchar(40) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`user_id`, `phone`, `name`, `passwd`, `time`) VALUES
('000001', '15767956536', 'howie', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000002', '15767956890', '用户157****890', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000003', '15767976598', '用户157****598', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000004', '15767979609', '用户157****609', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000005', '15766954544', '用户157****544', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000006', '15766954533', '用户157****533', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000007', '15766954531', '用户157****531', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000008', '12345678910', '用户123****910', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000009', '12345678916', '用户123****916', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000010', '12345678912', '用户123****912', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000011', '12345678986', '用户123****986', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000012', '12345678984', '用户123****984', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000013', '12345678911', '用户123****911', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000014', '12345678942', '用户123****942', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000015', '12345678941', '用户123****941', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000016', '12345678998', '用户123****998', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000017', '12356478421', '用户123****421', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000018', '12434518000', '用户124****000', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000019', '14725836912', '用户147****912', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000020', '78945612321', '用户789****321', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000021', '14789632569', '用户147****569', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000022', '14189132569', '用户141****569', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000023', '11111111111', '用户111****111', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000024', '88888888888', '用户888****888', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000025', '88888888887', '用户888****887', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000026', '87888687888', '用户878****888', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000027', '14725883691', '用户147****691', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000028', '14714714711', '用户147****711', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000029', '14714714712', '用户147****712', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000030', '14714714713', '用户147****713', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000031', '14714714717', '用户147****717', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000032', '14714714514', '用户147****514', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000033', '14714714719', '用户147****719', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000034', '99999999999', '用户999****999', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000035', '14714712345', '用户147****345', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000036', '15815815811', '用户158****811', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000037', '15815815812', '用户158****812', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000038', '15815815813', '用户158****813', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000039', '15815815814', '用户158****814', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000040', '15815815816', '用户158****816', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000041', '15815815817', '用户158****817', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000042', '15767956539', '小孩子', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000043', '15815815866', '用户158****866', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000044', '15815815877', '用户158****877', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000045', 'null', '用户112****211', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000046', '15469874566', '用户154****566', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000047', '11225544667', '用户112****667', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000048', '25814736911', '用户258****911', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000049', '88888555552', '用户888****552', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000050', '33333666661', '用户333****661', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000051', '22222222222', '用户222****222', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000052', '15767976538', '小熊猫', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000053', '15767956534', '用户157****534', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000054', '15767956541', '用户157****541', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000055', '15767956551', '用户157****551', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000056', '15767951228', '用户157****228', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000057', '15767976596', '用户157****596', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000058', '15767976593', '用户157****593', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000059', '15767976594', '用户15', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000060', '15767976592', '用户', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000061', '15767976591', '用户157***', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000062', '12457869639956', '用户12', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000063', '15765966563', '用户157', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000064', '15767976931', '用户157****931', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000065', '15767946563', '用户157****563', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000066', '15767976535', '用户157****535', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000067', '15767956891', '用户157****891', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000068', '123456', '123456', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000069', '15767976597', '用户157****597', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-04 07:36:33'),
('000070', '15767956636', '用户15767956636', 'c3cf5482a1d16021bf316d4441ea8e72', '2016-08-08 13:30:48'),
('000071', '1576796878', '353454343', '441ecebf73c4f37ef5112c4629dd4d7c', '2016-08-09 11:40:02'),
('000072', '1576797879', '3534543', '441ecebf73c4f37ef5112c4629dd4d7c', '2016-08-09 12:40:31'),
('000073', '1576*****779', '354543', '441ecebf73c4f37ef5112c4629dd4d7c', '2016-08-09 12:44:07');

-- --------------------------------------------------------

--
-- 表的结构 `user_behavior`
--

CREATE TABLE `user_behavior` (
  `user_id` varchar(10) NOT NULL,
  `news_id` varchar(20) NOT NULL,
  `news_tag` varchar(20) NOT NULL,
  `behavior_type` int(11) NOT NULL DEFAULT '0',
  `weight` double DEFAULT NULL,
  `is_comment` int(11) NOT NULL DEFAULT '0',
  `address` varchar(100) DEFAULT NULL,
  `news_way` int(11) NOT NULL DEFAULT '0',
  `age` varchar(20) DEFAULT NULL,
  `score` double DEFAULT NULL,
  `times` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user_love_tag`
--

CREATE TABLE `user_love_tag` (
  `user_id` varchar(10) NOT NULL,
  `tags` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user_love_tag`
--

INSERT INTO `user_love_tag` (`user_id`, `tags`) VALUES
('000001', '军事,美文,探索'),
('000002', '游戏,汽车,国际,育儿'),
('000003', '娱乐,探索,美文,故事,旅游,军事,财经'),
('000004', '游戏,娱乐,探索,养生'),
('000005', '时尚,旅游,社会,财经'),
('000006', '时尚,旅游,社会,财经'),
('000007', '时尚,旅游,社会,财经'),
('000008', '美文'),
('000009', '美文'),
('000010', '美文'),
('000011', '美文'),
('000012', '美文'),
('000013', '美文'),
('000014', '美文'),
('000015', '美文'),
('000016', '美文'),
('000017', '美食'),
('000018', '历史'),
('000019', '时尚'),
('000020', '养生'),
('000021', '社会'),
('000022', '社会,养生,历史'),
('000023', '时尚'),
('000024', '汽车'),
('000025', '科技,汽车,美文'),
('000026', '游戏,故事,汽车,娱乐,美食,社会,美文'),
('000027', '美食'),
('000028', '美食'),
('000029', '游戏'),
('000030', '游戏'),
('000031', '历史'),
('000032', '美食'),
('000033', '游戏'),
('000034', '美食,美文'),
('000035', '游戏'),
('000036', '美食'),
('000037', '游戏'),
('000038', '美食'),
('000039', '美食'),
('000040', '美食'),
('000041', '美食'),
('000042', '故事,美食,社会,历史,养生'),
('000043', '时尚,养生'),
('000044', '体育,社会'),
('000045', ''),
('000046', '历史,养生,时尚'),
('000047', '历史,养生,时尚'),
('000048', '历史,养生,时尚'),
('000049', '历史,养生,时尚'),
('000050', '养生,体育,科技'),
('000051', '探索,故事,旅游,军事,科技,财经'),
('000052', '国际,探索,故事,美食,美文,旅游,军事,科技,财经'),
('000053', '探索,故事,美食,美文,旅游,军事,科技,财经'),
('000054', ''),
('000055', '故事,探索,军事,财经,旅游,美文'),
('000056', '科技,财经,娱乐'),
('000057', '探索,美文,故事,美食,旅游,军事'),
('000058', '娱乐,探索,美文,故事,旅游,军事,科技,财经'),
('000059', '娱乐,探索,故事,旅游,军事,科技,财经'),
('000060', '社会,娱乐,探索,美文,故事,旅游,军事,科技,财经'),
('000061', '美文,探索'),
('000062', '美文,故事,旅游,军事,财经'),
('000063', '娱乐,探索,美文,故事,旅游,军事,科技,财经'),
('000064', '娱乐,探索,美文,故事,美食,旅游,军事,财经'),
('000065', '探索,美文,故事,旅游,军事,财经,科技'),
('000066', '娱乐,探索,美文,故事,美食,旅游,军事,科技,财经'),
('000067', '娱乐,国际,社会,财经'),
('000068', 'news_tech'),
('000069', '故事,探索,军事,财经,养生,旅游,美食,时尚,美文'),
('000070', '国际,体育'),
('000071', ''),
('000071', '体育,国际'),
('000072', ''),
('000073', '');

-- --------------------------------------------------------

--
-- 表的结构 `user_mess`
--

CREATE TABLE `user_mess` (
  `user_id` varchar(10) NOT NULL,
  `sex` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  `image` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user_mess`
--

INSERT INTO `user_mess` (`user_id`, `sex`, `age`, `email`, `address`, `image`) VALUES
('000001', NULL, NULL, 'yanshanren2013@163.c', NULL, ''),
('000002', NULL, NULL, NULL, NULL, NULL),
('000003', NULL, NULL, NULL, NULL, NULL),
('000004', NULL, NULL, NULL, NULL, NULL),
('000005', NULL, NULL, NULL, NULL, NULL),
('000006', NULL, NULL, NULL, NULL, NULL),
('000007', NULL, NULL, NULL, NULL, NULL),
('000008', NULL, NULL, NULL, NULL, NULL),
('000009', NULL, NULL, NULL, NULL, NULL),
('000010', NULL, NULL, NULL, NULL, NULL),
('000011', NULL, NULL, NULL, NULL, NULL),
('000012', NULL, NULL, NULL, NULL, NULL),
('000013', NULL, NULL, NULL, NULL, NULL),
('000014', NULL, NULL, NULL, NULL, NULL),
('000015', NULL, NULL, NULL, NULL, NULL),
('000016', NULL, NULL, NULL, NULL, NULL),
('000017', NULL, NULL, NULL, NULL, NULL),
('000018', NULL, NULL, NULL, NULL, NULL),
('000019', NULL, NULL, NULL, NULL, NULL),
('000020', NULL, NULL, NULL, NULL, NULL),
('000021', NULL, NULL, NULL, NULL, NULL),
('000022', NULL, NULL, NULL, NULL, NULL),
('000023', NULL, NULL, NULL, NULL, NULL),
('000024', NULL, NULL, NULL, NULL, NULL),
('000025', NULL, NULL, NULL, NULL, NULL),
('000026', NULL, NULL, NULL, NULL, NULL),
('000027', NULL, NULL, NULL, NULL, NULL),
('000028', NULL, NULL, NULL, NULL, NULL),
('000029', NULL, NULL, NULL, NULL, NULL),
('000030', NULL, NULL, NULL, NULL, NULL),
('000031', NULL, NULL, NULL, NULL, NULL),
('000032', NULL, NULL, NULL, NULL, NULL),
('000033', NULL, NULL, NULL, NULL, NULL),
('000034', NULL, NULL, NULL, NULL, NULL),
('000035', NULL, NULL, NULL, NULL, NULL),
('000036', NULL, NULL, NULL, NULL, NULL),
('000037', NULL, NULL, NULL, NULL, NULL),
('000038', NULL, NULL, NULL, NULL, NULL),
('000039', NULL, NULL, NULL, NULL, NULL),
('000040', NULL, NULL, NULL, NULL, NULL),
('000041', NULL, NULL, NULL, NULL, NULL),
('000042', NULL, NULL, 'null', NULL, ''),
('000043', NULL, NULL, NULL, NULL, NULL),
('000044', NULL, NULL, NULL, NULL, NULL),
('000045', NULL, NULL, NULL, NULL, NULL),
('000046', NULL, NULL, NULL, NULL, NULL),
('000047', NULL, NULL, NULL, NULL, NULL),
('000048', NULL, NULL, NULL, NULL, NULL),
('000049', NULL, NULL, NULL, NULL, NULL),
('000050', NULL, NULL, NULL, NULL, NULL),
('000051', NULL, NULL, NULL, NULL, NULL),
('000052', NULL, NULL, NULL, NULL, ''),
('000053', NULL, NULL, NULL, NULL, NULL),
('000054', NULL, NULL, NULL, NULL, NULL),
('000055', NULL, NULL, NULL, NULL, NULL),
('000056', NULL, NULL, NULL, NULL, NULL),
('000057', NULL, NULL, NULL, NULL, NULL),
('000058', NULL, NULL, NULL, NULL, NULL),
('000059', NULL, NULL, NULL, NULL, ''),
('000060', NULL, NULL, NULL, NULL, ''),
('000061', NULL, NULL, NULL, NULL, ''),
('000062', NULL, NULL, NULL, NULL, ''),
('000063', NULL, NULL, NULL, NULL, ''),
('000064', NULL, NULL, NULL, NULL, ''),
('000065', NULL, NULL, NULL, NULL, NULL),
('000066', NULL, NULL, NULL, NULL, ''),
('000067', NULL, NULL, NULL, NULL, NULL),
('000068', NULL, NULL, NULL, NULL, NULL),
('000069', NULL, NULL, NULL, NULL, NULL),
('000071', NULL, NULL, NULL, NULL, NULL),
('000072', NULL, NULL, NULL, NULL, NULL),
('000073', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `user_operate`
--

CREATE TABLE `user_operate` (
  `user_id` varchar(10) NOT NULL,
  `news_id` varchar(20) NOT NULL,
  `comment` varchar(1000) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_love` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user_tag_deep`
--

CREATE TABLE `user_tag_deep` (
  `user_id` varchar(10) NOT NULL,
  `news_society` double DEFAULT NULL,
  `news_entertainment` double DEFAULT NULL,
  `news_tech` double DEFAULT NULL,
  `news_car` double DEFAULT NULL,
  `news_sports` double DEFAULT NULL,
  `news_finance` double DEFAULT NULL,
  `news_military` double DEFAULT NULL,
  `news_world` double DEFAULT NULL,
  `news_fashion` double DEFAULT NULL,
  `news_travel` double DEFAULT NULL,
  `news_discovery` double DEFAULT NULL,
  `news_baby` double DEFAULT NULL,
  `news_regimen` double DEFAULT NULL,
  `news_story` double DEFAULT NULL,
  `news_essay` double DEFAULT NULL,
  `news_game` double DEFAULT NULL,
  `news_history` double DEFAULT NULL,
  `news_food` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user_tag_score`
--

CREATE TABLE `user_tag_score` (
  `user_id` varchar(10) NOT NULL,
  `news_society` double DEFAULT NULL,
  `news_entertainment` double DEFAULT NULL,
  `news_tech` double DEFAULT NULL,
  `news_car` double DEFAULT NULL,
  `news_sports` double DEFAULT NULL,
  `news_finance` double DEFAULT NULL,
  `news_military` double DEFAULT NULL,
  `news_world` double DEFAULT NULL,
  `news_fashion` double DEFAULT NULL,
  `news_travel` double DEFAULT NULL,
  `news_discovery` double DEFAULT NULL,
  `news_baby` double DEFAULT NULL,
  `news_regimen` double DEFAULT NULL,
  `news_story` double DEFAULT NULL,
  `news_essay` double DEFAULT NULL,
  `news_game` double DEFAULT NULL,
  `news_history` double DEFAULT NULL,
  `news_food` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user_tag_score`
--

INSERT INTO `user_tag_score` (`user_id`, `news_society`, `news_entertainment`, `news_tech`, `news_car`, `news_sports`, `news_finance`, `news_military`, `news_world`, `news_fashion`, `news_travel`, `news_discovery`, `news_baby`, `news_regimen`, `news_story`, `news_essay`, `news_game`, `news_history`, `news_food`) VALUES
('000001', 2.694537046614036, 2.512533923323375, 2.6750895454310064, 2.1522782579492628, 2.799692362566384, 2.250496310034508, 3.108259730537031, 3.3311367459787666, 2.2092105327698275, 2.7812033222513652, 2.2123955479525237, 2.9696680705535488, 2.176075568076781, 2.144448250281169, 2.9159446905096824, 2.0957476792748952, 3.680511261795824, 2.2907711541000144),
('000002', 5.23694051421028, 4.4558833154063775, 8.476075682968919, 13.67755177926377, 3.4937616943340575, 5.838625269616177, 5.673629955818645, 5.122406927701453, 6.310783928477896, 4.258381588785207, 5.841571127377751, 6.43179983772713, 5.874526075937517, 5.791844857872957, 7.22612400088063, 5.360897620264073, 3.753835917929619, 6.17535990542753),
('000003', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000004', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000005', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000006', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000007', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000008', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000009', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000010', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000011', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000012', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000013', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000014', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000015', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000016', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000017', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000018', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000019', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000020', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000021', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000022', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000023', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000024', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000025', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000026', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000027', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000028', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000029', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000030', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000031', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000032', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000033', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000034', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000035', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000036', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000037', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000038', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000039', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000040', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000041', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000042', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1),
('000043', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000044', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000045', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000046', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000047', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000048', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000049', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000050', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1),
('000051', 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1),
('000052', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
('000053', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000054', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000055', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000056', 2, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
('000057', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000058', 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000059', 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1),
('000060', 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
('000061', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000062', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000063', 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
('000064', 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
('000065', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000066', 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1),
('000067', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1),
('000068', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000069', 1.5497209752611714, 4.684211844004147, 9.662894649793694, 3.4335737307436975, 1.362041133395879, 12.971001385730487, 2.0561922416905314, 2.3408948114293455, 1.7496557333844642, 1.5268666010248908, 1.9823199713678405, 1.7530789990901845, 1.881822511462544, 1.7671557992271185, 2.0183009422470386, 5.038980176136956, 5.287616674729766, 1.933671819280247),
('000071', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000072', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000073', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
('000070', NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- 视图结构 `news_hot`
--
DROP TABLE IF EXISTS `news_hot`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `news_hot`  AS  select `a`.`news_id` AS `news_id`,`a`.`time` AS `time`,`a`.`image` AS `image`,`a`.`abstract` AS `abstract`,`a`.`source` AS `source`,`a`.`title` AS `title`,`b`.`tag` AS `tag`,`b`.`love_times` AS `love_times`,`b`.`read_times` AS `read_times`,`b`.`comment_times` AS `comment_times` from (`get_news` `a` join `news_mess` `b`) where (`a`.`news_id` = `b`.`news_id`) ;

-- --------------------------------------------------------

--
-- 视图结构 `news_nums_view`
--
DROP TABLE IF EXISTS `news_nums_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `news_nums_view`  AS  select `get_news`.`tag` AS `tag`,count(`get_news`.`tag`) AS `count` from `get_news` group by `get_news`.`tag` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `get_news`
--
ALTER TABLE `get_news`
  ADD PRIMARY KEY (`news_id`),
  ADD UNIQUE KEY `get_news_title_uindex` (`title`),
  ADD UNIQUE KEY `get_news_news_id_uindex` (`news_id`);

--
-- Indexes for table `news_comment`
--
ALTER TABLE `news_comment`
  ADD KEY `FK_get_news_news_comment` (`news_id`);

--
-- Indexes for table `news_feedback`
--
ALTER TABLE `news_feedback`
  ADD KEY `FK_user_news_feedback` (`user_id`);

--
-- Indexes for table `news_mess`
--
ALTER TABLE `news_mess`
  ADD KEY `FK_get_news_news_mess` (`news_id`);

--
-- Indexes for table `news_recommend`
--
ALTER TABLE `news_recommend`
  ADD KEY `FK_user_news_recomment` (`user_id`);

--
-- Indexes for table `news_tag_deep`
--
ALTER TABLE `news_tag_deep`
  ADD KEY `FK_get_news_news_tag_deep` (`news_id`);

--
-- Indexes for table `n_admin`
--
ALTER TABLE `n_admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `user_behavior`
--
ALTER TABLE `user_behavior`
  ADD KEY `FK_user_user_behavior` (`user_id`),
  ADD KEY `FK_get_news_user_behavior` (`news_id`);

--
-- Indexes for table `user_love_tag`
--
ALTER TABLE `user_love_tag`
  ADD KEY `FK_user_user_love_tag` (`user_id`);

--
-- Indexes for table `user_mess`
--
ALTER TABLE `user_mess`
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user_operate`
--
ALTER TABLE `user_operate`
  ADD KEY `FK_get_news_user_operate` (`news_id`),
  ADD KEY `FK_user_user_operator` (`user_id`);

--
-- Indexes for table `user_tag_deep`
--
ALTER TABLE `user_tag_deep`
  ADD KEY `FK_user_user_tag_deep` (`user_id`);

--
-- Indexes for table `user_tag_score`
--
ALTER TABLE `user_tag_score`
  ADD KEY `FK_user_user_tag_score` (`user_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `n_admin`
--
ALTER TABLE `n_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- 限制导出的表
--

--
-- 限制表 `news_comment`
--
ALTER TABLE `news_comment`
  ADD CONSTRAINT `FK_get_news_news_comment` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`);

--
-- 限制表 `news_feedback`
--
ALTER TABLE `news_feedback`
  ADD CONSTRAINT `FK_user_news_feedback` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `news_mess`
--
ALTER TABLE `news_mess`
  ADD CONSTRAINT `FK_get_news_news_mess` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`);

--
-- 限制表 `news_recommend`
--
ALTER TABLE `news_recommend`
  ADD CONSTRAINT `FK_user_news_recomment` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `news_tag_deep`
--
ALTER TABLE `news_tag_deep`
  ADD CONSTRAINT `FK_get_news_news_tag_deep` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`);

--
-- 限制表 `user_behavior`
--
ALTER TABLE `user_behavior`
  ADD CONSTRAINT `FK_get_news_user_behavior` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`),
  ADD CONSTRAINT `FK_user_user_behavior` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `user_love_tag`
--
ALTER TABLE `user_love_tag`
  ADD CONSTRAINT `FK_user_user_love_tag` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `user_mess`
--
ALTER TABLE `user_mess`
  ADD CONSTRAINT `fk_user_mess` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `user_operate`
--
ALTER TABLE `user_operate`
  ADD CONSTRAINT `FK_get_news_user_operate` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`),
  ADD CONSTRAINT `FK_user_user_operator` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `user_tag_deep`
--
ALTER TABLE `user_tag_deep`
  ADD CONSTRAINT `FK_user_user_tag_deep` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 限制表 `user_tag_score`
--
ALTER TABLE `user_tag_score`
  ADD CONSTRAINT `FK_user_user_tag_score` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
