-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 30, 2024 at 07:35 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `loc8_ml`
--

-- --------------------------------------------------------

--
-- Table structure for table `assigned_budgets`
--

CREATE TABLE `assigned_budgets` (
  `id` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `budget_id` varchar(100) NOT NULL,
  `status` int(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assigned_budgets`
--

INSERT INTO `assigned_budgets` (`id`, `user_id`, `budget_id`, `status`) VALUES
('7001a0a3-f2e5-4b7f-9223-0150fdef12ff', 39, 'f92657bc-8f51-47f4-9b48-116af6f2b5ab', 0);

-- --------------------------------------------------------

--
-- Table structure for table `billboards`
--

CREATE TABLE `billboards` (
  `id` varchar(36) NOT NULL,
  `video_id` varchar(36) DEFAULT NULL,
  `visibility_duration` float DEFAULT NULL,
  `distance_to_center` float DEFAULT NULL,
  `central_duration` float DEFAULT NULL,
  `near_p_duration` float DEFAULT NULL,
  `mid_p_duration` float DEFAULT NULL,
  `far_p_duration` float DEFAULT NULL,
  `central_distance` float DEFAULT NULL,
  `near_p_distance` float DEFAULT NULL,
  `mid_p_distance` float DEFAULT NULL,
  `far_p_distance` float DEFAULT NULL,
  `average_areas` float DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `tracker_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by_user_id` int(11) NOT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `vendor_name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `traffic_direction` varchar(255) DEFAULT NULL,
  `media_type` varchar(255) DEFAULT NULL,
  `illumination` varchar(255) DEFAULT NULL,
  `width` float DEFAULT 0,
  `height` float DEFAULT 0,
  `quantity` float DEFAULT 0,
  `area` float DEFAULT 0,
  `display_cost_per_month` float DEFAULT 0,
  `printing_rate` float DEFAULT 0,
  `mounting_rate` float DEFAULT 0,
  `printing_cost` float DEFAULT 0,
  `mounting_cost` float DEFAULT 0,
  `total_cost` float DEFAULT 0,
  `site_image` varchar(255) DEFAULT NULL,
  `map_image` varchar(255) DEFAULT NULL,
  `focal_vision_duration` float DEFAULT 0,
  `saliency_score_front_city` float DEFAULT NULL,
  `saliency_score_rear_city` float DEFAULT 0,
  `net_saliency_score_city` float DEFAULT 0,
  `duration` int(11) DEFAULT 0,
  `rental_per_month` float DEFAULT 0,
  `cost_for_duration` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `billboards`
--

INSERT INTO `billboards` (`id`, `video_id`, `visibility_duration`, `distance_to_center`, `central_duration`, `near_p_duration`, `mid_p_duration`, `far_p_duration`, `central_distance`, `near_p_distance`, `mid_p_distance`, `far_p_distance`, `average_areas`, `confidence`, `tracker_id`, `created_at`, `created_by_user_id`, `latitude`, `longitude`, `vendor_name`, `location`, `traffic_direction`, `media_type`, `illumination`, `width`, `height`, `quantity`, `area`, `display_cost_per_month`, `printing_rate`, `mounting_rate`, `printing_cost`, `mounting_cost`, `total_cost`, `site_image`, `map_image`, `focal_vision_duration`, `saliency_score_front_city`, `saliency_score_rear_city`, `net_saliency_score_city`, `duration`, `rental_per_month`, `cost_for_duration`) VALUES
('22a83f6b-48fd-404f-baa7-f2a54189bb9b', 'a48252b1-5961-42f8-a887-f358df838e62', 2.38, 42.7, 0.62, 0.93, 0.48, 0.34, 60.19, 66.38, 76.84, 87.03, 0.61, 0.76, 7, '2024-06-08 06:10:08', 1, 18.900602, 73.201966, 'max', 'Vishwadeep Housing Society, Rasayani, Khalapur Taluka, Raigad District, Maharashtra, 410222, India', 'right', 'media', 'backlit', 500, 500, 5, 1250000, 0, 8, 8, 10000000, 10000000, 20000000, NULL, NULL, 0, 26.986, 27.0165, 26.9921, 50, 65000, 108333),
('2af06afe-153e-4eb0-b7da-8230890b895e', 'a48252b1-5961-42f8-a887-f358df838e62', 1.76, 43.53, 0.21, 0.79, 0.41, 0.31, 61.48, 66.86, 77.64, 88.68, 1.45, 0.64, 12, '2024-06-08 06:10:09', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 26.7997, 26.8722, 26.8142, 0, 0, 0),
('35afb8f9-5026-4467-a29d-08b0831f6307', 'a48252b1-5961-42f8-a887-f358df838e62', 0.31, 31.18, 0, 0, 0.31, 0, 0, 0, 77.29, 0, 0.31, 0.56, 10, '2024-06-08 06:10:09', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 31.4017, 31.4172, 31.4048, 0, 0, 0),
('530b715d-1472-4b87-bdbc-037b0ccb650c', 'a48252b1-5961-42f8-a887-f358df838e62', 8.17, 43.95, 0, 3.1, 2.69, 2, 0, 39, 35.88, 34.37, 1.64, 0.7, 35, '2024-06-08 06:10:09', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 27.2059, 27.2879, 27.2223, 0, 0, 0),
('59f557a9-968f-494b-9992-f8333242e315', 'a48252b1-5961-42f8-a887-f358df838e62', 0.24, 41.36, 0, 0, 0.1, 0.14, 0, 0, 32.58, 30.77, 1.02, 0.69, 14, '2024-06-08 06:10:09', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 27.4629, 27.5139, 27.4731, 0, 0, 0),
('773f4cf1-be31-4350-b349-1dafba896dfd', 'a48252b1-5961-42f8-a887-f358df838e62', 1.55, 42.5, 0, 0.72, 0.48, 0.31, 0, 67.35, 76.91, 87.04, 0.58, 0.75, 9, '2024-06-08 06:10:09', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 27.0362, 27.0652, 27.042, 0, 0, 0),
('af801ffe-1b06-4b97-8742-b1430d690c18', 'a48252b1-5961-42f8-a887-f358df838e62', 0.59, 35.45, 0, 0.1, 0.38, 0.07, 0, 71.7, 77.62, 83.94, 0.37, 0.54, 8, '2024-06-08 06:10:08', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 29.7263, 29.7448, 29.73, 0, 0, 0),
('c4a40bb5-95b0-4110-9d00-b3e1981b741d', 'a48252b1-5961-42f8-a887-f358df838e62', 13.48, 46.76, 7.17, 2.76, 1.9, 1.38, 57.21, 70.15, 81.51, 92.43, 2.34, 0.69, 6, '2024-06-08 06:10:08', 1, 18.899417, 73.203320, 'Max', 'Mumbai - Pune Expressway, Rasayani, Khalapur Taluka, Raigad District, Maharashtra, 410222, India', 'straight', 'billboard', 'front lit', 200, 200, 15, 600000, 0, 8, 8, 4800000, 4800000, 9600000, NULL, NULL, 0, 26.0819, 26.1989, 26.1053, 20, 50000, 33333.3),
('d24367f3-a8a1-4e84-ab23-dbcf237ac058', 'a48252b1-5961-42f8-a887-f358df838e62', 3.24, 19.75, 2.1, 0, 0, 0, 51.02, 0, 0, 0, 9.82, 0.54, 11, '2024-06-08 06:10:09', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, 0, 37.8498, 38.3408, 37.948, 0, 0, 0);

--
-- Triggers `billboards`
--
DELIMITER $$
CREATE TRIGGER `calculate_area_before_insert` BEFORE INSERT ON `billboards` FOR EACH ROW BEGIN
    SET NEW.area = NEW.width * NEW.height * NEW.quantity;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `calculate_area_before_update` BEFORE UPDATE ON `billboards` FOR EACH ROW BEGIN
    SET NEW.area = NEW.width * NEW.height * NEW.quantity;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `calculate_total_cost_before_insert` BEFORE INSERT ON `billboards` FOR EACH ROW BEGIN
    SET NEW.printing_cost = NEW.area * NEW.printing_rate;
    SET NEW.mounting_cost = NEW.area * NEW.mounting_rate;
    SET NEW.total_cost = NEW.display_cost_per_month + NEW.printing_cost + NEW.mounting_cost;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `calculate_total_cost_before_update` BEFORE UPDATE ON `billboards` FOR EACH ROW BEGIN
    SET NEW.printing_cost = NEW.area * NEW.printing_rate;
    SET NEW.mounting_cost = NEW.area * NEW.mounting_rate;
    SET NEW.total_cost = NEW.display_cost_per_month + NEW.printing_cost + NEW.mounting_cost;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `briefs`
--

CREATE TABLE `briefs` (
  `brief_id` varchar(100) NOT NULL,
  `category` varchar(200) NOT NULL,
  `brand_name` varchar(200) NOT NULL,
  `brand_logo` varchar(300) NOT NULL,
  `target_audience` varchar(150) NOT NULL,
  `campaign_obj` varchar(200) NOT NULL,
  `media_approach` varchar(200) NOT NULL,
  `is_immediate_camp` tinyint(1) NOT NULL DEFAULT 0,
  `start_date` date DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `status` int(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `briefs`
--

INSERT INTO `briefs` (`brief_id`, `category`, `brand_name`, `brand_logo`, `target_audience`, `campaign_obj`, `media_approach`, `is_immediate_camp`, `start_date`, `notes`, `status`, `created_at`, `created_by_user_id`) VALUES
('2b4baa8d-4727-4679-a89f-32875e85412a', 'test', 'max life', '2b4baa8d-4727-4679-a89f-32875e85412aMax_Life_Insurance_logo.png', 'middle class', 'insurance', 'media', 0, NULL, NULL, 0, '2024-04-09 17:12:48', 34);

-- --------------------------------------------------------

--
-- Table structure for table `brief_budgets`
--

CREATE TABLE `brief_budgets` (
  `budget_id` varchar(100) NOT NULL,
  `brief_id` varchar(100) NOT NULL,
  `zone_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `budget` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `brief_budgets`
--

INSERT INTO `brief_budgets` (`budget_id`, `brief_id`, `zone_id`, `state_id`, `city_id`, `budget`) VALUES
('f92657bc-8f51-47f4-9b48-116af6f2b5ab', '2b4baa8d-4727-4679-a89f-32875e85412a', 3, 11, 8, 200000);

-- --------------------------------------------------------

--
-- Table structure for table `cities`
--

CREATE TABLE `cities` (
  `city_id` int(11) NOT NULL,
  `city_name` varchar(50) NOT NULL,
  `state_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cities`
--

INSERT INTO `cities` (`city_id`, `city_name`, `state_id`) VALUES
(6, 'new york city', 9),
(7, 'south city', 10),
(8, 'mumbai', 11);

-- --------------------------------------------------------

--
-- Table structure for table `plans`
--

CREATE TABLE `plans` (
  `plan_id` varchar(40) NOT NULL,
  `brief_id` varchar(40) NOT NULL,
  `budget_id` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  `video_id` varchar(40) NOT NULL,
  `location` varchar(100) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `illumination` varchar(200) NOT NULL,
  `media_type` varchar(150) NOT NULL,
  `width` float NOT NULL,
  `height` float NOT NULL,
  `qty` int(5) NOT NULL,
  `size` float NOT NULL,
  `units` decimal(8,3) NOT NULL,
  `duration` decimal(5,2) NOT NULL,
  `imp_per_month` decimal(5,2) NOT NULL,
  `rental_per_month` decimal(10,2) NOT NULL,
  `printing_rate` decimal(4,2) NOT NULL,
  `mounting_rate` decimal(4,2) NOT NULL,
  `cost_for_duration` decimal(10,2) NOT NULL,
  `printing_cost` decimal(10,2) NOT NULL,
  `mounting_cost` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `total_area` decimal(10,3) NOT NULL,
  `map_image` varchar(250) NOT NULL,
  `site_image` varchar(250) NOT NULL,
  `status` int(2) NOT NULL DEFAULT 1,
  `billboard_id` varchar(36) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'planner'),
(2, 'admin'),
(3, 'controller'),
(4, 'superadmin');

-- --------------------------------------------------------

--
-- Table structure for table `states`
--

CREATE TABLE `states` (
  `state_id` int(11) NOT NULL,
  `state_name` varchar(50) NOT NULL,
  `zone_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `states`
--

INSERT INTO `states` (`state_id`, `state_name`, `zone_id`) VALUES
(9, 'new york state', 5),
(10, 'south state', 2),
(11, 'maharashtra', 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `employee_id` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_by_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `role_id`, `first_name`, `last_name`, `employee_id`, `created_at`, `updated_at`, `created_by_user_id`) VALUES
(1, 'john@mail.com', '$2b$12$LGEvisGVlhfcCOF0R3KGD.EJNP4TZOyCv89zgHkbrC3Ucb5aO6x76', 4, 'John', 'Doe', '12345', '2024-03-06 18:00:33', '2024-03-20 15:38:18', 0),
(33, 'test@mail.com', '$2b$12$O7CNwBTngCzvIlPr430J6uilaOC6tKDG93C6.30DEFXMbaKNafQu6', 2, 'rem1', 'rem1', '123454', '2024-03-31 15:39:19', '2024-03-31 18:49:00', 1),
(34, 'controller1@mail.com', '$2b$12$5494Y9kAG2QnuomroKX1UeUvTk6Buy0SaUpiSLD5AXjz86FatsI2i', 3, 'test', 'controller', '7895', '2024-04-01 16:25:17', '2024-04-06 14:02:47', 1),
(36, 'test@email.com', '$2b$12$47bl28GpPwOwnIMz4JFDRe4C5dJwP7tKbC4eLatWcbveLNxWVMNOu', 2, 'test', 'test', 'emp_4', '2024-04-01 16:48:01', '2024-04-01 16:48:29', 1),
(39, 'planner1@mail.com', '$2b$12$CliLWWqa/NLjbMMV7oGJ8eZGAhnNFo2WHh.YC05mJuVeGHSvJDqsW', 1, 'planner', '1', 'planner_emp_1', '2024-04-02 18:47:29', '2024-04-03 01:20:11', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_areas`
--

CREATE TABLE `user_areas` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `zone_id` int(11) DEFAULT NULL,
  `state_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_areas`
--

INSERT INTO `user_areas` (`id`, `user_id`, `zone_id`, `state_id`, `city_id`) VALUES
(1, 33, 2, NULL, NULL),
(2, 36, 1, NULL, NULL),
(5, 34, 5, 9, 6),
(6, 34, 2, 10, 7),
(10, 39, 3, 11, 8);

-- --------------------------------------------------------

--
-- Table structure for table `videofiles`
--

CREATE TABLE `videofiles` (
  `video_id` varchar(36) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `zone_id` int(11) DEFAULT NULL,
  `state_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by_user_id` int(11) DEFAULT NULL,
  `video_path` varchar(500) NOT NULL,
  `average_speed` float DEFAULT 0,
  `length_of_stretch` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `videofiles`
--

INSERT INTO `videofiles` (`video_id`, `filename`, `zone_id`, `state_id`, `city_id`, `created_at`, `created_by_user_id`, `video_path`, `average_speed`, `length_of_stretch`) VALUES
('a48252b1-5961-42f8-a887-f358df838e62', 'H1755_1708086315_6815e6.mp4', 3, 11, 8, '2024-06-08 06:10:08', 1, 'C:\\Users\\sande\\OneDrive\\Desktop\\study-material\\upload\\loc8_backend\\instance\\H1755_1708086315_6815e6.mp4', 74.57, 1178.97);

-- --------------------------------------------------------

--
-- Table structure for table `video_coordinates`
--

CREATE TABLE `video_coordinates` (
  `video_id` varchar(40) NOT NULL,
  `id` int(11) NOT NULL,
  `speed` int(11) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video_coordinates`
--

INSERT INTO `video_coordinates` (`video_id`, `id`, `speed`, `latitude`, `longitude`) VALUES
('a48252b1-5961-42f8-a887-f358df838e62', 52, 92, 18.901300, 73.200000),
('a48252b1-5961-42f8-a887-f358df838e62', 53, 63, 18.900300, 73.201500),
('a48252b1-5961-42f8-a887-f358df838e62', 54, 66, 18.899100, 73.202500),
('a48252b1-5961-42f8-a887-f358df838e62', 55, 73, 18.897500, 73.203200),
('a48252b1-5961-42f8-a887-f358df838e62', 56, 74, 18.895900, 73.203800),
('a48252b1-5961-42f8-a887-f358df838e62', 57, 75, 18.894100, 73.204500),
('a48252b1-5961-42f8-a887-f358df838e62', 58, 79, 18.892300, 73.205400);

-- --------------------------------------------------------

--
-- Table structure for table `zones`
--

CREATE TABLE `zones` (
  `zone_id` int(11) NOT NULL,
  `zone_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `zones`
--

INSERT INTO `zones` (`zone_id`, `zone_name`) VALUES
(1, 'North'),
(2, 'South'),
(3, 'West'),
(4, 'East'),
(5, 'North East');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assigned_budgets`
--
ALTER TABLE `assigned_budgets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `budget_id` (`budget_id`);

--
-- Indexes for table `billboards`
--
ALTER TABLE `billboards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `video_id` (`video_id`),
  ADD KEY `fk_created_by_user_bill` (`created_by_user_id`);

--
-- Indexes for table `briefs`
--
ALTER TABLE `briefs`
  ADD PRIMARY KEY (`brief_id`),
  ADD KEY `created_by_user_id` (`created_by_user_id`);

--
-- Indexes for table `brief_budgets`
--
ALTER TABLE `brief_budgets`
  ADD PRIMARY KEY (`budget_id`),
  ADD KEY `brief_id` (`brief_id`),
  ADD KEY `city_id` (`city_id`),
  ADD KEY `state_id` (`state_id`),
  ADD KEY `zone_id` (`zone_id`);

--
-- Indexes for table `cities`
--
ALTER TABLE `cities`
  ADD PRIMARY KEY (`city_id`),
  ADD UNIQUE KEY `city_name` (`city_name`),
  ADD KEY `state_id` (`state_id`);

--
-- Indexes for table `plans`
--
ALTER TABLE `plans`
  ADD PRIMARY KEY (`plan_id`),
  ADD KEY `brief_id` (`brief_id`),
  ADD KEY `budget_id` (`budget_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `video_id` (`video_id`),
  ADD KEY `fk_plans_billboards` (`billboard_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `states`
--
ALTER TABLE `states`
  ADD PRIMARY KEY (`state_id`),
  ADD UNIQUE KEY `state_name` (`state_name`),
  ADD KEY `zone_id` (`zone_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`,`employee_id`),
  ADD UNIQUE KEY `unique_email` (`email`),
  ADD UNIQUE KEY `unique_epmloyee_id` (`employee_id`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `user_areas`
--
ALTER TABLE `user_areas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `zone_id` (`zone_id`),
  ADD KEY `state_id` (`state_id`),
  ADD KEY `city_id` (`city_id`);

--
-- Indexes for table `videofiles`
--
ALTER TABLE `videofiles`
  ADD PRIMARY KEY (`video_id`),
  ADD UNIQUE KEY `video_path` (`video_path`),
  ADD KEY `zone_id` (`zone_id`),
  ADD KEY `state_id` (`state_id`),
  ADD KEY `city_id` (`city_id`),
  ADD KEY `created_by_user_id` (`created_by_user_id`);

--
-- Indexes for table `video_coordinates`
--
ALTER TABLE `video_coordinates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `video_id` (`video_id`);

--
-- Indexes for table `zones`
--
ALTER TABLE `zones`
  ADD PRIMARY KEY (`zone_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cities`
--
ALTER TABLE `cities`
  MODIFY `city_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `states`
--
ALTER TABLE `states`
  MODIFY `state_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `user_areas`
--
ALTER TABLE `user_areas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `video_coordinates`
--
ALTER TABLE `video_coordinates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT for table `zones`
--
ALTER TABLE `zones`
  MODIFY `zone_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `assigned_budgets`
--
ALTER TABLE `assigned_budgets`
  ADD CONSTRAINT `assigned_budgets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `assigned_budgets_ibfk_2` FOREIGN KEY (`budget_id`) REFERENCES `brief_budgets` (`budget_id`);

--
-- Constraints for table `billboards`
--
ALTER TABLE `billboards`
  ADD CONSTRAINT `billboards_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `videofiles` (`video_id`),
  ADD CONSTRAINT `fk_created_by_user_bill` FOREIGN KEY (`created_by_user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `briefs`
--
ALTER TABLE `briefs`
  ADD CONSTRAINT `briefs_ibfk_1` FOREIGN KEY (`created_by_user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `brief_budgets`
--
ALTER TABLE `brief_budgets`
  ADD CONSTRAINT `brief_budgets_ibfk_1` FOREIGN KEY (`brief_id`) REFERENCES `briefs` (`brief_id`),
  ADD CONSTRAINT `brief_budgets_ibfk_2` FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`),
  ADD CONSTRAINT `brief_budgets_ibfk_3` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`),
  ADD CONSTRAINT `brief_budgets_ibfk_4` FOREIGN KEY (`zone_id`) REFERENCES `zones` (`zone_id`);

--
-- Constraints for table `cities`
--
ALTER TABLE `cities`
  ADD CONSTRAINT `cities_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`);

--
-- Constraints for table `plans`
--
ALTER TABLE `plans`
  ADD CONSTRAINT `fk_plans_billboards` FOREIGN KEY (`billboard_id`) REFERENCES `billboards` (`id`),
  ADD CONSTRAINT `plans_ibfk_1` FOREIGN KEY (`brief_id`) REFERENCES `briefs` (`brief_id`),
  ADD CONSTRAINT `plans_ibfk_2` FOREIGN KEY (`budget_id`) REFERENCES `brief_budgets` (`budget_id`),
  ADD CONSTRAINT `plans_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `plans_ibfk_4` FOREIGN KEY (`video_id`) REFERENCES `videofiles` (`video_id`);

--
-- Constraints for table `states`
--
ALTER TABLE `states`
  ADD CONSTRAINT `states_ibfk_1` FOREIGN KEY (`zone_id`) REFERENCES `zones` (`zone_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

--
-- Constraints for table `user_areas`
--
ALTER TABLE `user_areas`
  ADD CONSTRAINT `user_areas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_areas_ibfk_2` FOREIGN KEY (`zone_id`) REFERENCES `zones` (`zone_id`),
  ADD CONSTRAINT `user_areas_ibfk_3` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`),
  ADD CONSTRAINT `user_areas_ibfk_4` FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`);

--
-- Constraints for table `videofiles`
--
ALTER TABLE `videofiles`
  ADD CONSTRAINT `videofiles_ibfk_1` FOREIGN KEY (`zone_id`) REFERENCES `zones` (`zone_id`),
  ADD CONSTRAINT `videofiles_ibfk_2` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`),
  ADD CONSTRAINT `videofiles_ibfk_3` FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`),
  ADD CONSTRAINT `videofiles_ibfk_4` FOREIGN KEY (`created_by_user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `video_coordinates`
--
ALTER TABLE `video_coordinates`
  ADD CONSTRAINT `video_coordinates_ibfk_1` FOREIGN KEY (`video_id`) REFERENCES `videofiles` (`video_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
