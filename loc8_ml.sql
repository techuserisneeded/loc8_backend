-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 06, 2024 at 08:32 PM
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
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `area` int(11) DEFAULT NULL,
  `display_cost_per_month` int(11) DEFAULT NULL,
  `printing_rate` int(11) DEFAULT NULL,
  `mounting_rate` int(11) DEFAULT NULL,
  `printing_cost` int(11) DEFAULT NULL,
  `mounting_cost` int(11) DEFAULT NULL,
  `total_cost` int(11) DEFAULT NULL,
  `site_image` varchar(255) DEFAULT NULL,
  `map_image` varchar(255) DEFAULT NULL,
  `focal_vision_duration` int(11) DEFAULT NULL,
  `saliency_score_front` int(11) DEFAULT NULL,
  `saliency_score_rear` int(11) DEFAULT NULL,
  `net_saliency_score` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT 0,
  `rental_per_month` float DEFAULT 0,
  `cost_for_duration` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `billboards`
--

INSERT INTO `billboards` (`id`, `video_id`, `visibility_duration`, `distance_to_center`, `central_duration`, `near_p_duration`, `mid_p_duration`, `far_p_duration`, `central_distance`, `near_p_distance`, `mid_p_distance`, `far_p_distance`, `average_areas`, `confidence`, `tracker_id`, `created_at`, `created_by_user_id`, `latitude`, `longitude`, `vendor_name`, `location`, `traffic_direction`, `media_type`, `illumination`, `width`, `height`, `quantity`, `area`, `display_cost_per_month`, `printing_rate`, `mounting_rate`, `printing_cost`, `mounting_cost`, `total_cost`, `site_image`, `map_image`, `focal_vision_duration`, `saliency_score_front`, `saliency_score_rear`, `net_saliency_score`, `duration`, `rental_per_month`, `cost_for_duration`) VALUES
('017cdfbf-ef27-4886-bb6d-93d52ed50574', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.8, 0.68, 0.73, 0, 0, 0, 49.81, 0, 0, 0, 150.76, 0.57, 80, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('02038b22-7540-4ca8-8d95-48da6d719b8d', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 4.93, 43.08, 0, 0, 2.24, 1.83, 0, 0, 34.41, 32.19, 1.91, 0.61, 12, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('071f727a-0b47-4434-a1fb-f8041c9f88de', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.3, 42.77, 0, 0.6, 0.4, 0.3, 0, 67.53, 77.01, 87.53, 0.96, 0.72, 77, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('13080404-bd2a-4b9b-9807-f3762f83e98a', '612177b8-530a-4e86-b2cf-514cbdb6586d', 2.57, 42.48, 0, 0, 0.83, 0.97, 0, 0, 76.67, 87.26, 3.78, 0.56, 53, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('170727cc-45d3-48d6-9f2b-043e93e39447', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 3.76, 42.68, 0, 0, 2.07, 1.66, 0, 0, 33.97, 31.76, 1.21, 0.72, 1, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('1766ffe9-6d6d-447d-80a6-c7bfcf8e2905', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.07, 42.5, 0, 0.5, 0.33, 0.23, 0, 67.5, 76.96, 87.48, 1.25, 0.75, 56, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('1767155a-50a7-4337-8223-9940fa33a7fa', '612177b8-530a-4e86-b2cf-514cbdb6586d', 2.5, 40.92, 0, 0.43, 1.27, 0.8, 0, 71.43, 77.51, 86.95, 4.02, 0.66, 42, '2024-05-26 16:35:59', 1, 18.928696, 73.164801, 'name', 'Panvel Taluka, Raigad District, Maharashtra, 410222, India', 'test', 'Billboard', 'Front Lit', 100, 100, 1, 10000, NULL, 8, 8, 80000, 80000, NULL, '029fc0a5-6d15-4136-be51-dd5d2137d97arenault_billboard_images.jpg', '37eee43d-055a-4a34-b945-91d037598408map.png', NULL, NULL, NULL, NULL, 20, 50000, 33333.3),
('19269f35-1e6f-4988-859f-88d9b67e398d', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.87, 42.73, 0, 0, 0, 0.87, 0, 0, 0, 29.97, 0.78, 0.6, 45, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('19bab475-aaf0-4b24-8b2b-cd34055ed9b0', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.07, 31.04, 0, 0, 0.07, 0, 0, 0, 30.93, 0, 1.36, 0.52, 50, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('1d5614c4-64cb-4f38-bb76-d7ee301335f9', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.4, 42.22, 0, 0.6, 0.4, 0.33, 0, 67.88, 76.8, 87.14, 1.43, 0.66, 75, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('2c245e23-9546-4ef8-b853-1a1be55eccf8', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 7.28, 44.66, 3.14, 2.38, 1.07, 0.62, 60.77, 68.6, 80.54, 90.5, 2.42, 0.7, 18, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('2e151953-7db0-4bb4-85f5-8534abe4b24d', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 0.41, 42.68, 0, 0, 0.14, 0.28, 0, 0, 79.22, 86.33, 0.34, 0.62, 21, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('2e47e8e5-7dc2-41bd-98a2-1cc84bfd38c3', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.79, 42.61, 0.38, 0.76, 0.38, 0.28, 60.64, 66.38, 76.75, 87.09, 0.62, 0.73, 4, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('38bc2fc3-a522-4b85-be53-d62ebe26f6e9', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 2.21, 42.5, 0, 1.48, 0.48, 0.21, 0, 41.33, 37.67, 37.17, 1.32, 0.68, 38, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('3d4d1b99-00dd-40b6-8504-d32bace442a1', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 5.62, 41.6, 0, 1.41, 2, 1.34, 0, 38.34, 35.64, 33.1, 1.27, 0.66, 35, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('3e0a1e9b-ee50-4072-b0dd-c85d4c2c8f3a', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.1, 35.73, 0, 0, 0.03, 0.07, 0, 0, 24.7, 22.61, 2.61, 0.62, 82, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('41950f33-a73a-4490-aa07-10c463a9759b', 'fc3b9d48-2862-4ff0-92e3-f8bda5b6a3d6', 1.03, 12.75, 0.33, 0.7, 0, 0, 59.96, 61.13, 0, 0, 1.09, 0.68, 5, '2024-06-06 17:35:38', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('4ef01c32-2958-4dad-9b9e-76395d59eecd', '25de3614-826a-41c6-965f-8ad01ec7f00d', 4.37, 42.26, 0, 1.83, 1.57, 0.97, 0, 66.92, 75.98, 87.01, 2.46, 0.7, 7, '2024-06-06 17:09:43', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('59b04422-6004-46bd-9e86-992f16cdd3e0', 'fc3b9d48-2862-4ff0-92e3-f8bda5b6a3d6', 4.37, 42.26, 0, 1.83, 1.57, 0.97, 0, 66.92, 75.98, 87.01, 2.46, 0.7, 2, '2024-06-06 17:35:38', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('5a7b5ab7-4172-48aa-8c6c-c9e32a22480d', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.17, 40.94, 0, 0.63, 0.37, 0.17, 0, 39.12, 35.31, 33.28, 0.83, 0.71, 74, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('5e36c8cd-3781-4fcf-a54c-cb4caba313b2', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.28, 42.31, 0, 0.69, 0.34, 0.21, 0, 66.3, 76.69, 87.58, 0.51, 0.66, 6, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('61535828-cb70-4d79-9d31-d5f6c9c4a111', '612177b8-530a-4e86-b2cf-514cbdb6586d', 6.53, 44, 0, 1.17, 3.5, 1.83, 0, 38.29, 36, 34.65, 1.92, 0.7, 55, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('6212b2df-d4fc-4da0-9726-79bc2e3014ef', '612177b8-530a-4e86-b2cf-514cbdb6586d', 2, 41.55, 0, 1.47, 0.37, 0.17, 0, 41.45, 37.79, 37.34, 1.45, 0.67, 76, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('66bf9a12-750b-4a56-8962-6be2c963041e', 'fc3b9d48-2862-4ff0-92e3-f8bda5b6a3d6', 2.03, 42.59, 0, 0, 0.97, 1.07, 0, 0, 77.99, 86.99, 3.04, 0.67, 1, '2024-06-06 17:35:38', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('6e3ddba8-2aa2-4153-8c0c-7a3baafb262b', '612177b8-530a-4e86-b2cf-514cbdb6586d', 8.27, 42.92, 0, 0, 4.73, 3.07, 0, 0, 33.87, 30.67, 1.81, 0.74, 46, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('725ecfac-d4c4-4bd8-932a-7a199e7ff39d', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 0.76, 18.98, 0, 0.14, 0, 0, 0, 39.4, 0, 0, 0.64, 0.54, 30, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('74ccc3c1-3a00-4e63-b825-b15e09e45240', '612177b8-530a-4e86-b2cf-514cbdb6586d', 2.87, 33.33, 0, 1.47, 0.93, 0, 0, 69.07, 76.96, 0, 2.02, 0.58, 52, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('76322e07-6786-4920-9fed-84d3ae2d35a0', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 2.45, 42.66, 0, 0, 0.38, 1.55, 0, 0, 32.29, 31.37, 1.84, 0.6, 36, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('794112c2-fd11-4938-ac0c-b53d81c37f9c', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.77, 41.95, 0, 0.1, 0.4, 0.27, 0, 70.87, 76.46, 86.34, 0.94, 0.74, 48, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('7a24738d-72c6-478b-b066-6d1b8d0a3f81', 'ebe800b7-4ef5-4656-a315-8f9ecb5cf59d', 3.3, 25.02, 0, 2.83, 0.47, 0, 0, 65.15, 72.53, 0, 1.63, 0.71, 14, '2024-06-06 17:12:48', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('7eb13fde-147e-4458-b4f7-7b4a1a04680c', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.4, 0.95, 0.5, 0, 0, 0, 50.21, 0, 0, 0, 146.53, 0.57, 81, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('833c534f-39d8-4f89-9af0-5257c287d6fb', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.28, 41.65, 0, 0.28, 0.48, 0.52, 0, 69.31, 76.21, 86.2, 3.55, 0.66, 24, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('845079ac-5c4d-4ed3-8717-0a69d5c1052d', '25de3614-826a-41c6-965f-8ad01ec7f00d', 3.3, 25.02, 0, 2.83, 0.47, 0, 0, 65.15, 72.53, 0, 1.63, 0.71, 9, '2024-06-06 17:09:43', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('87efb251-61b6-4ade-854c-c74f83ad7129', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.79, 20.3, 0, 1.41, 0, 0, 0, 66.7, 0, 0, 1.94, 0.65, 40, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('90db6bde-9434-45c0-b0c7-01ab010666c0', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.34, 42.6, 0, 0.72, 0.38, 0.24, 0, 66.3, 77.08, 87.46, 0.77, 0.71, 2, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('9d835e41-602a-4da9-8920-0b9576bbd2ec', '25de3614-826a-41c6-965f-8ad01ec7f00d', 2.03, 42.59, 0, 0, 0.97, 1.07, 0, 0, 77.99, 86.99, 3.04, 0.67, 6, '2024-06-06 17:09:43', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('9e27370b-965c-4b27-b309-6c923c9c9a7f', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 8.48, 42.01, 0, 2.48, 3.66, 1.66, 0, 37.99, 35.04, 32.54, 1.35, 0.73, 3, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('a2845c30-c209-46cc-bef2-c35ea4a545db', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.17, 41.93, 0, 0.37, 0.47, 0.33, 0, 69.06, 76.38, 86.67, 1.62, 0.73, 72, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('a365667d-8e93-4966-a21f-f35c39c4d98c', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 7.21, 43.36, 0, 2, 3, 1.79, 0, 38.28, 35.11, 32.73, 1.47, 0.74, 28, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('a5d157ad-81cc-4af6-b6fa-cebb386c0df4', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.2, 43.21, 0.07, 0.6, 0.3, 0.23, 62.23, 67.14, 77.87, 88.35, 1.87, 0.68, 54, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('acdef2f2-b305-4518-a574-8bebc349a86c', 'ebe800b7-4ef5-4656-a315-8f9ecb5cf59d', 1.03, 12.75, 0.33, 0.7, 0, 0, 59.96, 61.13, 0, 0, 1.09, 0.68, 15, '2024-06-06 17:12:48', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('b26a9061-c4a3-4eb2-800c-24a76b87047e', '25de3614-826a-41c6-965f-8ad01ec7f00d', 1.03, 12.75, 0.33, 0.7, 0, 0, 59.96, 61.13, 0, 0, 1.09, 0.68, 10, '2024-06-06 17:09:43', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('b369925c-31f5-4391-84fb-35c5eef90d69', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.7, 36.17, 0, 0.23, 0.63, 0.17, 0, 67.78, 81.48, 85.01, 15.91, 0.57, 78, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('bccad289-bcf4-4315-b147-565312884ced', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.55, 42.12, 0.21, 0.72, 0.38, 0.24, 60.83, 65.86, 76.47, 86.88, 0.67, 0.72, 13, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('bee3837b-ca30-4436-8176-900ed6bc5469', '612177b8-530a-4e86-b2cf-514cbdb6586d', 6.47, 42.65, 0, 2.73, 2.1, 1.53, 0, 67.53, 76.56, 86.89, 2, 0.72, 49, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('bf07c52d-0c01-4e82-8d1c-8f94b8785215', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.37, 41.93, 0, 0, 0, 0.37, 0, 0, 0, 28.2, 1.58, 0.68, 51, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('c73797da-cccc-41ba-870f-a187d24eb8ec', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 0.1, 29.89, 0, 0, 0.1, 0, 0, 0, 34.39, 0, 0.81, 0.56, 16, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('ca6c92fe-6adb-446d-9b68-daa7cc363ada', 'ebe800b7-4ef5-4656-a315-8f9ecb5cf59d', 2.03, 42.59, 0, 0, 0.97, 1.07, 0, 0, 77.99, 86.99, 3.04, 0.67, 11, '2024-06-06 17:12:48', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('d141c2a7-cc14-443c-bdf2-fdccbde9d64e', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 2.76, 43.17, 0, 0, 0.31, 2.17, 0, 0, 33.27, 33.32, 3.05, 0.62, 25, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('d8befd4a-78db-4ba9-a523-3aa36854eb23', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.13, 42.34, 0, 0.33, 0.47, 0.33, 0, 69.47, 76.39, 86.55, 0.88, 0.71, 73, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('e2828a10-d100-490f-a1e1-95a921411b96', '612177b8-530a-4e86-b2cf-514cbdb6586d', 2.2, 42.16, 0, 0, 0, 1.67, 0, 0, 0, 30.32, 1.22, 0.59, 47, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('e5306d52-0114-45db-9571-dbc47bfbbdd5', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 2.03, 20.52, 0, 1.24, 0, 0, 0, 68.38, 0, 0, 1.02, 0.58, 23, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('e5b697f9-5670-4f8c-9f93-9eabd5d970f6', 'fc3b9d48-2862-4ff0-92e3-f8bda5b6a3d6', 3.3, 25.02, 0, 2.83, 0.47, 0, 0, 65.15, 72.53, 0, 1.63, 0.71, 4, '2024-06-06 17:35:38', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('ea2a3f34-c1a5-4e8e-ab0d-68999a3bcf94', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.87, 40.93, 0, 0.43, 0.3, 0.13, 0, 38.91, 35.17, 32.64, 1.43, 0.68, 71, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('edc82afd-a67e-4c31-a51b-a34ad8f59f83', 'f98f63e7-9eb4-4811-a258-6110d5591ece', 1.69, 42.8, 0.28, 0.79, 0.34, 0.28, 61.24, 66.58, 77.06, 87.27, 0.73, 0.73, 17, '2024-05-28 18:25:02', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('f9ed2db1-d990-4478-aab4-4bdf23d1dc3f', '612177b8-530a-4e86-b2cf-514cbdb6586d', 0.63, 36.91, 0, 0, 0, 0.27, 0, 0, 0, 30.75, 0.76, 0.52, 43, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('fb27aac5-9729-4b42-aaa5-854c063cf176', 'ebe800b7-4ef5-4656-a315-8f9ecb5cf59d', 4.37, 42.26, 0, 1.83, 1.57, 0.97, 0, 66.92, 75.98, 87.01, 2.46, 0.7, 12, '2024-06-06 17:12:48', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0),
('fea04933-f233-4a90-b981-3076b1252874', '612177b8-530a-4e86-b2cf-514cbdb6586d', 1.07, 41.69, 0, 0.37, 0.47, 0.23, 0, 69.62, 77.55, 87.38, 1.35, 0.7, 70, '2024-05-26 16:35:59', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0);

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
  `status` int(2) NOT NULL DEFAULT 1
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
('25de3614-826a-41c6-965f-8ad01ec7f00d', '5strimmed_nd_d2594a.mp4', 3, 11, 8, '2024-06-06 17:09:43', 1, 'C:\\Users\\sande\\OneDrive\\Desktop\\study-material\\upload\\loc8_backend\\instance\\5strimmed_nd_d2594a.mp4', 0, 0),
('612177b8-530a-4e86-b2cf-514cbdb6586d', '3be712f0-dbc1-40df-8e6c-4a2b398fb394.mp4', 3, 11, 8, '2024-05-26 16:35:59', 1, 'C:\\Users\\sande\\OneDrive\\Desktop\\study-material\\upload\\loc8_backend\\instance\\3be712f0-dbc1-40df-8e6c-4a2b398fb394.mp4', 0, 0),
('ebe800b7-4ef5-4656-a315-8f9ecb5cf59d', '5strimmed_nd_f8441f.mp4', 3, 11, 8, '2024-06-06 17:12:48', 1, 'C:\\Users\\sande\\OneDrive\\Desktop\\study-material\\upload\\loc8_backend\\instance\\5strimmed_nd_f8441f.mp4', 0, 0),
('f98f63e7-9eb4-4811-a258-6110d5591ece', '5de88ccb-f698-41a2-b5cf-a533e17129fc.mp4', 3, 11, 8, '2024-05-28 18:25:02', 1, 'C:\\Users\\sande\\OneDrive\\Desktop\\study-material\\upload\\loc8_backend\\instance\\5de88ccb-f698-41a2-b5cf-a533e17129fc.mp4', 0, 0),
('fc3b9d48-2862-4ff0-92e3-f8bda5b6a3d6', '5strimmed_nd_c1e68c.mp4', 3, 11, 8, '2024-06-06 17:35:38', 1, 'C:\\Users\\sande\\OneDrive\\Desktop\\study-material\\upload\\loc8_backend\\instance\\5strimmed_nd_c1e68c.mp4', 0, 0);

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
('612177b8-530a-4e86-b2cf-514cbdb6586d', 23, 80, 18.929500, 73.162400),
('612177b8-530a-4e86-b2cf-514cbdb6586d', 24, 73, 18.927900, 73.164000),
('612177b8-530a-4e86-b2cf-514cbdb6586d', 25, 76, 18.926600, 73.165100),
('612177b8-530a-4e86-b2cf-514cbdb6586d', 26, 80, 18.925000, 73.166400),
('612177b8-530a-4e86-b2cf-514cbdb6586d', 27, 75, 18.923600, 73.167900),
('612177b8-530a-4e86-b2cf-514cbdb6586d', 28, 70, 18.922300, 73.169400),
('612177b8-530a-4e86-b2cf-514cbdb6586d', 29, 54, 18.921400, 73.170400),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 38, 89, 18.941700, 73.157000),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 39, 89, 18.939500, 73.157600),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 40, 89, 18.937400, 73.158200),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 41, 89, 18.935200, 73.158900),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 42, 89, 18.932900, 73.159900),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 43, 89, 18.931200, 73.161000),
('f98f63e7-9eb4-4811-a258-6110d5591ece', 44, 80, 18.929500, 73.162400),
('25de3614-826a-41c6-965f-8ad01ec7f00d', 47, 71, 19.018300, 73.106100),
('ebe800b7-4ef5-4656-a315-8f9ecb5cf59d', 48, 71, 19.018300, 73.106100),
('fc3b9d48-2862-4ff0-92e3-f8bda5b6a3d6', 49, 71, 19.018300, 73.106100);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

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
