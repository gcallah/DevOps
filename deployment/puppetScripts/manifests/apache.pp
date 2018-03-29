package { 'httpd':
   ensure => installed,
}
service { 'httpd':
   ensure => running
}
