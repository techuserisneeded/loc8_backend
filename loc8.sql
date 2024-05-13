-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 11, 2024 at 05:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `loc8`
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
('7001a0a3-f2e5-4b7f-9223-0150fdef12ff', 39, 'f92657bc-8f51-47f4-9b48-116af6f2b5ab', 2);

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
  `created_by_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `billboards`
--

INSERT INTO `billboards` (`id`, `video_id`, `visibility_duration`, `distance_to_center`, `central_duration`, `near_p_duration`, `mid_p_duration`, `far_p_duration`, `central_distance`, `near_p_distance`, `mid_p_distance`, `far_p_distance`, `average_areas`, `confidence`, `tracker_id`, `created_at`, `created_by_user_id`) VALUES
('0c597ecf-6e37-445a-be17-ef66ffe1b32e', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 0.533333, 40.9304, 0, 0.1, 0.3, 0.133333, 0, 37.5667, 35.1676, 32.6411, 1.94432, 0.739295, 14, '2024-04-09 16:34:17', 1),
('1d68f8e9-f6b4-4c38-9fb5-d2ffeea24aa7', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 2.4, 40.1955, 0, 0.433333, 1.2, 0.5, 0, 71.4329, 77.2636, 86.201, 3.88608, 0.684429, 1, '2024-04-09 16:34:17', 1),
('2f52bbaf-16b1-4896-9e9d-5ca434127729', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 6.33333, 42.3777, 0, 2.63333, 2.1, 1.43333, 0, 67.603, 76.5585, 86.6283, 2.02649, 0.721102, 5, '2024-04-09 16:34:17', 1),
('4a99c16c-9857-4f88-82d8-9f8973d459e8', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 0.966667, 41.6873, 0, 0.266667, 0.466667, 0.233333, 0, 70.3299, 77.5462, 87.3839, 1.40408, 0.705476, 13, '2024-04-09 16:34:17', 1),
('4cf1e31b-4b3e-42a4-b4e1-4e6e760761b3', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 4.46667, 41.9305, 0, 0, 3.36667, 0.4, 0, 0, 34.4727, 28.3116, 1.26869, 0.72868, 2, '2024-04-09 16:34:17', 1),
('610bd002-53a3-4c6b-b182-25639d7deb7c', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 0.933333, 42.504, 0, 0.366667, 0.333333, 0.233333, 0, 68.5697, 76.9632, 87.4756, 1.31983, 0.764694, 10, '2024-04-09 16:34:17', 1),
('679af46e-ef32-4934-ba07-295f7efe2fae', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 0.766667, 41.9534, 0, 0.1, 0.4, 0.266667, 0, 70.874, 76.4563, 86.3429, 0.943969, 0.743478, 4, '2024-04-09 16:34:17', 1),
('7771a603-7f16-485e-ac20-8da8639943ba', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 6.23333, 44.0014, 0, 0.7, 3.26667, 1.76667, 0, 38.2006, 35.9821, 34.6587, 1.99876, 0.717535, 9, '2024-04-09 16:34:17', 1),
('89346ab7-e885-4efb-8a99-88ba81a05a99', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 1, 42.3359, 0, 0.2, 0.466667, 0.333333, 0, 70.3933, 76.3913, 86.5541, 0.92436, 0.723418, 16, '2024-04-09 16:34:17', 1),
('8f376d3d-e44b-4e35-8797-5a4538890145', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 1, 40.9369, 0, 0.466667, 0.366667, 0.166667, 0, 38.7022, 35.3083, 33.2759, 0.920398, 0.723142, 17, '2024-04-09 16:34:17', 1),
('a96520e8-09a9-429e-b35c-0b99a858ad9d', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 3.9, 42.8312, 0, 0, 0.866667, 3.03333, 0, 0, 31.9581, 30.6685, 2.33467, 0.766603, 6, '2024-04-09 16:34:17', 1),
('aaf8d7e9-5833-4ccb-8d0e-eb1b3d3c4cee', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 1.4, 42.2205, 0, 0.566667, 0.266667, 0.333333, 0, 67.6754, 77.9174, 87.145, 1.48693, 0.682638, 18, '2024-04-09 16:34:17', 1),
('ad5b9617-fb38-4ee6-b822-041a0b2d93cd', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 2.06667, 42.0527, 0, 0, 0, 0.733333, 0, 0, 0, 30.3151, 1.25907, 0.642193, 3, '2024-04-09 16:34:17', 1),
('bf113c58-13a6-4267-b5c5-a2b534a215cc', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 0.966667, 42.7744, 0, 0.266667, 0.4, 0.3, 0, 69.8988, 77.0088, 87.527, 1.08155, 0.763546, 20, '2024-04-09 16:34:17', 1),
('bfe99e47-352f-4d93-98d1-f7ef3c577ddb', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 1.03333, 41.9312, 0, 0.233333, 0.466667, 0.333333, 0, 69.9373, 76.3831, 86.6714, 1.70097, 0.741187, 15, '2024-04-09 16:34:17', 1),
('c5b39eb3-17a6-4e52-91af-960bf208113e', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 1.23333, 41.5504, 0, 0.7, 0.366667, 0.166667, 0, 40.3933, 37.7891, 37.3382, 2.09892, 0.721678, 19, '2024-04-09 16:34:17', 1),
('fc09491e-33f0-4377-a375-432c6c3e990d', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 1.06667, 43.2117, 0, 0.533333, 0.3, 0.166667, 0, 67.6631, 77.8671, 87.406, 1.90239, 0.699582, 8, '2024-04-09 16:34:17', 1),
('fc5e92a5-87f4-4b45-afa9-c4c8a5d87a22', '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 2.23333, 41.2883, 0, 0.1, 0.6, 0.433333, 0, 72.2848, 75.6743, 86.6601, 3.1917, 0.615183, 7, '2024-04-09 16:34:17', 1);

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
('2b4baa8d-4727-4679-a89f-32875e85412a', 'test', 'max life', '2b4baa8d-4727-4679-a89f-32875e85412aMax_Life_Insurance_logo.png', 'middle class', 'insurance', 'media', 0, NULL, NULL, 1, '2024-04-09 17:12:48', 34);

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
  `status` int(2) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plans`
