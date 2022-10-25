Install mysql
$ sudo apt install mysql-server

Confirm it installed successfully and is active:
$ systemctl status mysql

Connect to MySQL Server with the client
$ sudo mysql -u root 

Set a password for root 
$ sudo mysql -u root
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new-password';
mysql> exit;
$ sudo service mysql restart