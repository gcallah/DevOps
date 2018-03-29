package { 'git' :
  ensure => present,
}
vcsrepo { '/var/www/html':
  ensure   => latest,
  provider => git,
  source   => 'http://github.com/gcallah/DevOps.git',
  revision => 'master',
}
