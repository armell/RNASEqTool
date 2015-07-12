-- phpMyAdmin SQL Dump
-- version 4.2.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 12, 2015 at 09:27 PM
-- Server version: 5.5.41-0ubuntu0.14.10.1
-- PHP Version: 5.5.12-2ubuntu4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `rnaseqtool`
--
CREATE DATABASE IF NOT EXISTS `rnaseqtool` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `rnaseqtool`;

-- --------------------------------------------------------

--
-- Table structure for table `datasets`
--

DROP TABLE IF EXISTS `datasets`;
CREATE TABLE IF NOT EXISTS `datasets` (
`id` int(11) NOT NULL,
  `added_on` date NOT NULL,
  `intern_location` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `url` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `size` int(11) NOT NULL,
  `public_identifier` varchar(250) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `generation_type` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `granularity_level` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `is_raw` tinyint(1) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `raw_content` longblob,
  `compressed_location` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `intern_identifier` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `number_samples` int(11) NOT NULL,
  `number_features` int(11) NOT NULL,
  `feature_type` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `package_id` int(11) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=90 ;

-- --------------------------------------------------------

--
-- Table structure for table `dataset_genes_outliers`
--

DROP TABLE IF EXISTS `dataset_genes_outliers`;
CREATE TABLE IF NOT EXISTS `dataset_genes_outliers` (
`id` bigint(20) NOT NULL,
  `gene_id` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `dataset_id` int(11) NOT NULL,
  `method_id` int(11) DEFAULT NULL,
  `rank_score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `dataset_samples`
--

DROP TABLE IF EXISTS `dataset_samples`;
CREATE TABLE IF NOT EXISTS `dataset_samples` (
`id` bigint(20) NOT NULL,
  `identifier` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `sequencing_platform` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `control` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `dataset_types`
--

DROP TABLE IF EXISTS `dataset_types`;
CREATE TABLE IF NOT EXISTS `dataset_types` (
`id` int(11) NOT NULL,
  `name` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `description` text CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `first_sample` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Table structure for table `ensembl_name_conversion`
--

DROP TABLE IF EXISTS `ensembl_name_conversion`;
CREATE TABLE IF NOT EXISTS `ensembl_name_conversion` (
`id` bigint(20) NOT NULL,
  `ensembl_id` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `name` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `ensembl_version` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `experiments`
--

DROP TABLE IF EXISTS `experiments`;
CREATE TABLE IF NOT EXISTS `experiments` (
`id` bigint(20) NOT NULL,
  `created_on` date NOT NULL,
  `type` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `public_identifier` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `description` text CHARACTER SET latin1 COLLATE latin1_general_ci,
  `context` text CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

-- --------------------------------------------------------

--
-- Table structure for table `experiment_dataset`
--

DROP TABLE IF EXISTS `experiment_dataset`;
CREATE TABLE IF NOT EXISTS `experiment_dataset` (
  `experiment_id` bigint(20) NOT NULL,
  `dataset_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `experiment_package`
--

DROP TABLE IF EXISTS `experiment_package`;
CREATE TABLE IF NOT EXISTS `experiment_package` (
  `experiment_id` bigint(20) NOT NULL,
  `package_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `experiment_visualization`
--

DROP TABLE IF EXISTS `experiment_visualization`;
CREATE TABLE IF NOT EXISTS `experiment_visualization` (
  `experiment_id` bigint(20) NOT NULL,
  `visualization_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `generated_content`
--

DROP TABLE IF EXISTS `generated_content`;
CREATE TABLE IF NOT EXISTS `generated_content` (
`id` bigint(20) NOT NULL,
  `experiment` bigint(11) NOT NULL,
  `dataset` int(11) NOT NULL,
  `method` int(11) NOT NULL,
  `binary_content` longblob NOT NULL,
  `generated_on` date NOT NULL,
  `public_identifier` varchar(250) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `mime_type` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `job_executed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `GenesWithFamily`
--

DROP TABLE IF EXISTS `GenesWithFamily`;
CREATE TABLE IF NOT EXISTS `GenesWithFamily` (
  `Ensembl Gene ID` varchar(15) DEFAULT NULL,
  `Associated Gene Name` varchar(22) DEFAULT NULL,
  `Gene type` varchar(24) DEFAULT NULL,
  `Ensembl Family Description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `gene_length_ensembl`
--

DROP TABLE IF EXISTS `gene_length_ensembl`;
CREATE TABLE IF NOT EXISTS `gene_length_ensembl` (
  `Ensembl Gene ID` varchar(15) DEFAULT NULL,
  `Gene Start (bp)` int(9) DEFAULT NULL,
  `Gene End (bp)` int(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `gene_visualizations`
--

DROP TABLE IF EXISTS `gene_visualizations`;
CREATE TABLE IF NOT EXISTS `gene_visualizations` (
  `id` bigint(20) NOT NULL,
  `visualization_id` bigint(20) NOT NULL,
  `feature_identifier` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `sample_identifier` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `metadata_sources`
--

DROP TABLE IF EXISTS `metadata_sources`;
CREATE TABLE IF NOT EXISTS `metadata_sources` (
`id` int(11) NOT NULL,
  `name` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `description` text CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `public_identifier` varchar(250) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `version` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `methods`
--

DROP TABLE IF EXISTS `methods`;
CREATE TABLE IF NOT EXISTS `methods` (
`id` int(11) NOT NULL,
  `name` varchar(150) CHARACTER SET latin1 NOT NULL,
  `description` text CHARACTER SET latin1 NOT NULL,
  `public_identifier` varchar(150) CHARACTER SET latin1 NOT NULL,
  `updated` date NOT NULL,
  `type` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

-- --------------------------------------------------------

--
-- Table structure for table `method_package`
--

DROP TABLE IF EXISTS `method_package`;
CREATE TABLE IF NOT EXISTS `method_package` (
  `method_id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `applied_on` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `method_types`
--

DROP TABLE IF EXISTS `method_types`;
CREATE TABLE IF NOT EXISTS `method_types` (
`id` int(11) NOT NULL,
  `name` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `description` text CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `rank` int(11) NOT NULL,
  `Reference` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

-- --------------------------------------------------------

--
-- Table structure for table `mining`
--

DROP TABLE IF EXISTS `mining`;
CREATE TABLE IF NOT EXISTS `mining` (
`id` bigint(20) NOT NULL,
  `dataset_id` int(11) NOT NULL,
  `method_id` int(11) NOT NULL,
  `support` int(11) NOT NULL,
  `min_samples` int(11) NOT NULL,
  `min_distance` float NOT NULL,
  `created_on` date NOT NULL,
  `public_identifier` varchar(250) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `is_executed` tinyint(1) NOT NULL,
  `experiment_id` bigint(20) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=58 ;

-- --------------------------------------------------------

--
-- Table structure for table `mining_result`
--

DROP TABLE IF EXISTS `mining_result`;
CREATE TABLE IF NOT EXISTS `mining_result` (
`id` bigint(20) NOT NULL,
  `mining_id` bigint(20) NOT NULL,
  `feature_id` varchar(15) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `distance` float DEFAULT NULL,
  `range` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `name_gene_ensembl`
--

DROP TABLE IF EXISTS `name_gene_ensembl`;
CREATE TABLE IF NOT EXISTS `name_gene_ensembl` (
  `EnsemblGeneID` varchar(15) DEFAULT NULL,
  `GeneType` varchar(24) DEFAULT NULL,
  `GeneName` varchar(22) DEFAULT NULL,
  `Version` varchar(50) NOT NULL,
  `FamilyDescription` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `packages`
--

DROP TABLE IF EXISTS `packages`;
CREATE TABLE IF NOT EXISTS `packages` (
`id` int(11) NOT NULL,
  `public_identifier` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `language` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `version` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `added_on` date NOT NULL,
  `description` text CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `url_source` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `reference` varchar(500) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `name` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=20 ;

-- --------------------------------------------------------

--
-- Table structure for table `patient_information`
--

DROP TABLE IF EXISTS `patient_information`;
CREATE TABLE IF NOT EXISTS `patient_information` (
`id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `preprocessing`
--

DROP TABLE IF EXISTS `preprocessing`;
CREATE TABLE IF NOT EXISTS `preprocessing` (
`id` int(11) NOT NULL,
  `generated_on` date NOT NULL,
  `experiment_id` bigint(20) NOT NULL,
  `dataset_id` int(11) NOT NULL,
  `method_id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `public_identifier` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `outlier_threshold` int(11) NOT NULL,
  `rows_affected` int(11) NOT NULL,
  `colums_affected` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `preprocessing_result`
--

DROP TABLE IF EXISTS `preprocessing_result`;
CREATE TABLE IF NOT EXISTS `preprocessing_result` (
  `id` bigint(20) NOT NULL,
  `preprocessing_id` int(11) NOT NULL,
  `removed_feature` varchar(150) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
CREATE TABLE IF NOT EXISTS `reports` (
`id` int(11) NOT NULL,
  `name` int(11) NOT NULL,
  `language` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `package` int(11) NOT NULL,
  `public_identifier` varchar(250) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `binary` longblob NOT NULL,
  `updated_on` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `TABLE 26`
--

DROP TABLE IF EXISTS `TABLE 26`;
CREATE TABLE IF NOT EXISTS `TABLE 26` (
  `Ensembl Gene ID` varchar(15) DEFAULT NULL,
  `Ensembl Protein Family ID(s)` varchar(19) DEFAULT NULL,
  `Ensembl Family Description` varchar(255) DEFAULT NULL,
  `Associated Gene Name` varchar(22) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `visualizations`
--

DROP TABLE IF EXISTS `visualizations`;
CREATE TABLE IF NOT EXISTS `visualizations` (
`id` bigint(20) NOT NULL,
  `public_identifier` varchar(150) CHARACTER SET latin1 NOT NULL,
  `created_on` date NOT NULL,
  `type` varchar(50) CHARACTER SET latin1 NOT NULL,
  `chart_data` blob NOT NULL,
  `generated_by` varchar(50) CHARACTER SET latin1 NOT NULL,
  `mime_type` varchar(200) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `dataset_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `datasets`
--
ALTER TABLE `datasets`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `public_identifier` (`public_identifier`), ADD KEY `type` (`type`), ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `dataset_genes_outliers`
--
ALTER TABLE `dataset_genes_outliers`
 ADD PRIMARY KEY (`id`), ADD KEY `gene_id` (`gene_id`), ADD KEY `dataset_id` (`dataset_id`), ADD KEY `method_id` (`method_id`), ADD KEY `dataset_id_2` (`dataset_id`), ADD KEY `gene_id_2` (`gene_id`), ADD KEY `method_id_2` (`method_id`);

--
-- Indexes for table `dataset_samples`
--
ALTER TABLE `dataset_samples`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dataset_types`
--
ALTER TABLE `dataset_types`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ensembl_name_conversion`
--
ALTER TABLE `ensembl_name_conversion`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experiments`
--
ALTER TABLE `experiments`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `public_identifier` (`public_identifier`);

--
-- Indexes for table `experiment_dataset`
--
ALTER TABLE `experiment_dataset`
 ADD PRIMARY KEY (`experiment_id`,`dataset_id`), ADD KEY `dataset_id` (`dataset_id`);

--
-- Indexes for table `experiment_package`
--
ALTER TABLE `experiment_package`
 ADD PRIMARY KEY (`experiment_id`,`package_id`), ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `experiment_visualization`
--
ALTER TABLE `experiment_visualization`
 ADD PRIMARY KEY (`experiment_id`,`visualization_id`), ADD KEY `visualization_id` (`visualization_id`);

--
-- Indexes for table `generated_content`
--
ALTER TABLE `generated_content`
 ADD PRIMARY KEY (`id`), ADD KEY `experiment` (`experiment`), ADD KEY `dataset` (`dataset`), ADD KEY `method` (`method`);

--
-- Indexes for table `gene_visualizations`
--
ALTER TABLE `gene_visualizations`
 ADD KEY `visualization_id` (`visualization_id`);

--
-- Indexes for table `metadata_sources`
--
ALTER TABLE `metadata_sources`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `public_identifier` (`public_identifier`);

--
-- Indexes for table `methods`
--
ALTER TABLE `methods`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `public_identifier` (`public_identifier`), ADD KEY `type` (`type`), ADD KEY `type_2` (`type`), ADD KEY `type_3` (`type`), ADD KEY `type_4` (`type`);

--
-- Indexes for table `method_package`
--
ALTER TABLE `method_package`
 ADD PRIMARY KEY (`method_id`,`package_id`), ADD KEY `method_id` (`method_id`), ADD KEY `package_id` (`package_id`), ADD KEY `method_id_2` (`method_id`,`package_id`);

--
-- Indexes for table `method_types`
--
ALTER TABLE `method_types`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `mining`
--
ALTER TABLE `mining`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `public_identifier` (`public_identifier`), ADD KEY `dataset_id` (`dataset_id`), ADD KEY `method_id` (`method_id`), ADD KEY `experiment_id` (`experiment_id`);

--
-- Indexes for table `mining_result`
--
ALTER TABLE `mining_result`
 ADD PRIMARY KEY (`id`), ADD KEY `mining_id` (`mining_id`), ADD KEY `feature_id` (`feature_id`), ADD KEY `mining_id_2` (`mining_id`);

--
-- Indexes for table `packages`
--
ALTER TABLE `packages`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patient_information`
--
ALTER TABLE `patient_information`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `preprocessing`
--
ALTER TABLE `preprocessing`
 ADD PRIMARY KEY (`id`), ADD KEY `experiment_id` (`experiment_id`), ADD KEY `dataset_id` (`dataset_id`,`method_id`), ADD KEY `method_id` (`method_id`), ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `preprocessing_result`
--
ALTER TABLE `preprocessing_result`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `visualizations`
--
ALTER TABLE `visualizations`
 ADD PRIMARY KEY (`id`), ADD KEY `dataset_id` (`dataset_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `datasets`
--
ALTER TABLE `datasets`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=90;
--
-- AUTO_INCREMENT for table `dataset_genes_outliers`
--
ALTER TABLE `dataset_genes_outliers`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dataset_samples`
--
ALTER TABLE `dataset_samples`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dataset_types`
--
ALTER TABLE `dataset_types`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `ensembl_name_conversion`
--
ALTER TABLE `ensembl_name_conversion`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `experiments`
--
ALTER TABLE `experiments`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `generated_content`
--
ALTER TABLE `generated_content`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `metadata_sources`
--
ALTER TABLE `metadata_sources`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `methods`
--
ALTER TABLE `methods`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `method_types`
--
ALTER TABLE `method_types`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `mining`
--
ALTER TABLE `mining`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=58;
--
-- AUTO_INCREMENT for table `mining_result`
--
ALTER TABLE `mining_result`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `packages`
--
ALTER TABLE `packages`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `patient_information`
--
ALTER TABLE `patient_information`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `preprocessing`
--
ALTER TABLE `preprocessing`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `visualizations`
--
ALTER TABLE `visualizations`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `datasets`
--
ALTER TABLE `datasets`
ADD CONSTRAINT `datasets_ibfk_1` FOREIGN KEY (`type`) REFERENCES `dataset_types` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `datasets_ibfk_2` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `dataset_genes_outliers`
--
ALTER TABLE `dataset_genes_outliers`
ADD CONSTRAINT `dataset_genes_outliers_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `dataset_genes_outliers_ibfk_2` FOREIGN KEY (`method_id`) REFERENCES `methods` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `experiment_dataset`
--
ALTER TABLE `experiment_dataset`
ADD CONSTRAINT `experiment_dataset_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `experiment_dataset_ibfk_2` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `experiment_package`
--
ALTER TABLE `experiment_package`
ADD CONSTRAINT `experiment_package_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `experiment_package_ibfk_2` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `experiment_visualization`
--
ALTER TABLE `experiment_visualization`
ADD CONSTRAINT `experiment_visualization_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `experiment_visualization_ibfk_2` FOREIGN KEY (`visualization_id`) REFERENCES `visualizations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `generated_content`
--
ALTER TABLE `generated_content`
ADD CONSTRAINT `generated_content_ibfk_2` FOREIGN KEY (`dataset`) REFERENCES `datasets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `generated_content_ibfk_3` FOREIGN KEY (`method`) REFERENCES `methods` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `generated_content_ibfk_4` FOREIGN KEY (`experiment`) REFERENCES `experiments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `methods`
--
ALTER TABLE `methods`
ADD CONSTRAINT `methods_ibfk_1` FOREIGN KEY (`type`) REFERENCES `method_types` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `method_package`
--
ALTER TABLE `method_package`
ADD CONSTRAINT `method_package_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `method_package_ibfk_2` FOREIGN KEY (`method_id`) REFERENCES `methods` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `mining`
--
ALTER TABLE `mining`
ADD CONSTRAINT `mining_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `mining_ibfk_2` FOREIGN KEY (`method_id`) REFERENCES `methods` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `mining_ibfk_3` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `mining_result`
--
ALTER TABLE `mining_result`
ADD CONSTRAINT `fk_result_mining` FOREIGN KEY (`mining_id`) REFERENCES `mining` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `preprocessing`
--
ALTER TABLE `preprocessing`
ADD CONSTRAINT `preprocessing_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `preprocessing_ibfk_2` FOREIGN KEY (`method_id`) REFERENCES `methods` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `preprocessing_ibfk_3` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `preprocessing_ibfk_4` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
