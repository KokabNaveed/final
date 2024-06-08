-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 08, 2024 at 07:11 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `audio`
--

-- --------------------------------------------------------

--
-- Table structure for table `uploads`
--

CREATE TABLE `uploads` (
  `audio_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  `bitrate` int(11) NOT NULL,
  `loudness_plot_path` varchar(255) NOT NULL,
  `waveform_plot_path` varchar(255) NOT NULL,
  `silence_speech_ratio_plot_path` varchar(255) NOT NULL,
  `plot_path_decibels` varchar(255) NOT NULL,
  `plot_path_sr` varchar(255) NOT NULL,
  `harmonicity_plot_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uploads`
--

INSERT INTO `uploads` (`audio_id`, `user_id`, `filename`, `bitrate`, `loudness_plot_path`, `waveform_plot_path`, `silence_speech_ratio_plot_path`, `plot_path_decibels`, `plot_path_sr`, `harmonicity_plot_path`) VALUES
(16, 8, '20240608183241_thirdfile.mp3', 64000, 'static\\Noor_20240608183241_thirdfile.mp3_loudness_plot.png', 'static\\Noor_20240608183241_thirdfile.mp3_waveform_with_peak.png', 'static\\Noor_20240608183241_thirdfile.mp3_silence_speech_ratio.png', 'static\\Noor_20240608183241_thirdfile.mp3_plot_path_sr.png', 'static\\Noor_20240608183241_thirdfile.mp3_waveform_with_sampling_rate.png', 'static\\Noor_20240608183241_thirdfile.mp3_harmonicity.png');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`) VALUES
(1, 'Kokab', 'kokabnaveed2002@gmail.com', 'yoursmile'),
(2, 'Areeba', 'areeba@gmail.com', '12345'),
(6, 'Aliha', 'alihaali@gmail.com', '54321'),
(7, 'Hadia', 'hadia@gmail.com', '789'),
(8, 'Noor', 'noor@gmail.com', '12345');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `uploads`
--
ALTER TABLE `uploads`
  ADD PRIMARY KEY (`audio_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `uploads`
--
ALTER TABLE `uploads`
  MODIFY `audio_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `uploads`
--
ALTER TABLE `uploads`
  ADD CONSTRAINT `uploads_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
