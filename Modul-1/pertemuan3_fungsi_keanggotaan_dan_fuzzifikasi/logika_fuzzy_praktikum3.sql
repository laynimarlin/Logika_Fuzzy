-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 04, 2026 at 04:27 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `logika_fuzzy_praktikum3`
--

-- --------------------------------------------------------

--
-- Table structure for table `anak`
--

DROP TABLE IF EXISTS `anak`;
CREATE TABLE IF NOT EXISTS `anak` (
  `b_bawah` decimal(5,2) DEFAULT NULL,
  `b_atas` decimal(5,2) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `anak`
--

INSERT INTO `anak` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(6.00, 8.50, 'naik_anak'),
(8.50, 11.00, 'turun_anak'),
(11.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `bayi`
--

DROP TABLE IF EXISTS `bayi`;
CREATE TABLE IF NOT EXISTS `bayi` (
  `b_bawah` decimal(5,2) DEFAULT NULL,
  `b_atas` decimal(5,2) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bayi`
--

INSERT INTO `bayi` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(0.00, 2.50, 'naik_bayi'),
(2.50, 5.00, 'turun_bayi'),
(5.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `dewasa`
--

DROP TABLE IF EXISTS `dewasa`;
CREATE TABLE IF NOT EXISTS `dewasa` (
  `b_bawah` decimal(5,2) DEFAULT NULL,
  `b_atas` decimal(5,2) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `dewasa`
--

INSERT INTO `dewasa` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(20.00, 42.50, 'naik_dewasa'),
(42.50, 65.00, 'turun_dewasa'),
(65.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `lansia`
--

DROP TABLE IF EXISTS `lansia`;
CREATE TABLE IF NOT EXISTS `lansia` (
  `b_bawah` decimal(5,2) DEFAULT NULL,
  `b_atas` decimal(5,2) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lansia`
--

INSERT INTO `lansia` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(60.00, 70.00, 'naik_lansia'),
(70.00, 80.00, 'turun_lansia'),
(80.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `pemuda`
--

DROP TABLE IF EXISTS `pemuda`;
CREATE TABLE IF NOT EXISTS `pemuda` (
  `b_bawah` decimal(5,2) DEFAULT NULL,
  `b_atas` decimal(5,2) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pemuda`
--

INSERT INTO `pemuda` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(15.00, 19.50, 'naik_pemuda'),
(19.50, 24.00, 'turun_pemuda'),
(24.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `remaja`
--

DROP TABLE IF EXISTS `remaja`;
CREATE TABLE IF NOT EXISTS `remaja` (
  `b_bawah` decimal(5,2) DEFAULT NULL,
  `b_atas` decimal(5,2) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `remaja`
--

INSERT INTO `remaja` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(10.00, 14.50, 'naik_remaja'),
(14.50, 19.00, 'turun_remaja'),
(19.00, 150.00, '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
