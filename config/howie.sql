-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2016-05-30 16:05:13
-- 服务器版本： 10.1.13-MariaDB
-- PHP Version: 5.6.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `news`
--

-- --------------------------------------------------------

--
-- 表的结构 `get_news`
--

CREATE TABLE `get_news` (
  `news_id` varchar(20) NOT NULL,
  `news_link` varchar(100) DEFAULT NULL,
  `source` varchar(20) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(50) NOT NULL,
  `abstract` varchar(500) NOT NULL,
  `tag` varchar(20) NOT NULL,
  `text_content` mediumtext NOT NULL,
  `html_content` mediumtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
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
-- 表的结构 `news_recommend`
--

CREATE TABLE `news_recommend` (
  `user_id` varchar(10) NOT NULL,
  `news_score` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
(1, 'admin', 'b49515ad6e147d962c8696f31694ad8d');

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
('000002', '15767956890', '用户15767956890', '441ecebf73c4f37ef5112c4629dd4d7c', '2016-05-29 06:28:55');

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
  `score` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
('000002', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `user_operate`
--

CREATE TABLE `user_operate` (
  `user_id` varchar(10) NOT NULL,
  `news_id` varchar(20) NOT NULL,
  `comment` varchar(1000) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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

--
-- 转存表中的数据 `user_tag_deep`
--

INSERT INTO `user_tag_deep` (`user_id`, `news_society`, `news_entertainment`, `news_tech`, `news_car`, `news_sports`, `news_finance`, `news_military`, `news_world`, `news_fashion`, `news_travel`, `news_discovery`, `news_baby`, `news_regimen`, `news_story`, `news_essay`, `news_game`, `news_history`, `news_food`) VALUES
('000002', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

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
-- Indexes for dumped tables
--

--
-- Indexes for table `get_news`
--
ALTER TABLE `get_news`
  ADD PRIMARY KEY (`news_id`);

--
-- Indexes for table `news_comment`
--
ALTER TABLE `news_comment`
  ADD KEY `FK_get_news_news_comment` (`news_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- 限制导出的表
--

--
-- 限制表 `news_comment`
--
ALTER TABLE `news_comment`
  ADD CONSTRAINT `FK_get_news_news_comment` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`);

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
