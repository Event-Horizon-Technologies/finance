# Overview

An attempt to disprove the [efficient market hypothesis](https://en.wikipedia.org/wiki/Efficient-market_hypothesis). There are many models out there, without much statistics backing them up. So we will test and confirm the validaty of them all. Here is some information:

* [Jim Simmons](https://en.wikipedia.org/wiki/Jim_Simons_(mathematician))
  * [Renaissance Technology](https://en.wikipedia.org/wiki/Renaissance_Technologies#Medallion_Fund)
* [Fama French three-factor model](https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model) 
* [Carhart four-factor model](https://en.wikipedia.org/wiki/Carhart_four-factor_model)
* [Universal Portfolio](https://isl.stanford.edu/~cover/papers/paper93.pdf)
* [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
* [Efficient Frontier](https://en.wikipedia.org/wiki/Efficient_frontier)
* [Post-Modern Portfolio Theory](https://en.wikipedia.org/wiki/Post-modern_portfolio_theory)
* [Markowitz Model](https://en.wikipedia.org/wiki/Markowitz_model)
* [Black Litterman Model](https://en.wikipedia.org/wiki/Black%E2%80%93Litterman_model)
* [Black Scholes Model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
### High Frequency Trading (HFT)
* https://dm13450.github.io/2022/02/02/Order-Flow-Imbalance.html
* https://arxiv.org/pdf/1011.6402.pdf
* https://www.sciencedirect.com/science/article/abs/pii/S1386418115000415#:~:text=The%20Lee%20and%20Ready%20(1991,that%20occur%20at%20the%20midpoint.

## Front End
### ReactJS
Install cURL with: 

    sudo apt install curl

Install nvm, with: 

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
    
Install the current stable LTS release of Node.js: 

    nvm install --lts
    
Install react scripts:

    npm install react-scripts
    
Inside the root of the web app, start the web application with:

    npm start

## Back End
FastAPI

## Database
### MySQL

#### Install MySQL:

    sudo apt install mysql-server

Confirm it installed successfully and is active:

    systemctl status mysql

Connect to MySQL Server with the client:

    sudo mysql -u root 

#### Set a password for root:

Log in as root:

    sudo mysql -u root
    
Add a password for root, replacing `<password>` with your password:

    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>'; 

Log out of MySQL by executing `exit;` then restart the MySQL service:

    sudo service mysql restart
