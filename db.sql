CREATE TABLE `sentiments` (
  `id` text,
  `query` text,
  `tweet` text,
  `pos` float DEFAULT NULL,
  `neg` float DEFAULT NULL,
  `neutral` float DEFAULT NULL,
  `label` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 
