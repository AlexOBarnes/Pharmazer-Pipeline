-- Schema for pubmed database
DROP TABLE IF EXISTS `mesh_assignment`;
DROP TABLE IF EXISTS `keyword_assignment`;
DROP TABLE IF EXISTS `keywords`;
DROP TABLE IF EXISTS `affiliation_assignment`;
DROP TABLE IF EXISTS `article_assignment`;
DROP TABLE IF EXISTS `affiliation`;
DROP TABLE IF EXISTS `article`;
DROP TABLE IF EXISTS `mesh`;
DROP TABLE IF EXISTS `author`;


CREATE TABLE `mesh` (
    `mesh_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `mesh_word` VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE `author` (
    `author_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `forename` VARCHAR(255) NOT NULL,
    `surname` VARCHAR(255) NOT NULL,
    `email` TEXT
);

CREATE TABLE `keywords` (
    `keyword_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `keyword` VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE `affiliation` (
    `grid_id` VARCHAR(255) NOT NULL,
    `affiliate_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`grid_id`)
);

CREATE TABLE `article` (
    `pmid` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` TEXT NOT NULL
);

CREATE TABLE `mesh_assignment` (
    `assignment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `pmid` BIGINT UNSIGNED NOT NULL,
    `mesh_id` BIGINT UNSIGNED NOT NULL,
    CONSTRAINT `mesh_assignment_mesh_id_foreign` FOREIGN KEY (`mesh_id`) REFERENCES `mesh` (`mesh_id`),
    CONSTRAINT `mesh_assignment_pmid_foreign` FOREIGN KEY (`pmid`) REFERENCES `article` (`pmid`)
);

CREATE TABLE `article_assignment` (
    `assignment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `pmid` BIGINT UNSIGNED NOT NULL,
    `author_id` BIGINT UNSIGNED NOT NULL,
    CONSTRAINT `affiliation_assignment_author_id_foreign` FOREIGN KEY (`author_id`) REFERENCES `author`(`author_id`),
    CONSTRAINT `affiliation_assignment_pmid_foreign` FOREIGN KEY (`pmid`) REFERENCES `article`(`pmid`)
);

CREATE TABLE `affiliation_assignment` (
    `assignment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `grid_id` VARCHAR(255) NOT NULL,
    `author_id` BIGINT UNSIGNED NOT NULL,
    CONSTRAINT `article_assignment_grid_id_foreign` FOREIGN KEY (`grid_id`) REFERENCES `affiliation`(`grid_id`),
    CONSTRAINT `article_assignment_author_id_foreign` FOREIGN KEY (`author_id`) REFERENCES `author`(`author_id`)
);

CREATE TABLE `keyword_assignment` (
    `assignment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `keyword_id` BIGINT UNSIGNED NOT NULL, 
    `pmid` BIGINT UNSIGNED NOT NULL,
    CONSTRAINT `keyword_assignment_keyword_id_foreign` FOREIGN KEY (`keyword_id`) REFERENCES `keywords`(`keyword_id`),
    CONSTRAINT `keyword_assignment_pmid_foreign` FOREIGN KEY (`pmid`) REFERENCES `article`(`pmid`)
);