--

INSERT INTO `plans` (`plan_id`, `brief_id`, `budget_id`, `user_id`, `video_id`, `location`, `latitude`, `longitude`, `illumination`, `media_type`, `width`, `height`, `qty`, `size`, `units`, `duration`, `imp_per_month`, `rental_per_month`, `printing_rate`, `mounting_rate`, `cost_for_duration`, `printing_cost`, `mounting_cost`, `total`, `total_area`, `map_image`, `site_image`, `status`) VALUES
('303f37bb-e6bd-471c-8f61-1e1b108f2d48', '2b4baa8d-4727-4679-a89f-32875e85412a', 'f92657bc-8f51-47f4-9b48-116af6f2b5ab', 39, '1d616347-94a1-4ac0-a672-db8f6a8a49d1', 'SH82, Panvel, Raigad, Maharashtra, 410222, India', 18.915218, 73.152751, 'Front Lit', 'Billboard', 500, 500, 5, 800, 52.000, 25.00, 21.00, 56000.00, 8.00, 5.00, 46666.67, 6400.00, 4000.00, 57066.67, 9999999.999, 'd9494d32-93af-4fe9-a1c7-c17f1edfa8a9map.png', 'ae37dd02-2583-476a-a4cb-3739c02e4337renault_images.jpeg', 1);

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
  `video_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `videofiles`
--

INSERT INTO `videofiles` (`video_id`, `filename`, `zone_id`, `state_id`, `city_id`, `created_at`, `created_by_user_id`, `video_path`) VALUES
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', '99352fca-85f6-422c-b539-bddfbccd5601.mp4', 3, 11, 8, '2024-04-09 16:34:17', 1, './instance/99352fca-85f6-422c-b539-bddfbccd5601.mp4');

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
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', 2, 80, 18.929500, 73.162400),
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', 3, 73, 18.927900, 73.164000),
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', 4, 76, 18.926600, 73.165100),
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', 5, 80, 18.925000, 73.166400),
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', 6, 75, 18.923600, 73.167900),
('1d616347-94a1-4ac0-a672-db8f6a8a49d1', 7, 54, 18.921400, 73.170400);

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
  ADD KEY `video_id` (`video_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

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
