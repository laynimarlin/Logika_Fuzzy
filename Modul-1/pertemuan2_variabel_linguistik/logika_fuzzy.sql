-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 04, 2026 at 04:34 PM
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
-- Database: `logika_fuzzy`
--

-- --------------------------------------------------------

--
-- Table structure for table `anak`
--

DROP TABLE IF EXISTS `anak`;
CREATE TABLE IF NOT EXISTS `anak` (
  `b_bawah` decimal(5,2) NOT NULL,
  `b_atas` decimal(5,2) NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `anak`
--

INSERT INTO `anak` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(6.00, 8.00, 'naik_anak'),
(8.00, 9.00, '1'),
(9.00, 11.00, 'trapesium_down_anak'),
(11.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `bayi`
--

DROP TABLE IF EXISTS `bayi`;
CREATE TABLE IF NOT EXISTS `bayi` (
  `b_bawah` decimal(5,2) NOT NULL,
  `b_atas` decimal(5,2) NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bayi`
--

INSERT INTO `bayi` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(0.00, 2.00, 'naik_bayi'),
(2.00, 3.00, '1'),
(3.00, 5.00, 'trapesium_down_bayi'),
(5.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `dewasa`
--

DROP TABLE IF EXISTS `dewasa`;
CREATE TABLE IF NOT EXISTS `dewasa` (
  `b_bawah` decimal(5,2) NOT NULL,
  `b_atas` decimal(5,2) NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `dewasa`
--

INSERT INTO `dewasa` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(20.00, 42.00, 'naik_dewasa'),
(42.00, 43.00, '1'),
(43.00, 65.00, 'trapesium_down_dewasa'),
(65.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `lansia`
--

DROP TABLE IF EXISTS `lansia`;
CREATE TABLE IF NOT EXISTS `lansia` (
  `b_bawah` decimal(5,2) NOT NULL,
  `b_atas` decimal(5,2) NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lansia`
--

INSERT INTO `lansia` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(60.00, 69.50, 'naik_lansia'),
(69.50, 70.50, '1'),
(70.50, 80.00, 'trapesium_down_lansia'),
(80.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `pemuda`
--

DROP TABLE IF EXISTS `pemuda`;
CREATE TABLE IF NOT EXISTS `pemuda` (
  `b_bawah` decimal(5,2) NOT NULL,
  `b_atas` decimal(5,2) NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pemuda`
--

INSERT INTO `pemuda` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(15.00, 19.00, 'naik_pemuda'),
(19.00, 20.00, '1'),
(20.00, 24.00, 'trapesium_down_pemuda'),
(24.00, 150.00, '0');

-- --------------------------------------------------------

--
-- Table structure for table `remaja`
--

DROP TABLE IF EXISTS `remaja`;
CREATE TABLE IF NOT EXISTS `remaja` (
  `b_bawah` decimal(5,2) NOT NULL,
  `b_atas` decimal(5,2) NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `remaja`
--

INSERT INTO `remaja` (`b_bawah`, `b_atas`, `fungsi`) VALUES
(10.00, 14.00, 'naik_remaja'),
(14.00, 15.00, '1'),
(15.00, 19.00, 'trapesium_down_remaja'),
(19.00, 150.00, '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
